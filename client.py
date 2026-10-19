"""OpenAPI Spec to MCP Tool Synthesizer.
100% Python Standard Library.
"""
import re

class OpenApiSpecToMcpToolSynthesizer:
    """Inspect OpenAPI 3.0 specs and synthesize schema-compliant MCP tool declarations."""

    @staticmethod
    def synthesize_tools(spec: dict) -> dict:
        paths = spec.get("paths", {})
        tools = []
        endpoints_processed = 0

        for path, path_item in paths.items():
            for method in ["get", "post", "put", "delete", "patch"]:
                if method not in path_item:
                    continue
                op = path_item[method]
                endpoints_processed += 1

                op_id = op.get("operationId")
                if not op_id:
                    clean_path = re.sub(r'[^a-zA-Z0-9]+', '_', path).strip('_')
                    op_id = f"{method}_{clean_path}"

                summary = op.get("summary") or op.get("description") or f"Execute {method.upper()} on {path}"
                properties = {}
                required = []

                for param in op.get("parameters", []):
                    p_name = param.get("name")
                    if not p_name:
                        continue
                    p_desc = param.get("description", "")
                    p_schema = param.get("schema", {})
                    p_type = p_schema.get("type", "string")
                    properties[p_name] = {
                        "type": p_type,
                        "description": p_desc
                    }
                    if param.get("required"):
                        required.append(p_name)

                req_body = op.get("requestBody", {})
                content = req_body.get("content", {})
                json_content = content.get("application/json", {})
                body_schema = json_content.get("schema", {})
                if body_schema:
                    if body_schema.get("type") == "object" and "properties" in body_schema:
                        for bp_name, bp_spec in body_schema.get("properties", {}).items():
                            properties[bp_name] = {
                                "type": bp_spec.get("type", "string"),
                                "description": bp_spec.get("description", "")
                            }
                        for r in body_schema.get("required", []):
                            if r not in required:
                                required.append(r)
                    else:
                        properties["body"] = {
                            "type": body_schema.get("type", "object"),
                            "description": "Request payload body"
                        }
                        if req_body.get("required"):
                            required.append("body")

                tool_def = {
                    "name": op_id,
                    "description": summary,
                    "endpoint": {"path": path, "method": method.upper()},
                    "inputSchema": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
                tools.append(tool_def)

        return {
            "total_tools": len(tools),
            "tools": tools,
            "diagnostics": {
                "endpoints_processed": endpoints_processed,
                "api_title": spec.get("info", {}).get("title", "OpenAPI Spec")
            }
        }
