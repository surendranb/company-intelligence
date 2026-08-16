"""SEC EDGAR Direct API Collector.
Zero-auth standardized extraction of US-GAAP Financial Statements, 10-K, 8-K disclosures, and CIK entity resolution.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


SEC_USER_AGENT = "CompanyIntelligence/0.1.0 (surendran@builditwithai.xyz)"
_TICKER_CACHE: Dict[str, Dict[str, Any]] = {}


def _get_sec_headers() -> Dict[str, str]:
    return {
        "User-Agent": SEC_USER_AGENT,
        "Accept": "application/json",
    }


def resolve_cik(ticker_or_name: str) -> Optional[Tuple[str, str, str]]:
    """Resolve a ticker symbol or company name to (cik_str_10_digits, ticker, entity_name)."""
    global _TICKER_CACHE
    clean_query = ticker_or_name.strip().upper()

    if not _TICKER_CACHE:
        try:
            url = "https://www.sec.gov/files/company_tickers.json"
            req = urllib.request.Request(url, headers=_get_sec_headers())
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            for entry in raw.values():
                t = entry.get("ticker", "").upper()
                c = str(entry.get("cik_str", "")).zfill(10)
                title = entry.get("title", "")
                _TICKER_CACHE[t] = {"cik": c, "ticker": t, "title": title}
                _TICKER_CACHE[title.upper()] = {"cik": c, "ticker": t, "title": title}
        except Exception:
            return None

    # 1. Exact ticker match
    if clean_query in _TICKER_CACHE:
        info = _TICKER_CACHE[clean_query]
        if info["ticker"] == clean_query:
            return info["cik"], info["ticker"], info["title"]

    # 2. Company title match (query must be in title as a whole word or prefix)
    for key, info in _TICKER_CACHE.items():
        title_upper = info["title"].upper()
        if clean_query == title_upper or f" {clean_query} " in f" {title_upper} " or title_upper.startswith(f"{clean_query} "):
            return info["cik"], info["ticker"], info["title"]

    return None


def fetch_company_facts(cik: str) -> Optional[Dict[str, Any]]:
    """Fetch structured US-GAAP facts from SEC EDGAR API."""
    cik_10 = cik.zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_10}.json"
    try:
        req = urllib.request.Request(url, headers=_get_sec_headers())
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def fetch_submissions(cik: str) -> Optional[Dict[str, Any]]:
    """Fetch recent filing history (10-K, 10-Q, 8-K) from SEC EDGAR Submissions API."""
    cik_10 = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_10}.json"
    try:
        req = urllib.request.Request(url, headers=_get_sec_headers())
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def extract_standard_financials(facts: Dict[str, Any], periods: int = 4) -> List[Dict[str, Any]]:
    """Extract standardized annual GAAP financial metrics across recent fiscal years."""
    gaap = facts.get("facts", {}).get("us-gaap", {})
    if not gaap:
        return []

    rev_concepts = [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
        "TotalRevenuesAndOtherIncome",
    ]

    def _get_annual_units(concept_name: str) -> Dict[int, float]:
        concept_data = gaap.get(concept_name, {}).get("units", {}).get("USD", [])
        annual: Dict[int, float] = {}
        for item in concept_data:
            form = item.get("form", "")
            fp = item.get("fp", "")
            frame = item.get("frame", "")
            fy = item.get("fy")
            val = item.get("val")

            if form == "10-K" and (fp == "FY" or not fp):
                if "Q" not in frame and fy and val is not None:
                    annual[fy] = float(val)
        return annual

    revenue_map: Dict[int, float] = {}
    for rc in rev_concepts:
        m = _get_annual_units(rc)
        if m:
            if not revenue_map:
                revenue_map = m
            else:
                m_max = max(m.keys())
                cur_max = max(revenue_map.keys())
                if m_max > cur_max or (m_max == cur_max and len(m) > len(revenue_map)):
                    revenue_map = m

    gross_profit_map = _get_annual_units("GrossProfit")
    op_income_map = _get_annual_units("OperatingIncomeLoss")
    net_income_map = _get_annual_units("NetIncomeLoss")
    rd_expense_map = _get_annual_units("ResearchAndDevelopmentExpense")
    cash_flow_map = _get_annual_units("NetCashProvidedByUsedInOperatingActivities")

    all_years = sorted(set(revenue_map.keys()) | set(net_income_map.keys()), reverse=True)[:periods]

    financials_table = []
    for yr in all_years:
        rev = revenue_map.get(yr)
        gp = gross_profit_map.get(yr)
        op_inc = op_income_map.get(yr)
        ni = net_income_map.get(yr)
        rd = rd_expense_map.get(yr)
        ocf = cash_flow_map.get(yr)

        gm_pct = (gp / rev * 100.0) if (gp and rev and rev > 0) else None
        om_pct = (op_inc / rev * 100.0) if (op_inc and rev and rev > 0) else None
        nm_pct = (ni / rev * 100.0) if (ni and rev and rev > 0) else None

        financials_table.append({
            "fiscal_year": yr,
            "revenue": rev,
            "gross_profit": gp,
            "gross_margin_pct": round(gm_pct, 1) if gm_pct is not None else None,
            "operating_income": op_inc,
            "operating_margin_pct": round(om_pct, 1) if om_pct is not None else None,
            "net_income": ni,
            "net_margin_pct": round(nm_pct, 1) if nm_pct is not None else None,
            "rd_expense": rd,
            "operating_cash_flow": ocf,
        })

    return financials_table


def extract_recent_filings(submissions: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
    """Extract recent 10-K, 10-Q, and 8-K filings with accession numbers."""
    recent = submissions.get("filings", {}).get("recent", {})
    if not recent:
        return []

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accession_nums = recent.get("accessionNumber", [])
    descriptions = recent.get("primaryDocDescription", [])
    doc_names = recent.get("primaryDocument", [])

    filings = []
    for i in range(min(len(forms), limit)):
        form_type = forms[i]
        filing_date = dates[i] if i < len(dates) else ""
        acc = accession_nums[i] if i < len(accession_nums) else ""
        desc = descriptions[i] if i < len(descriptions) else ""
        doc = doc_names[i] if i < len(doc_names) else ""

        acc_clean = acc.replace("-", "")
        cik = submissions.get("cik", "")
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_clean}/{doc}" if cik and acc and doc else ""

        filings.append({
            "form": form_type,
            "filing_date": filing_date,
            "description": desc or form_type,
            "accession_number": acc,
            "url": url,
        })

    return filings
