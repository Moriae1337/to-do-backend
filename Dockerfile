FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

WORKDIR /app

# copy only deps to use layer caching 
COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY . /app

# load .env for pydantic BaseSettings.
ENV ENV_FILE=.env
# Logs > stdout
ENV PYTHONUNBUFFERED=1

ENV PATH="/app/.venv/bin:$PATH"

# Without sh -c, Docker would treat ${HOST} literally, not as a variable
CMD ["sh","-c","uv alembic upgrade head && uv uvicorn app.main:app --host ${HOST} --port ${PORT}"]