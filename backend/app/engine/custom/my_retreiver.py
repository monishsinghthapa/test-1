#Multithreading
from concurrent.futures import ThreadPoolExecutor

# import QueryBundle
from llama_index.core import QueryBundle

# import NodeWithScore
from llama_index.core.schema import NodeWithScore

# Retrievers
from llama_index.core.retrievers import BaseRetriever,VectorIndexRetriever
from llama_index.core.postprocessor import SentenceTransformerRerank,MetadataReplacementPostProcessor,SimilarityPostprocessor, LongContextReorder

import time
from typing import List
class CustomRetrieverAndReranker(BaseRetriever):
    """Custom retriever that performs aysnc\sync retreive from multiple retreivers."""

    def __init__(
        self,
        vector_retriever_ls: List[VectorIndexRetriever],                
        rerank_top_k=5,
    ) -> None:
        """Init params."""

        self._vector_retriever_ls = vector_retriever_ls
        # self._rerank = SentenceTransformerRerank(    model="cross-encoder/ms-marco-TinyBert-L-2-v2", top_n=rerank_top_k) 
        # self._rerank = SentenceTransformerRerank(    model="BAAI/bge-reranker-base", top_n=rerank_top_k)        
        # self._rerank = SentenceTransformerRerank(    model="colbert-ir/colbertv2.0", top_n=rerank_top_k)        

        self._rerank = LongContextReorder(top_n = rerank_top_k)
        super().__init__()

    def _aretriever(args:tuple):
        retriever, query_bundle=args
        return retriever.retrieve(query_bundle)
    
    
    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query."""
        retrieved_nodes = []
        start_time = time.perf_counter()
        for retreiver in self._vector_retriever_ls:             
             retrieved_nodes.extend(retreiver.retrieve(query_bundle))
        end_time = time.perf_counter()
        time_taken = end_time-start_time
        print("Retrieval Time", time_taken)

        start_time = time.perf_counter()
        processor = SimilarityPostprocessor(similarity_cutoff=0.4)
        filtered_nodes = processor.postprocess_nodes(retrieved_nodes)
        end_time = time.perf_counter()
        time_taken = end_time-start_time
        print("Similarity post process Time", time_taken)

        start_time = time.perf_counter()
        reranked_nodes = self._rerank.postprocess_nodes(nodes=filtered_nodes,query_bundle=query_bundle)
        reranked_nodes = reranked_nodes[:5]
        processed_nodes = MetadataReplacementPostProcessor(target_metadata_key="window").postprocess_nodes(nodes=reranked_nodes)
        end_time = time.perf_counter()
        time_taken = end_time-start_time
        print("Reranker Time", time_taken)
        return processed_nodes