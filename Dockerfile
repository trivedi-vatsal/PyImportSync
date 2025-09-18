FROM python:3.11-slim

# Set metadata
LABEL maintainer="trivedi-vatsal"
LABEL description="GitHub Action for synchronizing Python imports with requirements.txt"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /action

# Copy requirements first for better caching
COPY requirements.txt /action/

# Install Python dependencies
RUN pip install --no-cache-dir \
    pipreqs==0.4.13 \
    packaging \
    && pip install --no-cache-dir -r /action/requirements.txt

# Copy the action files
COPY src/ /action/src/
COPY entrypoint.sh /action/

# Make entrypoint executable
RUN chmod +x /action/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/action/entrypoint.sh"]