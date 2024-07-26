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
import time
from app.engine.FilterFileList import getSourceDict, filterFileList

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
        # ChatMessage(
        #     role=m.role,
        #     content=m.content,
        # )
        # for m in data.messages
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
    # An example of the format of the answer is given below:
    # prompt_example = '''
    # Respond according to the format given below:
    # \n\t\t  ###Answer Summary:\\\n
    # \n\t\t  <p>The drivers provided for the US Pharmaceutical outlook on the Q4 FY22 earnings call included the efficiency and durability of the core distribution platform, the continued expansion of the oncology ecosystem, anticipated revenue increases, and a range of operating profit outcomes. These were influenced by factors such as COVID-19 vaccine distribution for the US government.(Source: MCK-Q4-FY22-ECT.pdf, Page Number: 10)<\p>.\\\n
    # \n\t\t  ####Facts supporting the answer:\\\n
    # \n\t\t  - **Q1 of FY21**: Anticipated discrete tax items expected to be realized during the year, with a specific mention of a favorable tax discrete item anticipated to be recorded in the fiscal second quarter.\\\n
    # \n\t\t  - **Q1 of FY23**: A tax receivable gain related to McKesson's previous change healthcare investment.\\\n
    # '''
    # prompt = last_message.content+" Answer as briefly and as concisely as possible"
    # prompt = prompt + ". You must return the name of the Source file and the page number for each information in the response. This information must be presented elegantly in the markdown format.\n" + prompt_example
    # print(prompt)
    # prompt=last_message.content + ". You must return the name of the Source file and the page number for each information in the response. This information must be presented elegantly in the markdown format.\n" + prompt_example

    # prompt = last_message.content+"Provide details for each company seperately in points. \n"
    prompt = last_message.content
    filteringQuery = last_message.content + "  "
    prompt = prompt + ". You must return the name of the Source file and the page number for each information in the response in the format (Source: MCK-Q1-FY24-ECT.pdf, Page Number: 10). This information must be presented elegantly in the markdown format.\n" + prompt_example
    return prompt, messages, filteringQuery


# streaming endpoint - delete if not needed
@r.post("")
async def chat(
    request: Request,
    data: _ChatData,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    last_message_content, messages,filteringQuery = await parse_chat_data(data)

    event_handler = EventCallbackHandler()
    chat_engine = get_chat_engine(filteringQuery)

    q,y,company = filterFileList(filteringQuery)
    company = list(set(company))
    multi_company = False
    print(company,len(company))
    if len(company) > 1:
        multi_company = True
    

    chat_engine.callback_manager.handlers.append(event_handler)  # type: ignore
    response = await chat_engine.astream_chat(last_message_content, messages)
    print(response)

    responseStr = ""
    response_gen_obj = response.async_response_gen()
    async for token in response_gen_obj:
        responseStr += token
    sourceDict = getSourceDict(responseStr)
    print(responseStr)
            # customString = "abcde MCK-Q3-FY20-ECT.pdf"
    nodeListToPresent = []
    for sourceFile in sourceDict:
        for page in sourceDict[sourceFile]:
            for node in response.source_nodes:
                print(node.metadata["file_name"])
                print(node.metadata["page_label"])
                if(str(node.metadata["file_name"])==sourceFile and int(node.metadata["page_label"])==page):
                    # if(node not in nodeListToPresent):
                    if len(nodeListToPresent) == 0:
                        nodeListToPresent.append(node)
                    else:
                        for node2 in nodeListToPresent:
                            if str(node2.metadata["file_name"]) == sourceFile and int(node2.metadata["page_label"])==page:
                                break
                        else: 
                            nodeListToPresent.append(node)
    # print(nodeListToPresent)
    # print(len(nodeListToPresent))
    # print(sourceDict)
    async def content_generator():
        # Yield the text response
        
        async def _text_generator():
            # responseStr = ""
            # async for token in responseStr:
                # responseStr += token
            yield VercelStreamResponse.convert_text(responseStr)
                # time.sleep(0.1)
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
                        for node in nodeListToPresent
                    ]
                },
                "multiple_companies": multi_company
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
