# SPDX-License-Identifier: MIT
"""Unit tests for check_for_updates tool, get_upgrade_nudge, and cache throttling."""

import json
import time
from unittest.mock import MagicMock, patch

from company_intelligence import server
from company_intelligence.updates import (
    _FLEET_CACHE_FILE,
    _parse_version,
    check_server_update,
    get_upgrade_nudge,
)


def test_parse_version():
    assert _parse_version("0.1.4") == (0, 1, 4)
    assert _parse_version("v0.1.4") == (0, 1, 4)
    assert _parse_version("0.1.5") > _parse_version("0.1.4")
    assert _parse_version("0.2.0") > _parse_version("0.1.4")
    assert _parse_version("0.1.10") > _parse_version("0.1.4")
    assert _parse_version("unknown") == (0,)
    assert _parse_version("") == (0,)


def test_check_server_update_update_available(tmp_path):
    mock_pypi_data = json.dumps({"info": {"version": "0.2.0"}}).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = mock_pypi_data
    mock_resp.__enter__.return_value = mock_resp

    test_cache = tmp_path / "fleet_updates.json"
    with patch("company_intelligence.updates._FLEET_CACHE_FILE", test_cache), \
         patch("urllib.request.urlopen", return_value=mock_resp):
        res = check_server_update("company-intelligence", "0.1.4", force_check=True)

        assert res["server"] == "company-intelligence"
        assert res["current_version"] == "0.1.4"
        assert res["latest_version"] == "0.2.0"
        assert res["update_available"] is True
        assert res["upgrade_command"] == "uvx --refresh company-intelligence"
        assert "Inform the user to run 'uvx --refresh company-intelligence' to update." in res["message"]
        assert "Do NOT attempt to run this command yourself in this session." in res["message"]


def test_check_server_update_up_to_date(tmp_path):
    mock_pypi_data = json.dumps({"info": {"version": "0.1.4"}}).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = mock_pypi_data
    mock_resp.__enter__.return_value = mock_resp

    test_cache = tmp_path / "fleet_updates.json"
    with patch("company_intelligence.updates._FLEET_CACHE_FILE", test_cache), \
         patch("urllib.request.urlopen", return_value=mock_resp):
        res = check_server_update("company-intelligence", "0.1.4", force_check=True)

        assert res["update_available"] is False
        assert res["upgrade_command"] is None
        assert res["message"] == "company-intelligence is up to date (v0.1.4)."


def test_get_upgrade_nudge_throttle(tmp_path):
    test_cache = tmp_path / "fleet_updates.json"
    test_cache.write_text(json.dumps({
        "company-intelligence": {
            "latest_version": "0.2.0",
            "last_checked": time.time(),
            "last_nudged": 0,
        }
    }))

    with patch("company_intelligence.updates._FLEET_CACHE_FILE", test_cache):
        # First call: should produce nudge
        nudge1 = get_upgrade_nudge("company-intelligence", "0.1.4")
        assert "[NOTICE: An updated version of company-intelligence is available (v0.2.0, current: v0.1.4)." in nudge1
        assert "Inform the user to run 'uvx --refresh company-intelligence' to update. Do NOT attempt to run this command yourself in this session." in nudge1

        # Second call immediately after: should be throttled
        nudge2 = get_upgrade_nudge("company-intelligence", "0.1.4")
        assert nudge2 == ""

        # Bump latest_version to 0.3.0: should re-nudge despite throttle
        cache = json.loads(test_cache.read_text())
        cache["company-intelligence"]["latest_version"] = "0.3.0"
        test_cache.write_text(json.dumps(cache))

        nudge3 = get_upgrade_nudge("company-intelligence", "0.1.4")
        assert "v0.3.0" in nudge3


def test_check_for_updates_tool():
    res_str = server.check_for_updates()
    assert isinstance(res_str, str)
    res = json.loads(res_str)
    assert res["server"] == "company-intelligence"
    assert "current_version" in res
    assert "latest_version" in res
    assert "update_available" in res
    assert "message" in res


def test_tool_wrapper_upgrade_notice_attachment():
    @server.mcp.tool(name="_test_dummy_dict_tool")
    def _dummy_dict_tool():
        return {"data": "test_data"}

    @server.mcp.tool(name="_test_dummy_str_tool")
    def _dummy_str_tool():
        return "test_string"

    fake_nudge = "\n\n[NOTICE: An updated version is available]"
    with patch("company_intelligence.server.get_upgrade_nudge", return_value=fake_nudge):
        res_dict = _dummy_dict_tool()
        assert isinstance(res_dict, dict)
        assert res_dict.get("_upgrade_notice") == fake_nudge.strip()

        res_str = _dummy_str_tool()
        assert fake_nudge in res_str

        # check_for_updates tool should never have nudge appended
        res_updates = server.check_for_updates()
        assert fake_nudge not in res_updates
