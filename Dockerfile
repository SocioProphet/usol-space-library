# Minimal dev image (no GPUs required)
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl \
    libcfitsio-dev libatlas-base-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /workspace
RUN pip install -e .

CMD ["bash"]
