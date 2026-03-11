# wellx3 dev environment
# Base: Debian slim — uv manages Python + all dependencies

FROM debian:bookworm-slim

# System deps: Java (cb2xml), Chrome (Selenium), curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless \
    unzip \
    curl \
    gnupg \
    && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install Python 3.12 via uv
RUN uv python install 3.12

# Set up working directory
WORKDIR /wellx3

# Install Python dependencies from lockfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Install cb2xml from local zip
COPY cb2xml_1.01.6.zip /tmp/cb2xml.zip
RUN mkdir -p /opt/cb2xml \
    && unzip /tmp/cb2xml.zip -d /opt/cb2xml \
    && rm /tmp/cb2xml.zip

# Wrapper script to invoke cb2xml
RUN printf '#!/bin/sh\njava -cp /opt/cb2xml/lib/cb2xml.jar:/opt/cb2xml/lib/cb2xml_definitions.jar net.sf.cb2xml.CopyBookAnalyzer "$@"\n' \
    > /usr/local/bin/cb2xml && chmod +x /usr/local/bin/cb2xml

# Kaggle credentials: mount at runtime via -v ~/.kaggle:/root/.kaggle:ro
# or set KAGGLE_USERNAME and KAGGLE_KEY env vars

CMD ["bash"]
