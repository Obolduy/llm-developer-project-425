import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import email_poller  # noqa: E402

_REAL_MCP_CALL_OUTPUT = (
    '{"statusCode": 200, "body": "{\\"result\\": {\\"ticket_id\\": '
    '\\"483610b3-3af1-4133-978d-580051109cf4\\", \\"status\\": \\"open\\"}}"}'
)


def test_extract_created_ticket_id_from_real_mcp_shape():
    response_body = {
        "output": [
            {"type": "mcp_call", "name": "create_ticket", "output": _REAL_MCP_CALL_OUTPUT},
        ]
    }
    assert email_poller._extract_created_ticket_id(response_body) == "483610b3-3af1-4133-978d-580051109cf4"


def test_extract_created_ticket_id_ignores_other_tool_calls():
    response_body = {"output": [{"type": "mcp_call", "name": "list_my_tickets", "output": "[]"}]}
    assert email_poller._extract_created_ticket_id(response_body) is None


def test_extract_created_ticket_id_no_tool_calls():
    assert email_poller._extract_created_ticket_id({"output": []}) is None
