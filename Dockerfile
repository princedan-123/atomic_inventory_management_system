FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /atomic_inventory_management_system
WORKDIR /atomic_inventory_management_system
RUN pip install -r ./atomic_inventory/requirement.txt