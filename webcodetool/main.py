"""Main FastAPI application for WebCodeTool agentic coding server."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any

from .agent import AgentController, AgentRequest, AgentResponse
from .mcp import tool_registry
from .tools import register_builtin_tools
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup: Register built-in tools
    register_builtin_tools()
    yield
    # Shutdown: cleanup if needed


# Create FastAPI app
app = FastAPI(
    title="WebCodeTool",
    description="Custom web agentic coding server with FastAPI and MCP support",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
# Note: Configure allow_origins with specific domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Set to False when allowing all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent controller
agent_controller = AgentController()


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "name": "WebCodeTool",
        "version": "0.1.0",
        "description": "Custom web agentic coding server",
        "status": "active"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/tools")
async def list_tools() -> Dict[str, Any]:
    """List all available tools."""
    tools = tool_registry.list_tools()
    return {
        "count": len(tools),
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "description": p.description,
                        "required": p.required,
                        "default": p.default
                    }
                    for p in tool.parameters
                ]
            }
            for tool in tools
        ]
    }


@app.get("/tools/schemas")
async def get_tool_schemas() -> Dict[str, Any]:
    """Get tool schemas in MCP format."""
    return {
        "schemas": tool_registry.get_tool_schemas()
    }


@app.post("/agent/execute")
async def execute_agent(request: AgentRequest) -> AgentResponse:
    """Execute an agent task."""
    try:
        if request.stream:
            raise HTTPException(
                status_code=400,
                detail="Use /agent/execute/stream endpoint for streaming responses"
            )
        
        response = await agent_controller.execute(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/execute/stream")
async def execute_agent_stream(request: AgentRequest):
    """Execute an agent task with streaming responses."""
    try:
        return StreamingResponse(
            agent_controller.execute_stream(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/{tool_name}")
async def execute_tool(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a specific tool directly."""
    try:
        result = await tool_registry.execute_tool(tool_name, parameters)
        return {
            "success": True,
            "tool": tool_name,
            "result": result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Get current server configuration."""
    return {
        "max_iterations": settings.max_iterations,
        "timeout": settings.timeout,
        "enable_code_execution": settings.enable_code_execution,
        "code_execution_timeout": settings.code_execution_timeout
    }
