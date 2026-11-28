import json
import asyncio
from langgraph_sdk import get_client
from pathlib import Path
from langgraph_sdk.client import LangGraphClient
import httpx

# Configuration
LANGGRAPH_URL = "http://localhost:2024"
GRAPH_ID = "my_agent"
TOKEN_FILE = "tokens.json"

def load_tokens(filepath: str) -> dict:
    data = json.loads(Path(filepath).read_text(encoding="utf-8"))
    return data

# ============================================================
# 1. Create assistants for each user
# ============================================================
# Create one assistant for each user in the token dictionary.

# Each assistant is created using the JWT token
# associated with its owner.

# Returns a dictionary mapping user names
# to their assistant IDs.
async def create_assistant(tokens: dict = None,
                           langgraph_url: str = None,
                           graph_id: str = None) -> list:

    assistants = {}
    for name in tokens:
        client = get_client(
            url=langgraph_url,
            headers={"Authorization": f"Bearer {tokens[name]}"},
        )

        assistant = await client.assistants.create(
            graph_id=graph_id,
            name=f"Assistant {name}",
            context={
                "system_prompt": f"you are an assistant created by {name}"
            },
        )
        assistants[name] = assistant['assistant_id']
        print(f"Assistant created for {name} -> ID : {assistant['assistant_id']}")
    return assistants

# ============================================================
# 2. Create an authenticated LangGraph client
# ============================================================
# All API requests made through this client will include
# the Authorization header.
def create_authenticated_client(url: str, token: str) -> LangGraphClient:
    return get_client(
        url=url,
        headers={"Authorization": f"Bearer {token}"},
    )

# ============================================================
# 3. Create a new thread
# ============================================================
# Returns the ID of the newly created thread.
async def create_user_thread(client: LangGraphClient) -> str:
    """Crée un nouveau thread et retourne son identifiant."""
    thread = await client.threads.create()
    return thread["thread_id"]

# ============================================================
# 4. Retrieve an existing thread
# ============================================================
# The thread ID is used to identify the requested resource.

# The server's authorization rules determine whether
# the authenticated user is allowed to access it.
async def get_user_thread(client: LangGraphClient, thread_id: str) -> str:
    """Récupère les informations d'un thread spécifique via son ID."""
    thread = await client.threads.get(thread_id)
    return thread["thread_id"]

# ============================================================
# 8. Execute an assistant
# ============================================================
async def query_assistant(
    client: LangGraphClient,
    thread_id: str,
    assistant_id: str,
    question: str,
    context=None
) -> str:

    result = await client.runs.wait(
        thread_id=thread_id,
        assistant_id=assistant_id,
        input={"messages": [{"role": "user", "content": question}]},
        context=context
    )

    content = result["messages"][-1]["content"]
    if isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"
        )

    return content

# ============================================================
# 9. Run an authorization test
# ============================================================
# Execute an authorization test.

# This function can test:
# - Access to an assistant
# - Access to an existing thread
# - Creation of a new thread
# - Stateless execution
# - Context validation
# - Permission restrictions

# The result or error is displayed in the console.
async def run_access_check(
    client: LangGraphClient,
    assistant_id: str,
    label: str,
    question: str = "Who has created this agent ? Give your response in 15 words max. Don't use any tool and respect all rules in context",
    with_thread: bool = True,
    thread_id: str = None,
    context=None,
) -> None:
    print(f"\n{'=' * 100}\n  {label} | Assistant: {assistant_id} | Thread: {thread_id}\n{'=' * 100}")

    try:
        if with_thread and not thread_id:
            thread = await create_user_thread(client)
            print(f"Thread created : {thread}")
        if with_thread and thread_id:
            thread = await get_user_thread(client, thread_id)
            print(f"Thread loaded : {thread_id}")
        if not with_thread:
            thread = None
            print(f"No thread used")

        answer = await query_assistant(client, thread, assistant_id, question, context)
        print(f"SUCCESS ! Response : {answer}")

        return thread
    
    except httpx.HTTPStatusError as e:
        print(f"Forbidden access (HTTP {e.response.status_code}) : {e.response.text}")
    except Exception as e:
        print(f"Error ({type(e).__name__}) : {e}")

