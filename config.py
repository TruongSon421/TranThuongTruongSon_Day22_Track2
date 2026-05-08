"""
Shared configuration module for Day 22 Lab.

Loads environment variables from .env and provides helper functions
for creating LLM instances and verifying configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
_dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_dotenv_path)

# Export configuration constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "day22-langsmith-lab")
LANGSMITH_TRACING_V2 = os.getenv("LANGSMITH_TRACING_V2", "true")


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.0, **kwargs):
    """
    Create and return a configured ChatOpenAI instance.

    Args:
        model: The model name to use (default: gpt-4o-mini)
        temperature: Sampling temperature (default: 0.0 for deterministic)
        **kwargs: Additional arguments passed to ChatOpenAI

    Returns:
        ChatOpenAI: Configured LLM instance
    """
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        temperature=temperature,
        **kwargs,
    )


def get_embeddings(model: str = "text-embedding-3-small", **kwargs):
    """
    Create and return a configured OpenAIEmbeddings instance.

    Args:
        model: The embedding model name (default: text-embedding-3-small)
        **kwargs: Additional arguments passed to OpenAIEmbeddings

    Returns:
        OpenAIEmbeddings: Configured embeddings instance
    """
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=model,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        **kwargs,
    )


def verify_config() -> bool:
    """
    Verify that all required configuration values are present.

    Prints config values (with API keys masked) and returns True
    if all required values are set, False otherwise.
    """
    import os

    print("=" * 60)
    print("  Configuration Check")
    print("=" * 60)

    configs = [
        ("LangSmith project", LANGSMITH_PROJECT),
        ("OpenAI endpoint", OPENAI_BASE_URL),
    ]

    all_ok = True
    for name, value in configs:
        if value:
            print(f"  {name:25s}: {value}")
        else:
            print(f"  {name:25s}: NOT SET")
            all_ok = False

    # Mask API keys for display
    if OPENAI_API_KEY:
        masked_key = OPENAI_API_KEY[:8] + "..." + OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 12 else "***"
        print(f"  {'OpenAI API key':25s}: {masked_key}")
    else:
        print(f"  {'OpenAI API key':25s}: NOT SET")
        all_ok = False

    if LANGSMITH_API_KEY:
        masked_key = LANGSMITH_API_KEY[:8] + "..." + LANGSMITH_API_KEY[-4:] if len(LANGSMITH_API_KEY) > 12 else "***"
        print(f"  {'LangSmith API key':25s}: {masked_key}")
    else:
        print(f"  {'LangSmith API key':25s}: NOT SET")
        all_ok = False

    print("-" * 60)
    if all_ok:
        print("  Config loaded successfully!")
    else:
        print("  WARNING: Some configuration values are missing!")
        print("  Please check your .env file.")

    return all_ok


if __name__ == "__main__":
    verify_config()
