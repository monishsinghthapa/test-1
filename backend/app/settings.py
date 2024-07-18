import os
from typing import Dict
from llama_index.core.settings import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def init_settings():
    model_provider = os.getenv("MODEL_PROVIDER")
    if model_provider == "openai":
        init_openai()
    # elif model_provider == "ollama":
    #     init_ollama()
    # elif model_provider == "anthropic":
    #     init_anthropic()
    # elif model_provider == "gemini":
    #     init_gemini()
    else:
        raise ValueError(f"Invalid model provider: {model_provider}")
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "256"))


# def init_ollama():
#     from llama_index.llms.ollama import Ollama
#     from llama_index.embeddings.ollama import OllamaEmbedding

#     Settings.embed_model = OllamaEmbedding(model_name=os.getenv("EMBEDDING_MODEL"))
#     Settings.llm = Ollama(model=os.getenv("MODEL"))


def init_openai():
    from llama_index.llms.azure_openai import AzureOpenAI 
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from app.engine.constants import MODEL_MAP, LLM_MAX_TOKENS
    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {        
        "deployment_name": os.getenv("DEPLOYMENT_NAME"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "azure_endpoint": os.getenv("OPENAI_API_BASE"),
        "api_version" : os.getenv("OPENAI_API_VERSION"),        
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else LLM_MAX_TOKENS,
        "stream":True
    }
    Settings.llm = AzureOpenAI(   **config)    
    Settings.num_output = int(max_tokens) if max_tokens is not None else LLM_MAX_TOKENS
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=MODEL_MAP[os.getenv("EMBEDDING_MODEL")]
    )
    



# def init_anthropic():
#     from llama_index.llms.anthropic import Anthropic
#     from llama_index.embeddings.huggingface import HuggingFaceEmbedding

#     model_map: Dict[str, str] = {
#         "claude-3-opus": "claude-3-opus-20240229",
#         "claude-3-sonnet": "claude-3-sonnet-20240229",
#         "claude-3-haiku": "claude-3-haiku-20240307",
#         "claude-2.1": "claude-2.1",
#         "claude-instant-1.2": "claude-instant-1.2",
#     }

#     embed_model_map: Dict[str, str] = {
#         "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
#         "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
#     }

#     Settings.llm = Anthropic(model=model_map[os.getenv("MODEL")])
#     Settings.embed_model = HuggingFaceEmbedding(
#         model_name=embed_model_map[os.getenv("EMBEDDING_MODEL")]
#     )


# def init_gemini():
#     from llama_index.llms.gemini import Gemini
#     from llama_index.embeddings.gemini import GeminiEmbedding

#     model_map: Dict[str, str] = {
#         "gemini-1.5-pro-latest": "models/gemini-1.5-pro-latest",
#         "gemini-pro": "models/gemini-pro",
#         "gemini-pro-vision": "models/gemini-pro-vision",
#     }

#     embed_model_map: Dict[str, str] = {
#         "embedding-001": "models/embedding-001",
#         "text-embedding-004": "models/text-embedding-004",
#     }

#     Settings.llm = Gemini(model=model_map[os.getenv("MODEL")])
#     Settings.embed_model = GeminiEmbedding(
#         model_name=embed_model_map[os.getenv("EMBEDDING_MODEL")]
#     )
