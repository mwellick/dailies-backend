ARG PYTHON_VERSION=3.13
ARG UV_VERSION=0.11.6

# Build stage
FROM ghcr.io/astral-sh/uv:${UV_VERSION} as uv
FROM python:${PYTHON_VERSION}-slim AS builder
COPY --from=uv /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /dailies

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-install-project --no-dev

COPY . /dailies
RUN uv sync --frozen --no-cache --no-dev

# Run stage
FROM python:${PYTHON_VERSION}-slim AS run

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/dailies/.venv/bin:$PATH"

# Run as non-root user and copy app from builder
RUN useradd -m -u 1000 dailies
WORKDIR /dailies
COPY --from=builder --chown=dailies:dailies /dailies .
USER dailies

EXPOSE 8000

# Run the application.
CMD ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
