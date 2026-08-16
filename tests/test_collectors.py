"""Unit tests for company-intelligence collectors."""

import pytest
from company_intelligence.collectors.dns_fingerprint import fingerprint_domain
from company_intelligence.collectors.government import fetch_federal_contracts
from company_intelligence.collectors.patents import fetch_patents_by_assignee
from company_intelligence.collectors.sec_edgar import (
    extract_recent_filings,
    extract_standard_financials,
    fetch_company_facts,
    fetch_submissions,
    resolve_cik,
)


def test_sec_cik_resolution():
    res = resolve_cik("AAPL")
    assert res is not None
    cik, ticker, title = res
    assert ticker == "AAPL"
    assert "Apple" in title


def test_sec_company_facts_and_financials():
    # Apple CIK
    facts = fetch_company_facts("0000320193")
    assert facts is not None
    financials = extract_standard_financials(facts, periods=2)
    assert len(financials) > 0
    assert "fiscal_year" in financials[0]
    assert "revenue" in financials[0]
    assert financials[0]["revenue"] is not None


def test_sec_submissions():
    subs = fetch_submissions("0000320193")
    assert subs is not None
    filings = extract_recent_filings(subs, limit=3)
    assert len(filings) > 0
    assert "form" in filings[0]
    assert "accession_number" in filings[0]


def test_patents_collector():
    patents = fetch_patents_by_assignee("Apple", max_patents=2)
    assert isinstance(patents, list)
    if patents:
        assert "patent_number" in patents[0]
        assert "title" in patents[0]


def test_dns_fingerprint():
    data = fingerprint_domain("stripe.com")
    assert data["domain"] == "stripe.com"
    assert "email_infrastructure" in data
    assert "security_posture" in data
    assert data["security_posture"]["mx_count"] > 0


def test_federal_contracts():
    contracts = fetch_federal_contracts("Boeing", limit=2)
    assert isinstance(contracts, list)
