FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync --no-cache-dir
COPY . .

CMD ["uv", "run", "core/pipeline/main.py"]
