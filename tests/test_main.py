"""Tests for WebCodeTool."""

import pytest
from fastapi.testclient import TestClient

from webcodetool.main import app
from webcodetool.mcp import tool_registry
from webcodetool.tools import register_builtin_tools


@pytest.fixture
def client():
    """Create test client."""
    # Ensure tools are registered for testing
    register_builtin_tools()
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "WebCodeTool"
    assert data["status"] == "active"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_tools(client):
    """Test listing tools."""
    response = client.get("/tools")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "tools" in data
    assert data["count"] > 0
    assert len(data["tools"]) == data["count"]


def test_tool_schemas(client):
    """Test getting tool schemas."""
    response = client.get("/tools/schemas")
    assert response.status_code == 200
    data = response.json()
    assert "schemas" in data
    assert len(data["schemas"]) > 0


def test_execute_tool_list_files(client):
    """Test executing list_files tool."""
    response = client.post(
        "/tools/list_files",
        json={"directory": "."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["tool"] == "list_files"
    assert "result" in data


def test_execute_tool_not_found(client):
    """Test executing non-existent tool."""
    response = client.post(
        "/tools/nonexistent_tool",
        json={}
    )
    assert response.status_code == 404


def test_agent_execute(client):
    """Test agent execution."""
    request = {
        "task": "Test task",
        "max_iterations": 2,
        "stream": False
    }
    response = client.post("/agent/execute", json=request)
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "final_response" in data
    assert "iterations" in data


def test_get_config(client):
    """Test getting configuration."""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "max_iterations" in data
    assert "timeout" in data
    assert "enable_code_execution" in data
