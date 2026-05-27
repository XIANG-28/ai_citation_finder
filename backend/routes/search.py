from fastapi import APIRouter
from itertools import combinations

from backend.services.pubmed import search_pubmed, fetch_details
from backend.services.parser import extract_articles
from backend.services.matcher import find_best_sentence
from backend.services.query_expander import expand_query
from backend.services.embedding import get_embedding, cosine

router = APIRouter()


def generate_keyword_combinations(keywords, min_k=3):
    n = len(keywords)

    if n < min_k:
        return [(n, keywords)]

    combos = []

    for k in range(n, min_k - 1, -1):
        for combo in combinations(keywords, k):
            combos.append((k, list(combo)))

    return combos


@router.post("/search")
def search(query: str):
    # Step 1️⃣：Query expansion
    keywords = expand_query(query)

    all_results = []
    seen_ids = set()

    combos = generate_keyword_combinations(keywords)

    # Step 2️⃣：PubMed recall
    for k, combo in combos:
        ids = search_pubmed(combo)

        if not ids:
            continue

        for pmid in ids:
            if pmid not in seen_ids:
                seen_ids.add(pmid)
                all_results.append({
                    "pmid": pmid,
                    "keyword_score": k
                })

    if not all_results:
        return []

    # Step 3️⃣：关键词强度排序
    all_results.sort(key=lambda x: x["keyword_score"], reverse=True)

    # 控制数量（非常关键）
    sorted_ids = [item["pmid"] for item in all_results][:20]

    # Step 4️⃣：获取文章详情
    xml_data = fetch_details(sorted_ids)
    articles = extract_articles(xml_data)

    # Step 5️⃣：embedding（只算一次）
    query_emb = get_embedding(query)

    results = []

    for art in articles:
        abstract = art.get("abstract", "")

        if not abstract:
            continue

        # 👉 句子级匹配（解释性）
        best_sentence, sentence_score = find_best_sentence(query_emb, abstract)

        # 👉 文档级匹配
        doc_emb = get_embedding(abstract[:1000])
        doc_score = cosine(query_emb, doc_emb)

        # 👉 综合评分（可以调参）
        final_score = 0.7 * doc_score + 0.3 * sentence_score

        results.append({
            "title": art.get("title", ""),
            "link": art.get("link", ""),
            "matched_sentence": best_sentence,
            "score": float(final_score),

            # ✅ 产品级解释字段（很重要）
            "explain": {
                "doc_score": float(doc_score),
                "sentence_score": float(sentence_score)
            }
        })

    # Step 6️⃣：最终排序
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


#
# from fastapi import APIRouter
# from itertools import combinations
#
# from backend.services.pubmed import search_pubmed, fetch_details
# from backend.services.parser import extract_articles
# from backend.services.matcher import find_best_sentence
# from backend.services.query_expander import expand_query
#
# router = APIRouter()
#
#
# def generate_keyword_combinations(keywords, min_k=3):
#     n = len(keywords)
#
#     # 如果关键词本来就少
#     if n < min_k:
#         return [(n, keywords)]
#
#     combos = []
#
#     for k in range(n, min_k - 1, -1):
#         for combo in combinations(keywords, k):
#             combos.append((k, list(combo)))
#
#     return combos
#
#
# @router.post("/search")
# def search(query: str):
#     keywords = expand_query(query)
#
#     all_results = []
#     seen_ids = set()
#
#     combos = generate_keyword_combinations(keywords)
#
#     for k, combo in combos:
#
#         ids = search_pubmed(combo)
#
#         if not ids:
#             continue
#
#         for pmid in ids:
#             if pmid not in seen_ids:
#                 seen_ids.add(pmid)
#
#                 all_results.append({
#                     "pmid": pmid,
#                     "keyword_score": k
#                     # "score": k  # 关键词数量 = 相关性
#                 })
#
#     if not all_results:
#         return []
#
#     # ✅ 排序（关键词多的在前）
#     all_results.sort(key=lambda x: x["score"], reverse=True)
#
#     # 取前20篇
#     sorted_ids = [item["pmid"] for item in all_results][:20]
#
#     xml_data = fetch_details(sorted_ids)
#     articles = extract_articles(xml_data)
#
#
#
#     results = []
#     for art in articles:
#         best_sentence = find_best_sentence(query, art["abstract"])
#
#         results.append({
#             "title": art["title"],
#             "link": art["link"],
#             "matched_sentence": best_sentence
#         })
#
#     return results