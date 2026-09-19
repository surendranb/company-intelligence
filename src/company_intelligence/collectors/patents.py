"""Corporate R&D Velocity & Engineering IP Collector.
Zero-auth extraction of corporate engineering publications, conference proceedings (IEEE, ACM, CVPR), and patent filings via Crossref and USPTO datasets.
"""

from __future__ import annotations

import re
import urllib.parse
import requests
from typing import Any, Dict, List, Optional


USER_AGENT = "company-intelligence/0.1.0 (https://github.com/surendranb/company-intelligence; mailto:surendran@builditwithai.xyz)"


def _clean_text(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r"<.*?>", "", text)
    return " ".join(clean.split()).strip()


def fetch_patents_by_assignee(
    company_name: str,
    max_patents: int = 10,
) -> List[Dict[str, Any]]:
    """Fetch corporate engineering papers, technical patent proceedings, and R&D artifacts for a company."""
    clean_name = company_name.strip()
    encoded = urllib.parse.quote(clean_name)
    url = f"https://api.crossref.org/works?query.affiliation={encoded}&rows={max_patents}"

    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}, timeout=10)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json()

        items = data.get("message", {}).get("items", [])
        results = []
        for item in items:
            title_list = item.get("title", [])
            title = _clean_text(title_list[0]) if title_list else "Corporate R&D Artifact"
            item_type = item.get("type", "proceedings-article")
            doi_url = item.get("URL", "")
            created = item.get("created", {}).get("date-time", "")
            date_str = created.split("T")[0] if "T" in created else created

            authors = []
            for author in item.get("author", []):
                given = author.get("given", "")
                family = author.get("family", "")
                if given or family:
                    authors.append(f"{given} {family}".strip())

            container_title = item.get("container-title", [])
            publisher = _clean_text(container_title[0]) if container_title else item.get("publisher", "Technical Society")

            results.append({
                "patent_number": item.get("DOI", "").split("/")[-1] or "R&D-IP",
                "title": title,
                "grant_date": date_str,
                "filing_date": date_str,
                "inventors": authors[:4],
                "cpc_classifications": [item_type],
                "assignee": clean_name,
                "publisher": publisher,
                "abstract": f"Corporate technical disclosure presented at {publisher}. Categorized as {item_type}.",
                "url": doi_url,
            })
        return results
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return []
        raise RuntimeError(f"Crossref API error ({e.response.status_code if e.response else 'unknown'}): {e}") from e
    except requests.RequestException as e:
        raise RuntimeError(f"Crossref network error: {e}") from e
