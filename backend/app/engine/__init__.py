import os
from llama_index.core import get_response_synthesizer
from app.engine.index import get_index
from app.engine.constants import URL_DICT
from app.engine.custom.my_query_engine import RAGQueryEngine
from app.engine.custom.my_retreiver import CustomRetrieverAndReranker
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.settings import Settings
def get_chat_engine():
    system_prompt = os.getenv("SYSTEM_PROMPT")
    # top_k = os.getenv("TOP_K", "3")
    # tools = []

    # # Add query tool if index exists
    # index = get_index()
    # if index is not None:
    #     query_engine = index.as_query_engine(similarity_top_k=int(top_k))
    #     query_engine_tool = QueryEngineTool.from_defaults(query_engine=query_engine)
    #     tools.append(query_engine_tool)

    # # Add additional tools
    # tools += ToolFactory.from_env()

    # return AgentRunner.from_llm(
    #     llm=Settings.llm,
    #     tools=tools,
    #     system_prompt=system_prompt,
    #     verbose=True,
    # )
    retreiver_ls = []
    for file in URL_DICT.keys():        
        index = get_index(file)
        retriever = index.as_retriever(similarity_top_k=5)
        retreiver_ls.append(retriever)
    # synthesizer = get_response_synthesizer(response_mode="compact")
    top_k = os.getenv("TOP_K", "10")
    retreiver = CustomRetrieverAndReranker(retreiver_ls,rerank_top_k=top_k)
    # ragQueryEngine = RAGQueryEngine(        retriever=retreiver, response_synthesizer=synthesizer    )
    print("Retriever:",type(retreiver),retriever)
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    context_prompt=(        
        "Here are the relevant documents for the context:\n"
        "{context_str}"
        "\nInstructions: "
        "\n\t1. Use the previous chat history, or the context above, to interact and help the user."
        "\n\t2. Generate the answer in Markdown format only."
        "\n\t3. An example of the answer is given below:"
        "\n\t\t  ###Answer Summary:\\\n"
        "\n\t\t  <p>The drivers provided for the US Pharmaceutical outlook on the Q4 FY22 earnings call included the efficiency and durability of the core distribution platform, the continued expansion of the oncology ecosystem, anticipated revenue increases, and a range of operating profit outcomes. These were influenced by factors such as COVID-19 vaccine distribution for the US government.<\p>.\\\n"
        "\n\t\t  ####Facts supporting the answer:\\\n"
        "\n\t\t  - **Q1 of FY21**: Anticipated discrete tax items expected to be realized during the year, with a specific mention of a favorable tax discrete item anticipated to be recorded in the fiscal second quarter.\\\n"
        "\n\t\t  - **Q1 of FY23**: A tax receivable gain related to McKesson's previous change healthcare investment.\\\n")
    
    return CondensePlusContextChatEngine(memory=memory,
                                         retriever=retreiver,
                                         llm=Settings.llm,
                                         system_prompt=system_prompt,
                                         context_prompt=context_prompt
                                        )
    


