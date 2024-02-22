# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2021, 2022 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA Workflow Engine Snakemake configuration."""

from distutils.util import strtobool
import os
from enum import Enum

MOUNT_CVMFS = os.getenv("REANA_MOUNT_CVMFS", "false")

WORKFLOW_KERBEROS = bool(strtobool(os.getenv("REANA_WORKFLOW_KERBEROS", "false")))
"""Whether Kerberos is needed for the whole workflow."""

LOGGING_MODULE = "reana-workflow-engine-snakemake"
"""REANA Workflow Engine Snakemake logging module."""

DEFAULT_SNAKEMAKE_REPORT_FILENAME = "report.html"
"""Snakemake report default filename."""

SNAKEMAKE_MAX_PARALLEL_JOBS = int(os.getenv("SNAKEMAKE_MAX_PARALLEL_JOBS", "300"))
"""Snakemake maximum number of jobs that can run in parallel."""

POLL_JOBS_STATUS_SLEEP_IN_SECONDS = 10
"""Time to sleep between polling for job status."""


# defined in reana-db component, in reana_db/models.py file as JobStatus
class JobStatus(Enum):
    """Enumeration of job statuses.

    Example:
        JobStatus.started.name == "started"  # True
    """

    # FIXME: this state is not defined in reana-db but returned by r-job-controller
    started = 6

    created = 0
    running = 1
    finished = 2
    failed = 3
    stopped = 4
    queued = 5


# defined in reana-db component, in reana_db/models.py file as RunStatus
class RunStatus(Enum):
    """Enumeration of possible run statuses of a workflow."""

    created = 0
    running = 1
    finished = 2
    failed = 3
    deleted = 4
    stopped = 5
    queued = 6
    pending = 7
