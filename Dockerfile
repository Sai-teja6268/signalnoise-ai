FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

# Copy only dependency definitions first to maximize Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project itself
RUN uv sync --no-install-project

# Copy the rest of the application
COPY . .

# Final sync to install the project
RUN uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "--app-dir", "src", "signalnoise.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
