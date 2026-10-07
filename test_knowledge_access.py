#!/usr/bin/env python3
"""Quick test to verify Knowledge pages are accessible via the web."""

import json
import urllib.parse
import urllib.request

URL = "http://localhost:16069"
DB = "devel"
USERNAME = "admin"
PASSWORD = "admin"


def json_rpc(method, params):
    """Execute a JSON-RPC call."""
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "call",
            "params": params,
        }
    ).encode()
    req = urllib.request.Request(
        f"{URL}/web/dataset/call_kw",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    # Authenticate
    result = json_rpc(
        "call",
        {
            "model": "res.users",
            "method": "authenticate",
            "args": [DB, USERNAME, PASSWORD, {}],
        },
    )
    uid = result.get("result")
    print(f"Authenticated as user ID: {uid}")

    if not uid:
        print("ERROR: Authentication failed!")
        return

    # Get pages
    result = json_rpc(
        "call",
        {
            "model": "document.page",
            "method": "search_read",
            "args": [
                [["type", "=", "content"]],
                ["id", "name", "content"],
                0,
                20,
                "id",
            ],
        },
    )
    pages = result.get("result", [])
    print(f"\nPages found: {len(pages)}")

    for page in pages:
        has_content = bool(page.get("content") and page["content"] != "<p><br></p>")
        content_len = len(page.get("content", "")) if page.get("content") else 0
        print(
            f"  ID: {page['id']:2d} | {page['name'][:50]:50s} | Content: {content_len:5d} chars | {'OK' if has_content else 'EMPTY'}"
        )


if __name__ == "__main__":
    main()
