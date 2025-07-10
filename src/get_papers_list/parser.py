# parser.py

import xml.etree.ElementTree as ET
from typing import List, Dict

def parse_pubmed_xml(xml_data: str) -> List[Dict]:
    root = ET.fromstring(xml_data)
    results = []

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or article.findtext(".//PubDate/MedlineDate") or "Unknown"

        authors = article.findall(".//Author")
        non_academic_authors = []
        affiliations = set()
        emails = []

        for author in authors:
            last = author.findtext("LastName") or ""
            fore = author.findtext("ForeName") or ""
            name = f"{fore} {last}".strip()
            aff_elements = author.findall(".//AffiliationInfo/Affiliation")

            for aff in aff_elements:
                aff_text = aff.text or ""
                if is_non_academic(aff_text):
                    affiliations.add(aff_text)
                    non_academic_authors.append(name)
                if "@" in aff_text:
                    emails.append(extract_email(aff_text))

        if non_academic_authors:
            results.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(affiliations),
                "Corresponding Author Email": emails[0] if emails else "N/A"
            })

    return results

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "school", "institute", "department", "hospital", "centre", "center"]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)

def extract_email(text: str) -> str:
    import re
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""
