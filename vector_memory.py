# vector_memory.py

import chromadb

from sentence_transformers import (
    SentenceTransformer
)


class VectorMemory:

    def __init__(self):

        self.client = chromadb.Client()

        self.collection = self.client.create_collection(
            name="memory"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    # save memory
    def save_memory(
        self,
        text,
        memory_id
    ):

        embedding = self.embedding_model.encode(
            text
        ).tolist()

        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[memory_id]
        )

    # search memory
    def search_memory(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results["documents"]