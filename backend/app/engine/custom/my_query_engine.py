from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer


class RAGQueryEngine(CustomQueryEngine):
    """RAG Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)        
        prompt_helper=""
        return self.response_synthesizer.synthesize(query_str, nodes,streaming=True,prompt_helper=prompt_helper)


# class RAGQueryEngineString(CustomQueryEngine):
#     """RAG String Query Engine."""

#     retriever: BaseRetriever
#     # response_synthesizer: BaseSynthesizer
#     llm: AzureOpenAI
#     qa_prompt: PromptTemplate

#     def custom_query(self, query_str: str):
#         nodes = self.retriever.retrieve(query_str)

#         context_str = "\n\n".join([n.node.get_content() for n in nodes])
#         response = self.llm.complete(
#             qa_prompt.format(context_str=context_str, query_str=query_str)
#         )

#         return str(response)

