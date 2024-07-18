import logging
import os

from app.engine.constants import STORAGE_DIR
from llama_index.core.storage import StorageContext
from llama_index.core.indices import load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore

logger = logging.getLogger("uvicorn")


# def get_index():
#     # check if storage already exists
#     if not os.path.exists(STORAGE_DIR):
#         return None
#     # load the existing index
#     logger.info(f"Loading index from {STORAGE_DIR}...")
#     storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
#     index = load_index_from_storage(storage_context)
#     logger.info(f"Finished loading index from {STORAGE_DIR}")
#     return index



def get_index(index_name):
    if not os.path.exists(STORAGE_DIR):
        return None
    index = None
    vector_store = FaissVectorStore.from_persist_dir(
        f"{STORAGE_DIR}/{index_name}/"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{STORAGE_DIR}/{index_name}/", vector_store=vector_store    )
    index = load_index_from_storage(storage_context)
    logger.info(f"Finished loading index from {STORAGE_DIR}/{index_name}")
    return index
