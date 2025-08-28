## ------------------------------- Builder Stage ------------------------------ ## 
FROM python:3.13-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
# RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY ./pyproject.toml uv.lock* /app/

RUN uv sync --frozen

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.13-slim-bookworm AS production

WORKDIR /app

COPY . .
COPY --from=builder /app/.venv .venv

# Set up environment variables for production
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]