"""Tests for built-in tools."""

import pytest
import tempfile
import os
from pathlib import Path

from webcodetool.tools.builtin import (
    read_file,
    write_file,
    list_files,
    execute_python,
    execute_shell
)


@pytest.mark.asyncio
async def test_write_and_read_file():
    """Test writing and reading a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.txt")
        content = "Hello, World!"
        
        # Write file
        result = await write_file(file_path, content)
        assert "Successfully" in result
        
        # Read file
        result = await read_file(file_path)
        assert result == content


@pytest.mark.asyncio
async def test_read_nonexistent_file():
    """Test reading a non-existent file."""
    result = await read_file("/nonexistent/file.txt")
    assert "Error" in result


@pytest.mark.asyncio
async def test_list_files():
    """Test listing files in a directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some test files
        Path(tmpdir, "file1.txt").touch()
        Path(tmpdir, "file2.txt").touch()
        os.makedirs(os.path.join(tmpdir, "subdir"))
        
        result = await list_files(tmpdir)
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "subdir" in result


@pytest.mark.asyncio
async def test_execute_python():
    """Test executing Python code."""
    code = "print('Hello from Python')"
    result = await execute_python(code)
    assert "Hello from Python" in result


@pytest.mark.asyncio
async def test_execute_python_with_error():
    """Test executing Python code with error."""
    code = "raise ValueError('test error')"
    result = await execute_python(code)
    assert "test error" in result or "Stderr" in result


@pytest.mark.asyncio
async def test_execute_shell():
    """Test executing shell command."""
    result = await execute_shell("echo 'Hello from shell'")
    assert "Hello from shell" in result


@pytest.mark.asyncio
async def test_execute_python_timeout():
    """Test Python execution timeout."""
    code = "import time; time.sleep(10)"
    result = await execute_python(code, timeout=1)
    assert "timeout" in result.lower()
