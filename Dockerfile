# WebCodeTool Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webcodetool/ ./webcodetool/
COPY pyproject.toml .
COPY README.md .

# Install the package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000

# Run the application
CMD ["python", "-m", "webcodetool"]
