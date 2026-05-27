import requests


def build_query(keywords):
    return " AND ".join(keywords)


def search_pubmed(keywords):
    query = build_query(keywords)

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 5
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if "esearchresult" not in data:
            print("❌ PubMed error:", data)
            return []

        ids = data["esearchresult"]["idlist"]
        print(f"🔎 Query: {query} → {len(ids)} results")

        return ids

    except Exception as e:
        print("❌ PubMed request failed:", e)
        return []


def fetch_details(id_list):
    if not id_list:
        return ""

    ids = ",".join(id_list)

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        return res.text
    except Exception as e:
        print("❌ Fetch error:", e)
        return ""