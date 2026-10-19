"""MCP Server for OpenAPI Spec to MCP Tool Synthesizer.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import OpenApiSpecToMcpToolSynthesizer

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "synthesize_tools",
                                "description": "Synthesize MCP tool definitions from OpenAPI 3.0 specification",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "spec": {"type": "object", "description": "OpenAPI 3.0 specification dict"}
                                    },
                                    "required": ["spec"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                spec = args.get("spec", {})
                res = OpenApiSpecToMcpToolSynthesizer.synthesize_tools(spec)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
