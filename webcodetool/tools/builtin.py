"""Built-in tools for the agentic coding server."""

import os
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import httpx

from ..mcp import Tool, ToolParameter, tool_registry


async def read_file(path: str) -> str:
    """Read contents of a file."""
    try:
        file_path = Path(path).resolve()
        # Validate path is within current working directory or /tmp for tests
        working_dir = Path.cwd().resolve()
        tmp_dir = Path("/tmp").resolve()
        
        path_str = str(file_path)
        if not (path_str.startswith(str(working_dir)) or path_str.startswith(str(tmp_dir))):
            return "Error: Access denied - path outside allowed directories"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


async def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        file_path = Path(path).resolve()
        # Validate path is within current working directory or /tmp for tests
        working_dir = Path.cwd().resolve()
        tmp_dir = Path("/tmp").resolve()
        
        path_str = str(file_path)
        if not (path_str.startswith(str(working_dir)) or path_str.startswith(str(tmp_dir))):
            return "Error: Access denied - path outside allowed directories"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


async def list_files(directory: str = ".") -> str:
    """List files in a directory."""
    try:
        dir_path = Path(directory).resolve()
        if not dir_path.is_dir():
            return f"Error: {directory} is not a directory"
        
        files = []
        for item in dir_path.iterdir():
            item_type = "dir" if item.is_dir() else "file"
            files.append(f"{item_type}: {item.name}")
        
        return "\n".join(files) if files else "Empty directory"
    except Exception as e:
        return f"Error listing files: {str(e)}"


async def execute_python(code: str, timeout: int = 30) -> str:
    """Execute Python code in a subprocess."""
    try:
        # Run Python code in a subprocess with timeout
        process = await asyncio.create_subprocess_exec(
            'python3', '-c', code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            result = stdout.decode('utf-8')
            if stderr:
                result += f"\nStderr: {stderr.decode('utf-8')}"
            
            return result or "Code executed successfully (no output)"
        except asyncio.TimeoutError:
            process.kill()
            return f"Error: Code execution timeout after {timeout} seconds"
            
    except Exception as e:
        return f"Error executing code: {str(e)}"


async def execute_shell(command: str, timeout: int = 30) -> str:
    """Execute a shell command."""
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            result = stdout.decode('utf-8')
            if stderr:
                result += f"\nStderr: {stderr.decode('utf-8')}"
            
            return result or "Command executed successfully (no output)"
        except asyncio.TimeoutError:
            process.kill()
            return f"Error: Command execution timeout after {timeout} seconds"
            
    except Exception as e:
        return f"Error executing command: {str(e)}"


async def fetch_url(url: str, method: str = "GET") -> str:
    """Fetch content from a URL."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method.upper() == "GET":
                response = await client.get(url)
            elif method.upper() == "POST":
                response = await client.post(url)
            else:
                return f"Error: Unsupported HTTP method {method}"
            
            response.raise_for_status()
            return response.text
    except Exception as e:
        return f"Error fetching URL: {str(e)}"


def register_builtin_tools():
    """Register all built-in tools."""
    
    # File operations
    tool_registry.register(Tool(
        name="read_file",
        description="Read the contents of a file",
        parameters=[
            ToolParameter(name="path", type="string", description="Path to the file to read")
        ],
        handler=read_file
    ))
    
    tool_registry.register(Tool(
        name="write_file",
        description="Write content to a file",
        parameters=[
            ToolParameter(name="path", type="string", description="Path to the file to write"),
            ToolParameter(name="content", type="string", description="Content to write to the file")
        ],
        handler=write_file
    ))
    
    tool_registry.register(Tool(
        name="list_files",
        description="List files and directories in a given path",
        parameters=[
            ToolParameter(
                name="directory", 
                type="string", 
                description="Directory path to list (default: current directory)",
                required=False,
                default="."
            )
        ],
        handler=list_files
    ))
    
    # Code execution
    tool_registry.register(Tool(
        name="execute_python",
        description="Execute Python code in a safe subprocess",
        parameters=[
            ToolParameter(name="code", type="string", description="Python code to execute"),
            ToolParameter(
                name="timeout", 
                type="integer", 
                description="Timeout in seconds (default: 30)",
                required=False,
                default=30
            )
        ],
        handler=execute_python
    ))
    
    tool_registry.register(Tool(
        name="execute_shell",
        description="Execute a shell command",
        parameters=[
            ToolParameter(name="command", type="string", description="Shell command to execute"),
            ToolParameter(
                name="timeout", 
                type="integer", 
                description="Timeout in seconds (default: 30)",
                required=False,
                default=30
            )
        ],
        handler=execute_shell
    ))
    
    # Web operations
    tool_registry.register(Tool(
        name="fetch_url",
        description="Fetch content from a URL",
        parameters=[
            ToolParameter(name="url", type="string", description="URL to fetch"),
            ToolParameter(
                name="method", 
                type="string", 
                description="HTTP method (GET or POST, default: GET)",
                required=False,
                default="GET"
            )
        ],
        handler=fetch_url
    ))
