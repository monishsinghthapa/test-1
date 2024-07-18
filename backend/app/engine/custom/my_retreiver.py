#Multithreading
from concurrent.futures import ThreadPoolExecutor

# import QueryBundle
from llama_index.core import QueryBundle

# import NodeWithScore
from llama_index.core.schema import NodeWithScore

# Retrievers
from llama_index.core.retrievers import BaseRetriever,VectorIndexRetriever
from llama_index.core.postprocessor import SentenceTransformerRerank,MetadataReplacementPostProcessor,SimilarityPostprocessor


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
        self._rerank = SentenceTransformerRerank(    model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=rerank_top_k)        
        super().__init__()

    def _aretriever(args:tuple):
        retriever, query_bundle=args
        return retriever.retrieve(query_bundle)
    
    
    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query."""
        retrieved_nodes = []
        for retreiver in self._vector_retriever_ls:             
             retrieved_nodes.extend(retreiver.retrieve(query_bundle))
            
        processor = SimilarityPostprocessor(similarity_cutoff=0.4)
        filtered_nodes = processor.postprocess_nodes(retrieved_nodes)
        reranked_nodes = self._rerank.postprocess_nodes(nodes=filtered_nodes,query_bundle=query_bundle)
        processed_nodes = MetadataReplacementPostProcessor(target_metadata_key="window").postprocess_nodes(nodes=reranked_nodes)
        
        return processed_nodes