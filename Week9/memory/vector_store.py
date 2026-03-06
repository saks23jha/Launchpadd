import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    """
    Vector Memory using FAISS

    Responsibilities:
    - Convert text into embeddings
    - Store embeddings
    - Perform similarity search
    """

    def __init__(self):

        # embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # embedding dimension
        self.dimension = 384

        # FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)

        # store original text
        self.texts = []

    #ADD Memory
    def add(self, text: str):

        embedding = self.model.encode([text])
        embedding = np.array(embedding).astype("float32")

        self.index.add(embedding)
        self.texts.append(text)


    # Search Similar Memory

    def search(self, query: str, k=3):

        if len(self.texts) == 0:
            return []

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])

        return results