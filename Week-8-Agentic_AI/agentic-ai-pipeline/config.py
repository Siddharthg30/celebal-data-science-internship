import os
from dotenv import load_dotenv

from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


def get_model_client():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        return OllamaChatCompletionClient(
            model=os.getenv("OLLAMA_MODEL", "llama3.1:latest"),
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        )

    if provider == "gemini":
        return OpenAIChatCompletionClient(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {provider}. "
        "Use 'ollama' or 'gemini'."
    )