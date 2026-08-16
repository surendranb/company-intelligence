"""Native unit tests for company-intelligence MCP server tools."""

import pytest
from company_intelligence.server import (
    get_company_dossier,
    get_federal_contracts,
    get_financial_statements,
    get_patent_portfolio,
    get_sec_filings_radar,
    get_tech_stack_fingerprint,
    skill_read,
    skills_list,
)


def test_get_company_dossier_ticker():
    res = get_company_dossier("AAPL")
    assert "# 🏢 Comprehensive Account Dossier: AAPL" in res
    assert "Audited US-GAAP Financials" in res
    assert "Tech Stack & Infrastructure Fingerprint" in res


def test_get_company_dossier_domain():
    res = get_company_dossier("stripe.com")
    assert "# 🏢 Comprehensive Account Dossier" in res
    assert "Live Tech Stack & Infrastructure Fingerprint" in res


def test_get_financial_statements():
    res = get_financial_statements("AAPL", periods=3)
    assert "Standardized Financial Statements" in res
    assert "Fiscal Year" in res
    assert "Revenue" in res


def test_get_patent_portfolio():
    res = get_patent_portfolio("Apple", max_patents=2)
    assert "USPTO Patent Portfolio" in res


def test_get_tech_stack_fingerprint():
    res = get_tech_stack_fingerprint("linear.app")
    assert "Live Tech Stack Fingerprint" in res
    assert "Corporate Email Infrastructure" in res


def test_get_sec_filings_radar():
    res = get_sec_filings_radar("AAPL", limit=2)
    assert "SEC EDGAR Filings Radar" in res


def test_get_federal_contracts():
    res = get_federal_contracts("Boeing", limit=2)
    assert isinstance(res, str)


def test_skills_tools():
    s_list = skills_list()
    assert "company_dossier_skill" in s_list

    s_read = skill_read("company_dossier_skill")
    assert "Company Intelligence Playbook" in s_read
