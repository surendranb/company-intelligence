---
name: company_dossier_skill
description: Tactical operational playbook for generating exhaustive B2B account dossiers, financial tables, patent velocity charts, and tech stack fingerprints.
version: "1.0.0"
---

# Company Intelligence Playbook

## 1. When to Use
Use this skill when:
- Conducting deep B2B sales account research (SDR / AE account prep).
- Performing competitive due diligence on private or public tech enterprises.
- Auditing live corporate infrastructure, email routing, and SaaS tools via DNS.
- Pulling multi-year standardized US-GAAP audited financial statements (Revenue, Margins, R&D, Cash Flow).
- Inspecting patent filings and technological IP classifications (USPTO).
- Checking US federal contracting awards and procurement history (USAspending).

## 2. Tool Workflows

### A. The 1-Call Account Dossier
Call `get_company_dossier()` with a company domain or ticker:
```json
{
  "domain_or_ticker": "AAPL"
}
```
Or for private/unlisted tech firms:
```json
{
  "domain_or_ticker": "stripe.com"
}
```

### B. Standardized Financials Analysis
To inspect 5-year GAAP revenue, gross margin, operating margin, and R&D spending trends:
```json
{
  "ticker_or_cik": "MSFT",
  "periods": 5
}
```

### C. Technology & Patent Portfolio Analysis
To evaluate whether a company has authentic engineering patents vs marketing claims:
```json
{
  "company_name": "Palantir",
  "timeframe": "24m"
}
```

### D. Live Tech Stack Fingerprint
To map out email providers, CDNs, and detected marketing/product SaaS tooling:
```json
{
  "domain": "airbnb.com"
}
```

## 3. Formatting Standards
- **Standardized Multi-Year Tables**: Output audited numbers in Millions/Billions ($M / $B) with margin percentages.
- **Tech Stack Categorization**: Group detected infrastructure into Email, Security, Cloud/CDN, and SaaS tooling.
- **Patent Breadth**: Highlight primary CPC technology classes (e.g. `G06N` for AI/ML, `H04L` for Networks).
