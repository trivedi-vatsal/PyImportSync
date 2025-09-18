FROM python:3.11-slim

# Set metadata
LABEL maintainer="trivedi-vatsal"
LABEL description="GitHub Action for synchronizing Python imports with requirements.txt"

# Install system dependencies and UV in a single layer
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.cargo/bin/uv /usr/local/bin/uv

# Set working directory
WORKDIR /action

# Copy requirements first for better caching
COPY requirements.txt /action/

# Install Python dependencies using UV (much faster than pip)
RUN uv pip install --system --no-cache \
    pipreqs==0.4.13 \
    packaging \
    && uv pip install --system --no-cache -r /action/requirements.txt

# Copy the action files
COPY src/ /action/src/
COPY entrypoint.sh /action/

# Make entrypoint executable
RUN chmod +x /action/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/action/entrypoint.sh"]