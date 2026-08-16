"""Live DNS & SaaS Tech Stack Fingerprinting Collector.
Inspects MX, TXT/SPF, and NS records to identify corporate email providers, cloud hosting, and SaaS infrastructure.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set
import dns.resolver


# Known signature patterns in DNS records
EMAIL_SIGNATURES = {
    "google": ("Google Workspace", ["google.com", "googlemail.com", "aspmx.l.google.com"]),
    "microsoft": ("Microsoft 365 / Exchange Online", ["outlook.com", "protection.outlook.com", "microsoft.com"]),
    "mimecast": ("Mimecast Email Security", ["mimecast.com"]),
    "proofpoint": ("Proofpoint Enterprise Protection", ["pphosted.com", "proofpoint.com"]),
    "proton": ("Proton Mail Enterprise", ["protonmail.ch"]),
    "fastmail": ("Fastmail", ["fastmail.com"]),
}

SAAS_TXT_SIGNATURES = {
    "salesforce": "Salesforce CRM",
    "hubspot": "HubSpot Marketing/CRM",
    "stripe": "Stripe Payments",
    "sendgrid": "SendGrid Email Infrastructure",
    "zendesk": "Zendesk Support",
    "atlassian": "Atlassian Cloud (Jira/Confluence)",
    "posthog": "PostHog Product Analytics",
    "segment": "Twilio Segment CDP",
    "datadog": "Datadog Observability",
    "mailgun": "Mailgun Transactional Email",
    "intercom": "Intercom Customer Messaging",
    "github-verification": "GitHub Enterprise Organization",
    "docusign": "DocuSign",
    "slack": "Slack Enterprise Grid",
    "apple-domain-verification": "Apple Pay / Apple Services",
    "google-site-verification": "Google Cloud / Search Console",
    "ms-identity": "Microsoft Azure AD / Entra ID",
}

HOSTING_NS_SIGNATURES = {
    "cloudflare": "Cloudflare CDN & Security",
    "awsdns": "Amazon Web Services (Route 53)",
    "googledomains": "Google Cloud DNS",
    "akamai": "Akamai Edge Cloud",
    "fastly": "Fastly Edge Cloud",
    "azure": "Microsoft Azure DNS",
}


def _clean_domain(raw_domain: str) -> str:
    domain = raw_domain.strip().lower()
    domain = re.sub(r"^https?://", "", domain)
    domain = re.sub(r"/.*$", "", domain)
    domain = re.sub(r"^www\.", "", domain)
    return domain


def fingerprint_domain(raw_domain: str) -> Dict[str, Any]:
    """Inspect authoritative DNS records of a domain to map out tech stack & providers."""
    domain = _clean_domain(raw_domain)
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5.0
    resolver.lifetime = 5.0

    detected_email_providers: Set[str] = set()
    detected_saas: Set[str] = set()
    detected_hosting: Set[str] = set()
    raw_mx: List[str] = []
    raw_txt: List[str] = []
    raw_ns: List[str] = []
    dmarc_configured = False

    # 1. Resolve MX
    try:
        mx_records = resolver.resolve(domain, "MX")
        for rdata in mx_records:
            mx_host = str(rdata.exchange).lower()
            raw_mx.append(mx_host)
            for provider_id, (provider_name, patterns) in EMAIL_SIGNATURES.items():
                if any(p in mx_host for p in patterns):
                    detected_email_providers.add(provider_name)
    except Exception:
        pass

    # 2. Resolve TXT & SPF
    try:
        txt_records = resolver.resolve(domain, "TXT")
        for rdata in txt_records:
            for string_item in rdata.strings:
                txt_str = string_item.decode("utf-8", errors="ignore").lower()
                raw_txt.append(txt_str)
                for saas_key, saas_name in SAAS_TXT_SIGNATURES.items():
                    if saas_key in txt_str:
                        detected_saas.add(saas_name)
    except Exception:
        pass

    # 3. Resolve NS
    try:
        ns_records = resolver.resolve(domain, "NS")
        for rdata in ns_records:
            ns_host = str(rdata.target).lower()
            raw_ns.append(ns_host)
            for host_key, host_name in HOSTING_NS_SIGNATURES.items():
                if host_key in ns_host:
                    detected_hosting.add(host_name)
    except Exception:
        pass

    # 4. Check DMARC
    try:
        dmarc_records = resolver.resolve(f"_dmarc.{domain}", "TXT")
        if dmarc_records:
            dmarc_configured = True
    except Exception:
        dmarc_configured = False

    return {
        "domain": domain,
        "email_infrastructure": list(detected_email_providers) if detected_email_providers else ["Undetected / Self-Hosted"],
        "detected_saas_and_tooling": sorted(list(detected_saas)),
        "hosting_and_cdn": list(detected_hosting) if detected_hosting else ["Standard / Non-Cloudflare Nameservers"],
        "security_posture": {
            "dmarc_enabled": dmarc_configured,
            "spf_configured": any("v=spf1" in t for t in raw_txt),
            "mx_count": len(raw_mx),
        },
        "raw_mx_sample": raw_mx[:3],
    }
