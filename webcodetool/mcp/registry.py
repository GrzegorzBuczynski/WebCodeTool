"""Tool registry for the agentic coding server."""

from typing import Dict, Any, Callable, List, Optional
from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    """Tool parameter definition."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None


class Tool(BaseModel):
    """Tool definition compatible with MCP protocol."""
    name: str
    description: str
    parameters: List[ToolParameter] = Field(default_factory=list)
    handler: Optional[Callable] = Field(default=None, exclude=True)
    
    model_config = {"arbitrary_types_allowed": True}


class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a new tool."""
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[Tool]:
        """List all registered tools."""
        return list(self._tools.values())
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get tool schemas in MCP format."""
        schemas = []
        for tool in self._tools.values():
            schema = {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            
            for param in tool.parameters:
                schema["parameters"]["properties"][param.name] = {
                    "type": param.type,
                    "description": param.description
                }
                if param.required:
                    schema["parameters"]["required"].append(param.name)
            
            schemas.append(schema)
        
        return schemas
    
    async def execute_tool(self, name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool with given parameters."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        
        if not tool.handler:
            raise ValueError(f"Tool '{name}' has no handler")
        
        return await tool.handler(**parameters)


# Global tool registry instance
tool_registry = ToolRegistry()
