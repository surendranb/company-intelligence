# Setting Up Company Intelligence MCP Server

A zero-configuration MCP server for automated B2B company dossiers, SEC financial filings, USPTO patent portfolios, federal contracts, and DNS tech stack fingerprints.

Official Repository: [github.com/surendranb/company-intelligence](https://github.com/surendranb/company-intelligence)

---

## 1. Quickstart (Zero API Keys Required)

`company-intelligence` queries public federal, financial, and network infrastructure data sources:
- **SEC EDGAR**: 10-K, 10-Q, 8-K filings and financial statements
- **USPTO PatentsView**: Patent applications and grant portfolios
- **USASpending.gov**: Federal contracts and grant awards
- **DNS / MX / SPF / TXT Inspection**: Tech stack and vendor fingerprinting

**Zero API keys or credentials are required.**

---

## 2. Client Configuration

### Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "company-intelligence": {
      "command": "uvx",
      "args": ["company-intelligence"]
    }
  }
}
```

### Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "company-intelligence": {
      "command": "uvx",
      "args": ["company-intelligence"]
    }
  }
}
```

### Command Line / CLI Testing
```bash
uvx company-intelligence
```

---

## 3. Core Tools & Workflow

1. **`get_company_dossier(domain_or_ticker="stripe.com")`**:
   Generates a full 360-degree B2B account dossier combining DNS fingerprint, patents, SEC data (if public), and federal contracts.

2. **`get_financial_statements(ticker_or_cik="AAPL")`**:
   Extracts income statement, balance sheet, and cash flow trends from SEC EDGAR.

3. **`get_patent_portfolio(company_name="Snowflake")`**:
   Analyzes patent velocity, CPC technology classifications, and key inventors from USPTO.

4. **`get_tech_stack_fingerprint(domain="datadoghq.com")`**:
   Performs non-invasive DNS, mail exchanger, security, and verification record analysis to map cloud providers, CRM, and SaaS tooling.

5. **`get_federal_contracts(company_name="Palantir")`**:
   Audits federal awards, contracting agencies, and contract values from USASpending.

---

## 4. Troubleshooting & Operational Guidance

* **SEC EDGAR Rate Limits**: SEC allows 10 requests per second. The server automatically adheres to fair-use User-Agent headers.
* **Private vs. Public Companies**: For private companies, SEC tools return empty financial filings, but DNS fingerprinting and patent search remain fully functional.
* **Dynamic Skills**: Call `skill_read(skill_name='company_dossier_skill')` for comprehensive methodology on structuring executive account dossiers.
* **Update Verification**: Call `check_for_updates()` to check PyPI for newer versions and upgrade commands.
