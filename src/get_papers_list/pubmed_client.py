# pubmed_client.py

import requests
from typing import List

def fetch_pubmed_ids(query: str, max_results: int = 10) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_details(ids: List[str]) -> str:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text  # XML string
