# import faiss
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
class Company():
    def __init__(self, embedding, apple_embedding) -> None:
        self.embedding = embedding
        self.apple_embedding = apple_embedding
        self.cosine_similar = cosine_similarity(embedding, apple_embedding)
        self.top_similar_index = np.argmax(self.cosine_similar, axis=1)
        self.top_similar = [self.cosine_similar[index][max_index] for index, max_index in enumerate(np.argmax(self.cosine_similar, axis=1))]
        self.top_similar = np.array(self.top_similar)
        self.avg_similar = sum(self.top_similar) / len(self.top_similar)
