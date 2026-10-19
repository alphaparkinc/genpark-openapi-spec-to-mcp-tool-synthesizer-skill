"""Example usage for OpenAPI Spec to MCP Tool Synthesizer."""
from client import OpenApiSpecToMcpToolSynthesizer
import json

spec = {
    "openapi": "3.0.0",
    "info": {"title": "Payment Gateway API", "version": "1.0.0"},
    "paths": {
        "/v1/charges": {
            "post": {
                "operationId": "create_charge",
                "summary": "Create credit card charge",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": "integer", "description": "Amount in cents"},
                                    "currency": {"type": "string", "description": "3-letter currency"}
                                },
                                "required": ["amount", "currency"]
                            }
                        }
                    }
                }
            }
        }
    }
}

result = OpenApiSpecToMcpToolSynthesizer.synthesize_tools(spec)
print(json.dumps(result, indent=2))
