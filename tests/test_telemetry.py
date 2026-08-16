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
