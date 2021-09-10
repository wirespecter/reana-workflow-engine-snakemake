# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2021 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA Workflow Engine Snakemake configuration."""

import os

MOUNT_CVMFS = os.getenv("REANA_MOUNT_CVMFS", "false")

LOGGING_MODULE = "reana-workflow-engine-snakemake"
"""REANA Workflow Engine Snakemake logging module."""

DEFAULT_SNAKEMAKE_REPORT_FILENAME = "report.html"
"""Snakemake report default filename."""
