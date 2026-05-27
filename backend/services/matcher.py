from backend.services.embedding import cosine
import re
import numpy as np


def split_sentences(text):
    if not text:
        return []

    sentences = re.split(r'(?<=[.!?])\s+', text)

    # 控制数量（防止 embedding 爆炸）
    return [s.strip() for s in sentences if len(s.strip()) > 20][:10]


def get_embeddings_batch(text_list):
    from openai import OpenAI
    client = OpenAI()

    if not text_list:
        return []

    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_list
    )

    # ✅ 统一 numpy（非常关键）
    return [np.array(item.embedding) for item in res.data]


def find_best_sentence(query_emb, abstract):
    """
    输入：
        query_emb: 已经算好的 query embedding（避免重复计算）
        abstract: 文章摘要

    输出：
        (best_sentence, score)
    """
    if not abstract:
        return "", 0.0

    sentences = split_sentences(abstract)

    if not sentences:
        return "", 0.0

    sentence_embs = get_embeddings_batch(sentences)

    best_score = -1
    best_sentence = ""

    for s, emb in zip(sentences, sentence_embs):
        score = cosine(query_emb, emb)

        if score > best_score:
            best_score = score
            best_sentence = s

    return best_sentence, float(best_score)


# from openai import OpenAI
# import re
#
# client = OpenAI()
# def split_sentences(text):
#     if not text:
#         return []
#
#     # 简单英文句子切分
#     sentences = re.split(r'(?<=[.!?])\s+', text)
#     return [s.strip() for s in sentences if len(s.strip()) > 20]
#
# def find_best_sentence(query, abstract):
#     if not abstract:
#         return ""
#
#     sentences = split_sentences(abstract)
#
#     if not sentences:
#         return ""
#
#     prompt = f"""
# You are a biomedical assistant.
#
# Task:
# Choose the MOST relevant sentence to the query.
#
# Rules:
# - Return ONLY one sentence
# - Do NOT modify the sentence
# - Do NOT add explanation
#
# Query:
# {query}
#
# Sentences:
# {chr(10).join(sentences)}
#
# Return the most relevant single sentence from the abstract.
# """
#
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "Extract the most relevant sentence from scientific text."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0
#     )
#
#     result = response.choices[0].message.content.strip()
#
#     # fallback保护
#     if not result or len(result) < 10:
#         return sentences[0] if sentences else ""
#
#     return result