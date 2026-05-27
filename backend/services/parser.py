import xml.etree.ElementTree as ET

def extract_articles(xml_data):
    if not xml_data:  #防止xml空
        return []

    try:
        root = ET.fromstring(xml_data)  #xml字符串->树结构
    except Exception as e:
        print("❌ XML parse error:", e)
        return []
    articles = []

    for article in root.findall(".//PubmedArticle"):  #遍历每篇文章
        title = article.findtext(".//ArticleTitle")
        abstract = article.findtext(".//AbstractText")
        pmid = article.findtext(".//PMID")

        if not title:
            continue

        articles.append({   #转化成标题、摘要、链接的形式
                "pmid": pmid,
                "title": title,
                "abstract": abstract if abstract else "",
                "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })



    return articles


