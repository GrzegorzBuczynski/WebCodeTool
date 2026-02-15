"""Tests for tool registry."""

import pytest
from webcodetool.mcp import Tool, ToolParameter, ToolRegistry


@pytest.fixture
def registry():
    """Create a fresh tool registry."""
    return ToolRegistry()


async def dummy_handler(**kwargs):
    """Dummy tool handler."""
    return "dummy result"


def test_register_tool(registry):
    """Test registering a tool."""
    tool = Tool(
        name="test_tool",
        description="A test tool",
        parameters=[
            ToolParameter(name="param1", type="string", description="Test param")
        ],
        handler=dummy_handler
    )
    
    registry.register(tool)
    assert registry.get_tool("test_tool") is not None


def test_list_tools(registry):
    """Test listing tools."""
    tool1 = Tool(name="tool1", description="Tool 1", handler=dummy_handler)
    tool2 = Tool(name="tool2", description="Tool 2", handler=dummy_handler)
    
    registry.register(tool1)
    registry.register(tool2)
    
    tools = registry.list_tools()
    assert len(tools) == 2


def test_get_tool_schemas(registry):
    """Test getting tool schemas."""
    tool = Tool(
        name="test_tool",
        description="A test tool",
        parameters=[
            ToolParameter(name="param1", type="string", description="Param 1", required=True),
            ToolParameter(name="param2", type="integer", description="Param 2", required=False)
        ],
        handler=dummy_handler
    )
    
    registry.register(tool)
    schemas = registry.get_tool_schemas()
    
    assert len(schemas) == 1
    assert schemas[0]["name"] == "test_tool"
    assert "parameters" in schemas[0]
    assert "param1" in schemas[0]["parameters"]["properties"]


@pytest.mark.asyncio
async def test_execute_tool(registry):
    """Test executing a tool."""
    async def test_handler(value: str):
        return f"Result: {value}"
    
    tool = Tool(
        name="test_tool",
        description="A test tool",
        parameters=[
            ToolParameter(name="value", type="string", description="Value")
        ],
        handler=test_handler
    )
    
    registry.register(tool)
    result = await registry.execute_tool("test_tool", {"value": "hello"})
    assert result == "Result: hello"


@pytest.mark.asyncio
async def test_execute_nonexistent_tool(registry):
    """Test executing a non-existent tool."""
    with pytest.raises(ValueError, match="not found"):
        await registry.execute_tool("nonexistent", {})
