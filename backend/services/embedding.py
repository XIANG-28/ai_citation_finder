from openai import OpenAI
import numpy as np

client = OpenAI()


def get_embedding(text):
    if not text:
        return None

    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return np.array(res.data[0].embedding)


def cosine(a, b):
    if a is None or b is None:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# def get_embedding(text):
#     res = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return np.array(res.data[0].embedding)
#
#
# def cosine(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))