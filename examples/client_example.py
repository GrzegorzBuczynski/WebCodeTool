#!/usr/bin/env python3
"""Example client for interacting with WebCodeTool server."""

import asyncio
import httpx
import json


async def main():
    """Run example interactions with the server."""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # 1. Check server health
        print("=== Checking Server Health ===")
        response = await client.get(f"{base_url}/health")
        print(f"Status: {response.json()}")
        print()
        
        # 2. List available tools
        print("=== Available Tools ===")
        response = await client.get(f"{base_url}/tools")
        tools_data = response.json()
        print(f"Total tools: {tools_data['count']}")
        for tool in tools_data['tools']:
            print(f"  - {tool['name']}: {tool['description']}")
        print()
        
        # 3. Execute a tool directly
        print("=== Executing 'list_files' Tool ===")
        response = await client.post(
            f"{base_url}/tools/list_files",
            json={"directory": "."}
        )
        result = response.json()
        print(f"Result:\n{result['result']}")
        print()
        
        # 4. Execute an agent task
        print("=== Executing Agent Task ===")
        agent_request = {
            "task": "List the files in the current directory and tell me about this project",
            "max_iterations": 5,
            "stream": False
        }
        response = await client.post(
            f"{base_url}/agent/execute",
            json=agent_request
        )
        agent_response = response.json()
        print(f"Success: {agent_response['success']}")
        print(f"Iterations: {agent_response['iterations']}")
        print(f"Final Response: {agent_response['final_response']}")
        print()
        
        # 5. Get tool schemas (MCP format)
        print("=== Tool Schemas (MCP Format) ===")
        response = await client.get(f"{base_url}/tools/schemas")
        schemas = response.json()
        print(f"Available schemas: {len(schemas['schemas'])}")
        if schemas['schemas']:
            first_schema = schemas['schemas'][0]
            print(f"Example schema for '{first_schema['name']}':")
            print(json.dumps(first_schema, indent=2))


if __name__ == "__main__":
    print("WebCodeTool Example Client\n")
    print("Make sure the server is running on http://localhost:8000\n")
    asyncio.run(main())
