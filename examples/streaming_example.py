#!/usr/bin/env python3
"""Example of using the streaming agent endpoint."""

import httpx
import json
import asyncio


async def stream_agent_task():
    """Demonstrate streaming agent execution."""
    base_url = "http://localhost:8000"
    
    agent_request = {
        "task": "Check if Python is available and execute a simple calculation",
        "max_iterations": 5,
        "stream": True
    }
    
    print("=== Streaming Agent Execution ===\n")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream(
            "POST",
            f"{base_url}/agent/execute/stream",
            json=agent_request
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    event_type = data.get("type")
                    
                    if event_type == "start":
                        print(f"🚀 Starting agent (max {data['max_iterations']} iterations)")
                    elif event_type == "iteration":
                        print(f"\n📍 Iteration {data['number']}")
                    elif event_type == "thought":
                        print(f"💭 Thought: {data['content']}")
                    elif event_type == "tool_call":
                        print(f"🔧 Calling tool: {data['name']}")
                        print(f"   Parameters: {data['parameters']}")
                    elif event_type == "tool_result":
                        print(f"✅ Tool result from {data['name']}:")
                        print(f"   {data['result'][:200]}...")
                    elif event_type == "tool_error":
                        print(f"❌ Tool error in {data['name']}: {data['error']}")
                    elif event_type == "response":
                        print(f"\n💬 Final Response: {data['content']}")
                    elif event_type == "done":
                        print(f"\n✨ Completed in {data['iterations']} iterations")
                    elif event_type == "error":
                        print(f"❌ Error: {data['message']}")


if __name__ == "__main__":
    print("WebCodeTool Streaming Example\n")
    print("Make sure the server is running on http://localhost:8000\n")
    asyncio.run(stream_agent_task())
