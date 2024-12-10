FROM python:3.13-slim as build-python

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/code/.venv

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/
COPY pyproject.toml uv.lock /_lock/
RUN --mount=type=cache,target=/root/.cache \
    cd /_lock && \
    uv sync \
      --frozen \
      --no-group dev \
      --group prod

FROM python:3.13-slim
WORKDIR /opt/app
COPY --from=build-python /code /code
ENV PATH="/code/.venv/bin:$PATH"
COPY . /opt/app
