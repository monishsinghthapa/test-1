import logging
from pydantic import BaseModel
from typing import List, Any, Optional, Dict, Tuple
from fastapi import APIRouter, Depends, HTTPException, Request, status
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.schema import NodeWithScore
from llama_index.core.llms import ChatMessage, MessageRole
from app.engine import get_chat_engine
from app.api.routers.vercel_response import VercelStreamResponse
from app.api.routers.messaging import EventCallbackHandler
from aiostream import stream
logger = logging.getLogger("uvicorn")
chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "What standards for letters exist?",
                    }
                ]
            }
        }


class _SourceNodes(BaseModel):
    id: str
    metadata: Dict[str, Any]
    score: Optional[float]
    text: str

    @classmethod
    def from_source_node(cls, source_node: NodeWithScore):
        return cls(
            id=source_node.node.node_id,
            metadata=source_node.node.metadata,
            score=source_node.score,
            text=source_node.node.text,  # type: ignore
        )

    @classmethod
    def from_source_nodes(cls, source_nodes: List[NodeWithScore]):
        return [cls.from_source_node(node) for node in source_nodes]


class _Result(BaseModel):
    result: _Message
    nodes: List[_SourceNodes]


async def parse_chat_data(data: _ChatData) -> Tuple[str, List[ChatMessage]]:
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    last_message = data.messages.pop()
    if last_message.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]
    prompt_example = ''' 
    Example: The effective tax rate was 8.4% 
    driven by the recognition of a net discrete
    tax benefit of $147 million in the first 
     quarter of fiscal 2024 related to the repatriation 
     of certain intellectual property between 
     wholly-owned legal entities that were
    based in different tax jurisdictions. (Source: MCK-Q1-FY24-ECT.pdf, Page Number: 10)
    '''
    # prompt = last_message.content+" Answer as briefly and as concisely as possible"
    # prompt = prompt + ". You must return the name of the Source file and the page number for each information in the response. This information must be presented elegantly in the markdown format.\n" + prompt_example
    # print(prompt)
    # prompt=last_message.content + ". You must return the name of the Source file and the page number for each information in the response. This information must be presented elegantly in the markdown format.\n" + prompt_example

    prompt = last_message.content+"Provide details for each company seperately in points. \n"
    prompt = prompt + ". You must return the name of the Source file and the page number for each information in the response. This information must be presented elegantly in the markdown format.\n" + prompt_example
    return prompt, messages


# streaming endpoint - delete if not needed
@r.post("")
async def chat(
    request: Request,
    data: _ChatData,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    last_message_content, messages = await parse_chat_data(data)

    event_handler = EventCallbackHandler()
    chat_engine = get_chat_engine(last_message_content)

    chat_engine.callback_manager.handlers.append(event_handler)  # type: ignore
    response = await chat_engine.astream_chat(last_message_content, messages)
    print(response)
    
    async def content_generator():
        # Yield the text response
        async def _text_generator():
            responseStr = ""
            async for token in response.async_response_gen():
                responseStr += token
                yield VercelStreamResponse.convert_text(token)
            # the text_generator is the leading stream, once it's finished, also finish the event stream
            event_handler.is_done = True
            print(responseStr)
        # Yield the events from the event handler
        async def _event_generator():
            async for event in event_handler.async_event_gen():
                event_response = event.to_response()
                if event_response is not None:
                    yield VercelStreamResponse.convert_data(event_response)

        combine = stream.merge(_text_generator(), _event_generator())
        async with combine.stream() as streamer:
            async for item in streamer:
                if await request.is_disconnected():
                    break
                yield item

        # Yield the source nodes
        yield VercelStreamResponse.convert_data(
            {
                "type": "sources",
                "data": {
                    "nodes": [
                        _SourceNodes.from_source_node(node).dict()
                        for node in response.source_nodes
                    ]
                },
            }
        )

    return VercelStreamResponse(content=content_generator())


# non-streaming endpoint - delete if not needed
@r.post("/request")
async def chat_request(
    data: _ChatData,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
) -> _Result:
    last_message_content, messages = await parse_chat_data(data)

    response = await chat_engine.achat(last_message_content, messages)
    print(response)
    return _Result(
        result=_Message(role=MessageRole.ASSISTANT, content=response.response),
        nodes=_SourceNodes.from_source_nodes(response.source_nodes),
    )
