# WebCodeTool

Custom web agentic coding server with FastAPI and MCP (Model Context Protocol) support.

## Features

- 🚀 **FastAPI-based Server**: High-performance async web server
- 🤖 **Agent Orchestration**: Manage AI agent workflows with tool execution
- 🔧 **Built-in Tools**: File operations, code execution, web fetching
- 📡 **MCP Support**: Model Context Protocol compatible tool definitions
- 🌊 **Streaming Responses**: Real-time agent execution feedback
- 🔒 **Safe Execution**: Sandboxed code execution with timeouts

## Architecture

```
WebCodeTool
├── Agent Controller    → Orchestrates agent workflows
├── Tool Registry      → Manages available tools (MCP compatible)
├── Built-in Tools     → File ops, code execution, web requests
└── FastAPI Server     → RESTful API with streaming support
```

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using development mode

```bash
pip install -e .
```

## Quick Start

### Start the Server

```bash
# Using Python module
python -m webcodetool

# Or using uvicorn directly
uvicorn webcodetool.main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### Access API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health & Info

- `GET /` - Root endpoint with server info
- `GET /health` - Health check endpoint
- `GET /config` - Get current configuration

### Tools

- `GET /tools` - List all available tools
- `GET /tools/schemas` - Get tool schemas in MCP format
- `POST /tools/{tool_name}` - Execute a specific tool directly

### Agent Execution

- `POST /agent/execute` - Execute an agent task (non-streaming)
- `POST /agent/execute/stream` - Execute with streaming responses (Server-Sent Events)

## Built-in Tools

### File Operations
- **read_file**: Read contents of a file
- **write_file**: Write content to a file
- **list_files**: List files and directories

### Code Execution
- **execute_python**: Execute Python code in a subprocess
- **execute_shell**: Execute shell commands

### Web Operations
- **fetch_url**: Fetch content from a URL (GET/POST)

## Usage Examples

### Example 1: List Available Tools

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("http://localhost:8000/tools")
    print(response.json())
```

### Example 2: Execute a Tool Directly

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/tools/list_files",
        json={"directory": "."}
    )
    print(response.json())
```

### Example 3: Execute an Agent Task

```python
import httpx

agent_request = {
    "task": "List files in the current directory",
    "max_iterations": 5,
    "stream": False
}

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/agent/execute",
        json=agent_request
    )
    print(response.json())
```

### Example 4: Streaming Agent Execution

```python
import httpx
import json

agent_request = {
    "task": "Execute some Python code",
    "max_iterations": 5,
    "stream": True
}

async with httpx.AsyncClient() as client:
    async with client.stream(
        "POST",
        "http://localhost:8000/agent/execute/stream",
        json=agent_request
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                event = json.loads(line[6:])
                print(event)
```

## Example Scripts

The `examples/` directory contains ready-to-run examples:

```bash
# Basic client example
python examples/client_example.py

# Streaming example
python examples/streaming_example.py
```

## Configuration

Configuration can be set via environment variables or a `.env` file:

```bash
# Server settings
HOST=0.0.0.0
PORT=8000
RELOAD=false

# Agent settings
MAX_ITERATIONS=10
TIMEOUT=300

# Code execution settings
ENABLE_CODE_EXECUTION=true
CODE_EXECUTION_TIMEOUT=30

# Optional API keys
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

## MCP (Model Context Protocol) Integration

WebCodeTool implements MCP-compatible tool definitions. Tools can be accessed in MCP format:

```bash
curl http://localhost:8000/tools/schemas
```

This returns tool schemas that can be used with MCP-compatible clients like Claude Desktop or other AI agents.

## Development

### Project Structure

```
WebCodeTool/
├── webcodetool/
│   ├── __init__.py
│   ├── __main__.py         # Entry point
│   ├── main.py             # FastAPI application
│   ├── config.py           # Configuration management
│   ├── agent/              # Agent orchestration
│   │   ├── controller.py   # Agent controller
│   │   └── models.py       # Data models
│   ├── mcp/                # Model Context Protocol
│   │   └── registry.py     # Tool registry
│   └── tools/              # Built-in tools
│       └── builtin.py      # Tool implementations
├── examples/               # Example scripts
├── tests/                  # Test suite
├── pyproject.toml          # Project metadata
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=webcodetool
```

### Code Formatting

```bash
# Format code with black
black webcodetool/

# Lint with ruff
ruff check webcodetool/
```

## Security Considerations

⚠️ **Important Security Notes:**

- **Code Execution Tools**: The `execute_python` and `execute_shell` tools run code in subprocesses with timeout limits but without full sandboxing. These tools should only be used in trusted, controlled environments.
- **Production Deployment**: For production use:
  - Run the server in isolated containers (Docker/Kubernetes)
  - Implement authentication and authorization
  - Disable code execution tools if not needed (set `ENABLE_CODE_EXECUTION=false`)
  - Configure CORS with specific allowed origins
  - Use reverse proxies with rate limiting
- **File Operations**: File operations are restricted to the working directory to prevent path traversal attacks
- **Network Access**: The `fetch_url` tool has basic timeout protection but no URL filtering

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source. Add your license here.

## Roadmap

- [ ] LLM integration (OpenAI, Anthropic, local models)
- [ ] Enhanced security and sandboxing
- [ ] Database integration for agent memory
- [ ] Authentication and authorization
- [ ] More built-in tools
- [ ] WebSocket support for bidirectional communication
- [ ] Plugin system for custom tools

## Support

For issues, questions, or contributions, please open an issue on GitHub.