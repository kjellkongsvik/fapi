FROM python:3.13-slim AS build

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY . /app
WORKDIR /app

RUN uv sync --frozen --no-cache --no-dev

FROM python:3.13-slim

WORKDIR /app

COPY --from=build /app/.venv .venv
COPY fapi fapi
CMD ["/app/.venv/bin/fastapi", "run", "fapi", "--port", "8080"]
