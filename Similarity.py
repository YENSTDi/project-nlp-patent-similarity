from sklearn.metrics.pairwise import cosine_similarity

class Similarity():
    def __init__(self) -> None:
        pass

    def cosine(self, emb1, emb2):
        similar = cosine_similarity(emb1, emb2)
        return similar[0][0]

    # def cala_top1_similarity(self):
        