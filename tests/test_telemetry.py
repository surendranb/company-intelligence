"""Schema v2 Telemetry contract tests for company-intelligence."""

import pytest
from company_intelligence.telemetry import (
    ERROR_CATEGORIES,
    SCHEMA_VERSION,
    SERVER_NAME,
    _get_env_metadata,
)

SCHEMA_V2_REQUIRED_PROPS = {
    "schema_version",
    "mcp_server_name",
    "mcp_server_version",
    "$os",
    "python_version",
    "cpu_arch",
    "in_virtual_env",
    "timezone_offset",
    "run_context",
    "agent_name",
    "discovery_channel",
    "install_source",
    "session_id",
    "has_ever_worked",
    "mcp_client_name",
    "mcp_client_version",
    "mcp_protocol_version",
    "client_capabilities",
    "traceparent",
    "trace_id",
    "span_id",
    "$process_person_profile",
}


def test_schema_v2_envelope_compliance():
    metadata = _get_env_metadata()
    missing = SCHEMA_V2_REQUIRED_PROPS - set(metadata.keys())
    assert not missing, f"Missing Schema v2 properties: {missing}"
    assert metadata["schema_version"] == 2
    assert metadata["mcp_server_name"] == "company-intelligence"
    assert metadata["$process_person_profile"] is False


def test_error_categories():
    assert "APIError" in ERROR_CATEGORIES
    assert "ValidationError" in ERROR_CATEGORIES
    assert "TimeoutError" in ERROR_CATEGORIES
    assert "SourceUnavailable" in ERROR_CATEGORIES


def test_track_tool_call_v2_properties(monkeypatch):
    from company_intelligence import telemetry
    captured = []
    monkeypatch.setattr(telemetry, "track_event", lambda ev, props: captured.append((ev, props)))
    
    telemetry.track_tool_call(
        tool_name="get_company_dossier",
        duration_ms=230.4,
        status="success",
        rows_returned=15,
        result_chars=2048,
        intent="Research NVDA 3-year GAAP revenue",
        custom_props={"is_domain": False}
    )
    
    assert len(captured) == 1
    ev, props = captured[0]
    assert ev == "tool_executed"
    assert props["tool_name"] == "get_company_dossier"
    assert props["status"] == "success"
    assert props["latency_ms"] == 230
    assert props["duration_ms"] == 230
    assert props["rows_returned"] == 15
    assert props["result_chars"] == 2048
    assert props["intent"] == "Research NVDA 3-year GAAP revenue"
    assert props["is_domain"] is False


def test_classify_exception_and_error_capture(monkeypatch):
    from company_intelligence import telemetry
    from company_intelligence.telemetry import classify_exception
    
    assert classify_exception(ValueError("Invalid ticker format")) == "ValidationError"
    assert classify_exception(TimeoutError("HTTP request timed out")) == "TimeoutError"
    assert classify_exception(KeyError("404 not found in database")) == "NotFoundError"
    assert classify_exception(PermissionError("403 Forbidden unauthorized")) == "IAMError"
    assert classify_exception(Exception("Rate limit 429 exceeded")) == "RateLimitError"
    assert classify_exception(RuntimeError("503 Service Unavailable")) == "SourceUnavailable"
    
    captured = []
    monkeypatch.setattr(telemetry, "track_event", lambda ev, props: captured.append((ev, props)))
    
    telemetry.track_tool_call(
        tool_name="get_financial_statements",
        duration_ms=120.0,
        status="error",
        error_category=classify_exception(ValueError("Bad ticker")),
        error_message="Bad ticker"
    )
    
    assert len(captured) == 1
    ev, props = captured[0]
    assert ev == "tool_executed"
    assert props["status"] == "error"
    assert props["error_category"] == "ValidationError"
    assert props["error_message"] == "Bad ticker"

