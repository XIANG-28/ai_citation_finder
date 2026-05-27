from openai import OpenAI
import re

client = OpenAI()


def expand_query(user_input: str):
    prompt = f"""
You are a medical search assistant.

Convert the following user input into PubMed search keywords.

STRICT RULES:
- Each query must be SHORT (2-4 words)
- Use common medical terms
- Each query should represent ONE idea
- Return each query on a NEW LINE
- Do NOT include words like "keywords", "query", etc.

Input:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You convert clinical sentences into PubMed search queries."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    queries = []

    for line in text.split("\n"):
        q = line.strip()

        if not q:
            continue

        # 去掉编号 / - / *
        q = re.sub(r"^[\d\-\.\*\s]+", "", q)

        # 去掉特殊字符（保留字母数字和 -）
        q = re.sub(r"[^a-zA-Z0-9\s\-]", "", q)

        # 限制最多4个词
        words = q.split()[:4]
        q = " ".join(words)

        if q:
            queries.append(q)

    print("🔍 Cleaned Queries:", queries)

    return queries