import streamlit as st
import requests

# =====================
# 🎨 页面配置（产品感）
# =====================
st.set_page_config(
    page_title="AI Evidence Finder",
    page_icon="🧠",
    layout="centered"
)

# =====================
# 🧠 Header（产品包装）
# =====================
st.title("🧠 AI Medical Evidence Finder")
st.caption("Turn clinical text into PubMed evidence in seconds.")

st.markdown("""
💡 Paste a clinical sentence or research question below  
and get **relevant PubMed evidence with supporting sentences**
""")

# =====================
# 输入区
# =====================
query = st.text_area(
    "Enter clinical statement:",
    placeholder="e.g. Acupuncture reduces hot flashes in menopausal women"
)

# =====================
# 搜索按钮
# =====================
if st.button("🔍 Find Evidence"):

    if not query.strip():
        st.warning("Please enter a valid sentence.")
        st.stop()

    with st.spinner("Searching PubMed & analyzing evidence..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/search",
                params={"query": query},
                timeout=60
            )

            if response.status_code != 200:
                st.error(f"Server error: {response.status_code}")
                st.stop()

            results = response.json()

        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    # =====================
    # 空结果处理
    # =====================
    if not results:
        st.warning("No relevant evidence found.")
        st.stop()

    st.success(f"Found {len(results)} relevant papers")

    # =====================
    # 结果展示（产品核心）
    # =====================
    for i, r in enumerate(results):

        st.markdown("---")

        # 标题
        st.subheader(f"{i+1}. {r.get('title', 'No title')}")

        # 链接
        link = r.get("link", "")
        if link:
            st.markdown(f"🔗 [View on PubMed]({link})")

        # 评分（增强可信度）
        score = r.get("score", 0)
        st.caption(f"Relevance score: {score:.3f}")

        # 证据句子
        st.markdown("### 📌 Evidence sentence")
        st.write(r.get("matched_sentence", "No sentence found"))

        # explain（如果后端有）
        if "explain" in r:
            with st.expander("🔬 Score breakdown"):
                st.write(r["explain"])

    st.markdown("---")
    st.success("Done ✔")



# import streamlit as st
# import requests
# from backend.routes.search import search
#
# st.set_page_config(
#     page_title="AI Medical Citation Finder",
#     page_icon="🧠",
#     layout="centered"
# )
#
# st.title("🧠 AI Medical Citation Finder")
# st.markdown(
#     "Enter a clinical sentence and find supporting PubMed evidence."
# )
# query = st.text_input("🔍 Enter your sentence:")
#
# if st.button("Search"):
#
#     if not query.strip():
#         st.warning("Please enter a sentence.")
#         st.stop()
#
#     with st.spinner("🔎 Searching PubMed and extracting evidence..."):
#
#         try:
#             response = requests.post(
#                 "http://127.0.0.1:8000/search",
#                 params={"query": query},
#                 timeout=60
#             )
#
#             if response.status_code != 200:
#                 st.error(f"Server error: {response.status_code}")
#                 st.stop()
#
#             results = response.json()
#
#         except Exception as e:
#             st.error(f"Request failed: {e}")
#             st.stop()
#
#     if not results:
#         st.warning("No relevant papers found.")
#         st.stop()
#
#     for r in results:
#         st.subheader(r.get("title", "No title"))
#
#         link = r.get("link", "")
#         if link:
#             st.write(f"[View on PubMed]({link})")
#
#         st.write("📌 Matched sentence:")
#
#         sentence = r.get("matched_sentence", "")
#         if sentence:
#             st.write(sentence)
#         else:
#             st.write("No sentence extracted.")
#
#         st.divider()