from langfuse.langchain import CallbackHandler
from langfuse import get_client
from dotenv import load_dotenv

load_dotenv()

def init_langfuse(): 
    langfuse_client = get_client()
    langfuse_handler = CallbackHandler()
    return langfuse_client, langfuse_handler

