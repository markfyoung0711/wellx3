# wellx3 dev environment
# Base: small Debian image with Python + Java for cb2xml + Jupyter + Kaggle CLI

FROM python:3.12-slim

# Install Java (for cb2xml) and minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python tools: Jupyter, Kaggle CLI, data science stack
RUN pip install --no-cache-dir \
    kaggle \
    jupyter \
    jupyterlab \
    pandas \
    numpy \
    geopandas \
    scikit-learn \
    xgboost \
    matplotlib \
    lxml

# Set up working directory
WORKDIR /wellx3

# Install cb2xml from local zip (zip extracts flat, no top-level folder)
COPY cb2xml_1.01.6.zip /tmp/cb2xml.zip
RUN mkdir -p /opt/cb2xml \
    && unzip /tmp/cb2xml.zip -d /opt/cb2xml \
    && rm /tmp/cb2xml.zip

# Wrapper script to invoke cb2xml
RUN printf '#!/bin/sh\njava -cp /opt/cb2xml/lib/cb2xml.jar:/opt/cb2xml/lib/cb2xml_definitions.jar net.sf.cb2xml.CopyBookAnalyzer "$@"\n' \
    > /usr/local/bin/cb2xml && chmod +x /usr/local/bin/cb2xml

# Kaggle credentials: mount at runtime via -v ~/.kaggle:/root/.kaggle:ro
# or set KAGGLE_USERNAME and KAGGLE_KEY env vars

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--notebook-dir=/wellx3"]
