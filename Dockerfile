# This file is part of REANA.
# Copyright (C) 2021, 2022, 2023 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Use Ubuntu LTS base image
FROM docker.io/library/ubuntu:20.04

# Use default answers in installation commands
ENV DEBIAN_FRONTEND=noninteractive

# Prepare list of Python dependencies
COPY requirements.txt /code/

# Install all system and Python dependencies in one go
# hadolint ignore=DL3008, DL3009, DL3013, DL4006
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        cmake \
        curl \
        g++ \
        gcc \
        gnupg2 \
        graphviz \
        graphviz-dev \
        krb5-config \
        krb5-user \
        libauthen-krb5-perl \
        libkrb5-dev \
        libssl-dev \
        make \
        pkg-config \
        python3-dev \
        python3-pip \
        python3.8 \
        uuid-dev \
        vim-tiny && \
    # Install xrootd
    echo "deb [arch=amd64] http://storage-ci.web.cern.ch/storage-ci/debian/xrootd/ focal release" | tee -a /etc/apt/sources.list.d/xrootd.list && \
    curl -sL http://storage-ci.web.cern.ch/storage-ci/storageci.key | apt-key add - && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        libxrootd-client-dev \
        xrootd-client && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/requirements.txt && \
    apt-get remove -y \
        cmake \
        g++ \
        gcc \
        graphviz-dev \
        libssl-dev \
        make \
        pkg-config \
        python3-dev \
        uuid-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy cluster component source code
WORKDIR /code
COPY . /code

# Are we debugging?
ARG DEBUG=0
# hadolint ignore=DL3013
RUN if [ "${DEBUG}" -gt 0 ]; then pip install -e ".[debug,xrootd]"; else pip install ".[xrootd]"; fi;

# Are we building with locally-checked-out shared modules?
# hadolint ignore=SC2102
RUN if test -e modules/reana-commons; then pip install -e modules/reana-commons[kubernetes] --upgrade; fi

# Check for any broken Python dependencies
RUN pip check

# Set useful environment variables
ENV TERM=xterm \
    PYTHONPATH=/workdir
