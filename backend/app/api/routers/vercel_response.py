import json
import logging
from typing import Any
from fastapi.responses import StreamingResponse
logger = logging.getLogger("uvicorn")

class VercelStreamResponse(StreamingResponse):
    """
    Class to convert the response from the chat engine to the streaming format expected by Vercel
    """

    TEXT_PREFIX = "0:"
    DATA_PREFIX = "8:"

    @classmethod
    def convert_text(cls, token: str):
        # Escape newlines and double quotes to avoid breaking the stream
        token = json.dumps(token)
        # logger.info(f"streaming token {token}")
        return f"{cls.TEXT_PREFIX}{token}\n"

    @classmethod
    def convert_data(cls, data: dict):
        data_str = json.dumps(data)
        logger.info("streaming source nodes")
        return f"{cls.DATA_PREFIX}[{data_str}]\n"

    def __init__(self, content: Any, **kwargs):
        super().__init__(
            content=content,
            **kwargs,
        )
