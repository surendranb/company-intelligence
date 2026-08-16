"""USAspending Federal Procurement & Contract Collector.
Zero-auth lookup for US Federal contractor status, prime award totals, and agency spending.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, List, Optional


USER_AGENT = "company-intelligence/0.1.0 (https://github.com/surendranb/company-intelligence; usaspending-bot)"


def fetch_federal_contracts(
    company_name: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Fetch federal contract awards and spending for a company from USAspending.gov API."""
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    payload = {
        "filters": {
            "recipient_search_text": [company_name.strip()],
            "award_type_codes": ["A", "B", "C", "D"],  # Contracts
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Awarding Agency",
            "Award Amount",
            "Description",
            "Start Date",
            "End Date",
        ],
        "limit": limit,
        "page": 1,
        "sort": "Award Amount",
        "order": "desc",
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"User-Agent": USER_AGENT, "Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        raw_results = data.get("results", [])
        awards = []
        for r in raw_results:
            desc = r.get("Description", "") or "Federal Procurement Contract"
            amount = r.get("Award Amount", 0.0)
            agency = r.get("Awarding Agency", "Federal Agency")
            recipient = r.get("Recipient Name", company_name)
            award_id = r.get("Award ID", "")

            awards.append({
                "award_id": award_id,
                "recipient": recipient,
                "awarding_agency": agency,
                "obligated_amount": float(amount) if amount is not None else 0.0,
                "description": desc[:300] + ("..." if len(desc) > 300 else ""),
                "start_date": r.get("Start Date", ""),
                "end_date": r.get("End Date", ""),
            })
        return awards
    except Exception:
        return []
