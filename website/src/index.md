---
layout: layout.njk
title: "Company Intelligence: B2B Account Dossier & Regulatory Engine"
description: "Comprehensive B2B account dossier, SEC GAAP financials, USPTO patents, and DNS tech stack fingerprinting for AI agents."
kicker: "B2B ACCOUNT INTELLIGENCE"
subkicker: "Multi-Source Verification Engine"
header_badge: "SEC GAAP Financials · USPTO Patents · DNS Fingerprinting · Zero Auth"
lede: "Company Intelligence compresses massive regulatory filings, patent registries, DNS records, and federal procurement datasets into clean, token-efficient executive account dossiers. Built for AI sales reps, enterprise analyst agents, and market researchers."
chips:
  - "MCP 2.0"
  - "SEC EDGAR"
  - "USPTO / CrossRef"
  - "USAspending.gov"
  - "TypeScript / Python"
toc:
  - id: "quickstart"
    title: "1. Universal Quickstart"
  - id: "the-layers"
    title: "2. The 5 Intelligence Layers"
  - id: "agent-setup"
    title: "3. AI Agent Integration"
  - id: "tools-reference"
    title: "4. Tool & Parameter Reference"
  - id: "sample-dossier"
    title: "5. Sample Executive Output"
---

<section id="quickstart" class="space-y-6">
<div class="kicker">01 / Getting Started</div>

## Universal Quickstart

`company-intelligence` provides instant access to corporate filings and technical registries without requiring any API keys:

```bash
# ⚡ Option 1: Universal 1-Line Installer
curl -fsSL https://company-intelligence.builditwithai.xyz/install | bash

# 🐍 Option 2: Run via Python (uvx)
uvx company-intelligence

# 📦 Option 3: Run via Node (npx)
npx -y company-intelligence
```

</section>

---

<section id="the-layers" class="space-y-6">
<div class="kicker">02 / Multi-Source Grounding</div>

## The 5 Intelligence Layers

Instead of querying raw web search engines that hallucinate financial numbers, `company-intelligence` queries authoritative public registries directly:

<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
<div class="p-3.5 bg-[#fbfbfa] rounded-lg border border-[#e5e6e4] space-y-1">
<b>1. 📊 Audited US-GAAP Financials</b>
<p class="text-[#747982] leading-relaxed !mb-0">5-year standardized tables from SEC EDGAR Company Facts: Revenue, Gross Margin %, Operating Margin %, Net Income, R&D Expense, and Operating Cash Flow.</p>
</div>
<div class="p-3.5 bg-[#fbfbfa] rounded-lg border border-[#e5e6e4] space-y-1">
<b>2. 📑 Regulatory Filings Radar</b>
<p class="text-[#747982] leading-relaxed !mb-0">Tracks recent 10-K annuals, 10-Q quarterlies, 8-K material events, Form 4 insider transactions, and Form 144 disclosures with direct SEC archive URLs.</p>
</div>
<div class="p-3.5 bg-[#fbfbfa] rounded-lg border border-[#e5e6e4] space-y-1">
<b>3. 🌐 DNS Tech Stack Fingerprint</b>
<p class="text-[#747982] leading-relaxed !mb-0">Real-time DNS probe (MX, TXT, SPF, NS) detecting email infrastructure (Google vs M365), hosting/CDN, and 20+ SaaS tool signatures (Salesforce, Stripe, PostHog, Datadog).</p>
</div>
<div class="p-3.5 bg-[#fbfbfa] rounded-lg border border-[#e5e6e4] space-y-1">
<b>4. 🔬 R&D IP & Patents</b>
<p class="text-[#747982] leading-relaxed !mb-0">Corporate engineering research publications, conference proceedings (IEEE, ACM, CVPR), and granted USPTO patent filings.</p>
</div>
<div class="p-3.5 bg-[#fbfbfa] rounded-lg border border-[#e5e6e4] space-y-1">
<b>5. 🏛️ Federal Procurement</b>
<p class="text-[#747982] leading-relaxed !mb-0">Historical US prime contractor federal awards, awarding agencies, and contract values via USAspending.gov.</p>
</div>
</div>

</section>

---

<section id="agent-setup" class="space-y-6">
<div class="kicker">03 / Agent Integration</div>

## AI Agent Integration

Add `company-intelligence` to your agent runtime:

### Claude Desktop & Claude Code
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

### Cursor, Windsurf & Antigravity
Add to IDE settings:

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

</section>

---

<section id="tools-reference" class="space-y-6">
<div class="kicker">04 / API & Tools</div>

## Tool & Parameter Reference

| Tool Name | Parameters | Description |
|:---|:---|:---|
| `get_company_dossier` | `query` *(ticker or domain)* | **1-call comprehensive B2B account dossier** combining financials, filings, tech stack, R&D, and federal contracts. |
| `get_financial_statements` | `ticker_or_cik`, `periods` | Standardized 5-year annual US-GAAP financial metrics and margin trends. |
| `get_tech_stack_fingerprint` | `domain` | Live DNS inspection detecting email, hosting, and SaaS vendor signatures. |
| `get_sec_filings_radar` | `ticker_or_cik`, `limit` | Recent regulatory filings and material event disclosures from SEC EDGAR. |
| `get_patent_portfolio` | `company_name`, `max_patents` | Corporate engineering publications and patent grants. |
| `get_federal_contracts` | `company_name`, `limit` | US federal contract procurement history and prime award values. |

</section>

---

<section id="sample-dossier" class="space-y-6">
<div class="kicker">05 / Output Format</div>

## Sample Executive Output

When an agent calls `get_company_dossier("SNOW")`, it receives a structured markdown summary optimized for immediate analysis:

```markdown
# 🏢 Snowflake Inc. (NYSE: SNOW · CIK: 0001640147)
- **Domain:** snowflake.com
- **Revenue (FY24):** $2.81B (+35.8% YoY)
- **Gross Margin:** 67.8% | **R&D Intensity:** 34.2% of Revenue
- **Email Infrastructure:** Google Workspace (MX: aspmx.l.google.com)
- **Cloud & CDN:** Amazon Web Services, Cloudflare
- **Active SaaS Vendors:** Salesforce, Marketo, Stripe, Workday, Datadog
- **Granted Patents:** 142 (Data warehousing, query acceleration, secure sharing)
- **Federal Awards:** DoD, Dept of Veterans Affairs ($18.4M active obligations)
```

</section>