# ============================================================
# 10. Main test procedure
# ============================================================
async def main():
    tokens = load_tokens(TOKEN_FILE)
    list_assistants = await create_assistant(tokens=tokens, 
                     langgraph_url=LANGGRAPH_URL, 
                     graph_id=GRAPH_ID)

    user_clients = {}
    for name in tokens:
        user_clients[name] = create_authenticated_client(LANGGRAPH_URL, tokens[name])

    # ========================================================
    # TEST 1: Alice accesses her own assistant
    # ========================================================
    # Alice creates a new thread and executes her assistant.
    #
    # Expected result:
    # Access should be allowed.
    thread_id = await run_access_check(client=user_clients["alice_user"], 
                                       assistant_id=list_assistants["alice_user"], 
                                       label="User Alice -> Assistant Alice, new thread",
                                       with_thread=True)

    # ========================================================
    # TEST 2: Alice reuses her own thread
    # ========================================================

    # Alice executes her assistant using the thread
    # created during the previous test.
    #
    # Expected result:
    # Access should be allowed because Alice owns the thread.  
    await run_access_check(client=user_clients["alice_user"], 
                                       assistant_id=list_assistants["alice_user"], 
                                       label="User Alice -> Assistant Alice, Alice thread",
                                       with_thread=True,
                                       thread_id=thread_id) 


    # ========================================================
    # TEST 3: Claude try to access Alice's assistant
    # ========================================================

    # Claude attempts to access an assistant created by Alice.
    #
    # Expected result:
    # Access should be denied by the ownership filter.
    thread_id_claude = await create_user_thread(client=user_clients["claude_user"])
    await run_access_check(client=user_clients["claude_user"], 
                                assistant_id=list_assistants["alice_user"], 
                                label="User Claude -> Assistant Alice, Claude thread",
                                with_thread=True,
                                thread_id=thread_id_claude)

    # ========================================================
    # TEST 4: Claude attempts to access Alice's assistant 
    # with Alice's thread
    # ========================================================

    # Claude attempts to retrieve and execute a thread/assistant
    # that was created by Alice.
    #
    # The thread/assistant belongs to Alice, so Claude should not 
    # be allowed to access it.
    #
    # Expected result:
    # Access should be denied by the thread ownership filter.
    await run_access_check(client=user_clients["claude_user"],
                           assistant_id= list_assistants["alice_user"], 
                           label="User Claude -> Assistant Alice, Alice thread",
                           with_thread=True,
                           thread_id=thread_id)
    
    # ========================================================
    # TEST 5: Claude attempts to execute Alice's assistant
    # without using a thread
    # ========================================================

    # Claude attempts to execute Alice's assistant
    # without providing an existing thread.
    #
    # This test checks whether assistant execution is allowed
    # independently of thread ownership.
    #
    # Since no thread is used, the thread ownership filter
    # does not apply.
    #
    # Expected result:
    # The execution should be allowed if Claude has the
    # required permissions to run the assistant.
    await run_access_check(client=user_clients["claude_user"],
                        assistant_id=list_assistants["alice_user"], 
                        label="User Claude -> Assistant Alice, new thread",
                        with_thread=False)

   # ========================================================
    # TEST 6: Administrator accesses Alice's thread/assistant
    # =======================================================

    # Bob is an administrator.
    #
    # He attempts to access and execute a thread/assistant
    # created by Alice.
    #
    # Administrators are allowed to access resources
    # regardless of their ownership.
    #
    # Expected result:
    # Access should be allowed.
    await run_access_check(client=user_clients["bob_admin"],
                           assistant_id= list_assistants["alice_user"], 
                           label="User admin -> Assistant Alice, Alice thread",
                           with_thread=True,
                           thread_id=thread_id)

 # ========================================================
    # TEST 7: Administrator executes Alice's assistant
    # without using a thread
    # ========================================================

    # Bob attempts to execute Alice's assistant
    # without using an existing thread.
    #
    # This test verifies that an administrator can perform
    # a stateless execution.
    #
    # Expected result:
    # Access should be allowed.   
    await run_access_check(client=user_clients["bob_admin"],
                        assistant_id= list_assistants["alice_user"], 
                        label="User admin -> Assistant Alice, new thread",
                        with_thread=False)


    # ========================================================
    # TEST 8: Reject unexpected context attributes
    # ========================================================

    # Bob attempts to provide an additional context attribute
    # that is not defined in the AssistantConfig schema.
    #
    # The schema uses extra="forbid", which means that
    # unexpected fields must be rejected.
    #
    # Expected result:
    # Configuration validation should fail.
    await run_access_check(client=user_clients["bob_admin"],
                        assistant_id= list_assistants["alice_user"], 
                        label="Add custom attribute in context",
                        question="Say Hello",
                        with_thread=True,
                        context={"test": True})

    # ========================================================
    # TEST 9: Administrator modifies Alice's system prompt
    # ========================================================

    # Bob attempts to override the system prompt
    # of Alice's assistant.
    #
    # Administrators are allowed to modify the system prompt
    # according to the authorization rules.
    #
    # Expected result:
    # The request should be allowed.
    await run_access_check(client=user_clients["bob_admin"],
                        assistant_id= list_assistants["alice_user"], 
                        label="Modify system prompt by admin",
                        with_thread=True,
                        context={"system_prompt": "For each response, you MUST start by 'ADMIN CONTEXT: '"})

    # ========================================================
    # TEST 10: Regular user modifies the system prompt
    # ========================================================

    # Claude attempts to override the system prompt.
    #
    # Expected result:
    # The request should be denied because Claude
    # does not have the administrator role.
    await run_access_check(client=user_clients["claude_user"],
                        assistant_id= list_assistants["claude_user"], 
                        label="Modify system prompt by user",
                        with_thread=True,
                        context={"system_prompt": "For each response, you MUST start by 'USER CONTEXT: '"})

    # ========================================================
    # TEST 11: Regular user provides additional user context
    # ========================================================

    # Claude provides additional context through user_context.
    #
    # Expected result:
    # The request should be allowed if user_context
    # is permitted by the context validation rules.
    await run_access_check(client=user_clients["claude_user"],
                        assistant_id= list_assistants["claude_user"], 
                        label="Modify user prompt by user",
                        with_thread=True,
                        context={"user_context": "For each response, you MUST start by 'USER CONTEXT: '"})

    # ========================================================
    # TEST 12: Administrator accesses sensitive tools
    # ========================================================

    # Ask the administrator to retrieve information
    # about the AGENT enterprise.
    #
    # The administrator should have access to both:
    # - public_tool
    # - admin_tool         
    await run_access_check(client=user_clients["bob_admin"],
                    assistant_id= list_assistants["alice_user"], 
                    label="User admin -> Check tools limitation",
                    question="Give me all information concerning AGENT enterprise. Keep reasonning short and concise. You can run multiples tools in one call. Response with 15 words max",
                    with_thread=True)

    # ========================================================
    # TEST 13: Regular user accesses public tools only
    # ========================================================

    # Ask Alice to retrieve information about the enterprise.
    #
    # Alice should only have access to public_tool.
    #
    # The admin_tool should not be available to her agent.   
    await run_access_check(client=user_clients["alice_user"],
                    assistant_id= list_assistants["alice_user"], 
                    label="User Alice -> Check tools limitation",
                    question="Give me all information concerning AGENT enterprise. Keep reasonning short and concise. You can run multiples tools in one call. Response with 15 words max",
                    with_thread=True)
    
if __name__ == "__main__":
    asyncio.run(main())