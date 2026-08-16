# 🏢 company-intelligence

[![PyPI version](https://img.shields.io/pypi/v/company-intelligence.svg?color=blue)](https://pypi.org/project/company-intelligence/)
[![NPM version](https://img.shields.io/npm/v/company-intelligence.svg?color=green)](https://www.npmjs.com/package/company-intelligence)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP 2.0](https://img.shields.io/badge/MCP-2.0-purple.svg)](https://modelcontextprotocol.io/)
[![Zero Auth Required](https://img.shields.io/badge/auth-zero_keys_required-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Comprehensive B2B Account Dossier, SEC GAAP Financials, USPTO/Crossref R&D IP & Live Tech Stack Registry Engine for AI Agents.**

`company-intelligence` compresses massive regulatory filings, patent registries, DNS records, and federal procurement datasets into clean, token-efficient executive account dossiers. **Zero API keys or authentication required.**

---

## 🚀 Quick Start

### ⚡ Option 1: Universal 1-Line Installer
```bash
curl -fsSL https://company-intelligence.builditwithai.xyz/install | bash
```

### 🐍 Option 2: Run via Python (`uvx`)
```bash
uvx company-intelligence
```

### 📦 Option 3: Run via Node (`npx`)
```bash
npx -y company-intelligence
```

---

## 🛠️ Model Context Protocol (MCP) Setup

Add `company-intelligence` directly to your agent client configuration:

### 🤖 Claude Desktop / Claude Code
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "company-intelligence": {
      "command": "uvx",
      "args": ["--from", "company-intelligence", "company-intelligence"]
    }
  }
}
```

### 💻 Cursor / Windsurf / Antigravity
Add to your IDE MCP settings:
```json
{
  "mcpServers": {
    "company-intelligence": {
      "command": "npx",
      "args": ["-y", "company-intelligence"]
    }
  }
}
```

---

## 🧭 Intelligence Dimensions

`company-intelligence` provides multi-source verification across 5 enterprise intelligence layers:

1. **📊 Audited US-GAAP Financials**: 5-year standardized tables from SEC EDGAR Company Facts (Revenue, Gross Margin %, Operating Margin %, Net Income, R&D Expense, Operating Cash Flow).
2. **📑 Regulatory Disclosures**: Recent 10-K, 10-Q, 8-K material event filings, Form 4 insider transactions, and Form 144 disclosures with direct SEC archive links.
3. **🌐 Live Tech Stack Fingerprint**: Real-time DNS probe (MX, TXT/SPF, NS) identifying email infrastructure (Google Workspace vs M365), cloud hosting/CDN, and 20+ SaaS tool signatures (Salesforce, Stripe, PostHog, Datadog, Hubspot).
4. **🔬 R&D IP & Engineering Velocity**: Corporate technical publications, conference proceedings (IEEE, ACM, CVPR), and granted patent filings.
5. **🏛️ US Federal Procurement**: Historical prime contractor federal awards and funding agencies via USAspending.gov.

---

## 📡 Available Tools

| Tool Name | Parameters | Description |
|---|---|---|
| `get_company_dossier` | `query` *(ticker or domain)* | 1-call comprehensive B2B account dossier combining financials, filings, tech stack, R&D, and federal contracts. |
| `get_financial_statements` | `ticker_or_cik`, `periods` | Standardized 5-year annual US-GAAP financial metrics and margin trends. |
| `get_tech_stack_fingerprint` | `domain` | Live DNS inspection detecting email, hosting, security posture, and SaaS vendor signatures. |
| `get_sec_filings_radar` | `ticker_or_cik`, `limit` | Recent regulatory filings and material event disclosures from SEC EDGAR. |
| `get_patent_portfolio` | `company_name`, `max_patents` | Corporate engineering publications, conference papers, and patent filings. |
| `get_federal_contracts` | `company_name`, `limit` | US federal contract procurement history and prime award values. |
| `skill_read` | `skill_name` | Load bundled operational skills and account intelligence prompts dynamically. |
| `skills_list` | *(none)* | List available operational skills. |

---

## 🔒 Telemetry

To opt out of anonymous usage telemetry:
```bash
export DO_NOT_TRACK=1
```

---

## 📄 License

MIT License. Free and open source for all developers and AI agents.
