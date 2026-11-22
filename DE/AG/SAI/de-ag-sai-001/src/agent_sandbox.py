from microsandbox import (
    Sandbox,
    Network,
    NetworkPolicy,
    Action,
    Rule,
    Protocol,
    Secret,
    SecurityProfile
)
from langchain_backend_microsandbox import MicrosandboxSandbox
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
import uuid
from pathlib import Path
from api_utils import init_langfuse
import asyncio

# Init langfuse connector
_ , langfuse_handler = init_langfuse()
session_id = str(uuid.uuid4())
CONFIG = {"callbacks": [langfuse_handler], 
                        "metadata": {"langfuse_session_id": session_id,
                                     "langfuse_user_id": "test_agent",
                                     "langfuse_tags": ["agent-deepagent"]
                                     },
                        "configurable": {"thread_id": str(uuid.uuid4())}
        }


# Define the LLM model
model = init_chat_model("google_genai:gemma-4-26b-a4b-it")

# Define the SYSTEM PROMPT
SYSTEM_PROMPT="""
You are an agent capable of performing HTTP requests from your Python environment.

To perform HTTP requests:
- Use only Python's standard library `urllib.request`.
- Generate the required Python code based on the user's request.
- Retrieve and analyze the HTTP response.

You can perform GET and POST requests, add headers, send JSON data, and interact with REST APIs.

Be concise in your reasonning, only small sentences.

Rules:
1. Never use curl or pip.
2. Never ask the user to write Python code.
3. Always execute real HTTP requests.
4. Never simulate responses.
5. Display the HTTP status code and response body.
6. Clearly explain any errors.
7. Be as short as possible during your reasonning
8. If you receive a HTTP Error 403: Forbidden message, don't try to fix it and return the message to the user
"""

policy = NetworkPolicy(
    default_egress=Action.DENY,
    default_ingress=Action.DENY,
    rules=(
        *Rule.allow_dns(),
        Rule.allow(
            destination="httpbin.org",
            protocol=Protocol.TCP,
            port=443,
        ),
    ),
)

network = Network(policy=policy)

async def agent():

    sandbox = None
    backend = None

    try:
        # Create a sandbox for the agent harness
        sandbox = await Sandbox.create(
            "deep-agent",
            image="python:3.13",
            workdir="/tmp",
            # Sets no_new_privs, drops mount-admin capability from user commands, and forces nosuid,nodev on user mounts
            security=SecurityProfile.RESTRICTED,  # Good practice 2: Least privileges
            user="nobody",                        # Good practice 2: Least privileges
            memory=1024,                          # Good Practice 4: Define limited ressources (RAM)
            cpus=2,                               # Good Practice 4: Define limited ressources (CPU)
            network=network,                      # Good practice 5: Limited network
            secrets=[                             # Good practice 6: Secrets protection
                Secret.env(
                    "MY_VALUE",
                    value="123456",
                    allow=["httpbin.org"],
                )
            ],
            ephemeral=True,
        )
        
        backend = await MicrosandboxSandbox.create(
            sandbox,
            timeout=1800,        # Good Practice 4: Define limited ressources (Execution time)
        )

        await sandbox.exec("/bin/sh", ["-c", "mkdir -p /tmp/workspace && chmod 700 /tmp/workspace"], user="nobody")
        
        content = Path("src/python_test.py").read_bytes()
        await backend.aupload_files([("/tmp/workspace/python_test.py", content)])

        agent = create_deep_agent(model=model,
                                  backend=backend, # Good practice 1: Isolation by default
                                  system_prompt=SYSTEM_PROMPT,
                                #   interrupt_on={
                                #       "execute": True,  # Good practice 8: Human-in-the-loop (not implemented in this example)
                                #       },
                                    )
        
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": """Execute /tmp/workspace/python_test.py. 
                        Envoie le stdout dans le fichier /tmp/workspace/test.txt. Retourne le stdout en réponse.
                        Ne fais pas de vérification avec cat ou ls.
                        """,
                    }
                ]
            },
            config=CONFIG, # Good Practice 7: Monitoring
        )

        content_file = await backend.adownload_files(["/tmp/workspace/test.txt"])
        print(f"data: {content_file}")

    finally:
        if sandbox is not None:
            # Stop the sandbox and destroy it automatically (because `ephemeral=True`)
            await sandbox.stop() # Good practice 3: Temporary environment

asyncio.run(agent())

