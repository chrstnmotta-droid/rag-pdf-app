# 4 sentences -> Embed -> Compute cosine similarity

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

s1_pair1 = "I like sports very much"
s2_pair1 = "I love football, tennis, and every other sport"
s1_pair2 = "I am going to the beach"
s2_pair2 = "I work 5 times a week"

model = SentenceTransformer("all-MiniLM-L6-v2")

def similarity(s1, s2):
    vector1 = model.encode(s1)
    vector2 = model.encode(s2)

    sim_score = cosine_similarity(
        np.array(vector1).reshape(1, -1),
        np.array(vector2).reshape(1, -1))[0][0]
    return sim_score

print(f"Cosine similarity for pair 1 is {similarity(s1_pair1, s2_pair1)}")
print(f"Cosine similarity for pair 2 is {similarity(s1_pair2, s2_pair2)}")
