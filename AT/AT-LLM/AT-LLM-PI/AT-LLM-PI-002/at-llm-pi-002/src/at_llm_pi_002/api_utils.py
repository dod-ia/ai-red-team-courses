from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import get_google_credentials,build_gmail_service
from langfuse.langchain import CallbackHandler
from langfuse import get_client
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


def init_langfuse(): 
    langfuse_client = get_client()
    langfuse_handler = CallbackHandler()
    return langfuse_client, langfuse_handler

def init_gmail_tools(base_dir: str):
    credentials = get_google_credentials(
        token_file=Path(base_dir) / "token.json",
        client_secrets_file=Path(base_dir) / "credentials.json",
        scopes=["https://mail.google.com/"],
    )
    api_resource = build_gmail_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    return toolkit
