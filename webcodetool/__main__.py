"""Entry point for running the WebCodeTool server."""

import uvicorn
from .config import settings


def main():
    """Run the FastAPI server."""
    uvicorn.run(
        "webcodetool.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
