from langchain_core.runnables import RunnableConfig
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, ConfigDict, ValidationError
from langchain_core.tools import tool
from langgraph_sdk.runtime import ServerRuntime
from langgraph.prebuilt import ToolRuntime
from typing import Optional

from langchain_ollama import ChatOllama
model = ChatOllama(
    model="qwen3.5:9b",
    temperature=0.0,
    num_ctx=8192,)

#model = init_chat_model("google_genai:gemma-4-26b-a4b-it", streaming=False)


# ============================================================
# 1. Define the assistant configuration schema
# ============================================================

# AssistantConfig defines the structure of the context
# that can be provided when executing the agent.
#
# Pydantic validates the input data before it is used.
class AssistantConfig(BaseModel):
    system_prompt: str # If system_prompt is None, we block the run
    user_context: Optional[str] = None
    model_config = ConfigDict(extra="forbid")

# Used by langgraph for intern work. Not used by user requests
default_agent = create_deep_agent(
    model=model,
    system_prompt="You are a helpful assistant",
    context_schema=AssistantConfig,
)

# ============================================================
# 2. Define tools
# ============================================================

# The @tool decorator exposes this function
# as a tool that the agent can call.
#
# This tool is available to all authenticated users according 
# to permissions.
#
# ToolRuntime provides access to runtime information,
# including the identity of the authenticated user.
@tool
def public_tool(runtime: ToolRuntime) -> str:
    """Public tool returning public data on AGENT enterprise"""
    server = runtime.server_info
    if server is None or server.user is None:
        raise PermissionError("Utilisateur non authentifié.")

    print(f"Access public tool by: {server.user.identity}")
    return "AGENT is an enterprise in Paris"

@tool
def admin_tool(runtime: ToolRuntime) -> str:
    """Administrator tool returning sensible data on AGENT enterprise"""

   # Retrieve information about the current server execution.
    server = runtime.server_info
    if server is None or server.user is None:
        raise PermissionError("Utilisateur non authentifié.")
    
    if "role:admin" not in server.user.permissions:
        raise PermissionError(f"Accès refusé pour {server.user.identity}")

    print(f"Access admin tool by: {server.user.identity}")
    return "AGENT is an enterprise with 10 customers"

# ============================================================
# 3. Dynamically create the agent graph
# ============================================================

# This function is responsible for creating the agent
# according to the current execution context and user permissions.
#
# It receives:
# - config: LangGraph execution configuration (thread_id, context...)
# - runtime: Server-side runtime information (auth information)
async def make_graph(config: RunnableConfig, runtime: ServerRuntime):

    # Retrieve the execution runtime.
    execution = runtime.execution_runtime


    # If there is no execution runtime,
    # return the default agent.
    #
    # This can occur when the graph is initialized
    # outside a normal execution context.
    if execution is None:
        return default_agent

    # --------------------------------------------------------
    # Validate the execution context
    # --------------------------------------------------------

    # The execution context contains the configuration
    # provided for the current agent execution.
    #
    # Validate it against the AssistantConfig schema.
    #
    # Invalid fields or missing required fields
    # will cause a ValidationError.
    try:
        validated_config = AssistantConfig.model_validate(execution.context)
    except ValidationError as e:
        raise ValueError(f"Configuration invalide : {e}") from e

   
    # --------------------------------------------------------
    # Retrieve the authenticated user
    # --------------------------------------------------------

    # Ensure that the current execution has
    # an authenticated user. 
    user = runtime.ensure_user()
    user_id = user.identity
    permissions = user.permissions


    # --------------------------------------------------------
    # Configure tools according to user permissions
    # --------------------------------------------------------

    # All authenticated users receive access
    tools = [public_tool]

    # Administrators also receive access
    # to the administrator-only tool.
    #
    # This dynamically controls which tools
    # are available to the agent.
    if "role:admin" in permissions:
        tools.append(admin_tool)

    # --------------------------------------------------------
    # Build the system prompt
    # --------------------------------------------------------

    # Start with the system prompt provided
    # in the validated configuration.
    # The default system_prompt is given at the creation of the agent
    custom_prompt = validated_config.system_prompt
    # If additional user context is provided,
    # append it to the system prompt.
    #
    # A separator is used to distinguish the
    # user-provided context from the main prompt.
    if validated_config.user_context:
        custom_prompt += (
            "\n\n--- CONTEXTE FOURNI PAR L'UTILISATEUR ---\nApply all rules\n"
            f"{validated_config.user_context}"
        )

    print(f"User: {user_id} | Permissions: {permissions} | tools: {tools} | prompt: \n")
    print(custom_prompt)

    # --------------------------------------------------------
    # Create and return the customized agent
    # --------------------------------------------------------

    # Create a new agent using the current user's configuration.
    #
    # The agent receives:
    # - The language model
    # - The tools allowed for this user
    # - The customized system prompt
    # - The context schema used for validation
    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=custom_prompt,
        context_schema=AssistantConfig,
    )