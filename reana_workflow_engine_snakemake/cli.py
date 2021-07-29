# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2021 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA-Workflow-Engine-Snakemake command line interface."""


import logging
import os

from reana_commons.config import (
    REANA_LOG_FORMAT,
    REANA_LOG_LEVEL,
    REANA_WORKFLOW_UMASK,
    SHARED_VOLUME_PATH,
)
from reana_commons.workflow_engine import create_workflow_engine_command

from reana_workflow_engine_snakemake.config import LOGGING_MODULE
from reana_workflow_engine_snakemake.executor import run_jobs


logging.basicConfig(level=REANA_LOG_LEVEL, format=REANA_LOG_FORMAT)
log = logging.getLogger(LOGGING_MODULE)


def run_snakemake_workflow_engine_adapter(
    publisher,
    rjc_api_client,
    workflow_uuid=None,
    workflow_workspace=None,
    workflow_file=None,
    workflow_parameters=None,
    operational_options={},
    **kwargs,
):
    """Run a ``snakemake`` workflow."""
    workflow_workspace = "{0}/{1}".format(SHARED_VOLUME_PATH, workflow_workspace)
    # use some shared object between tasks.
    os.environ["workflow_uuid"] = workflow_uuid
    os.environ["workflow_workspace"] = workflow_workspace
    os.umask(REANA_WORKFLOW_UMASK)

    log.info("Snakemake workflows are not yet supported. Skipping...")
    log.info(f"Workflow spec received: {workflow_file}")
    publisher.publish_workflow_status(workflow_uuid, 1)
    run_jobs(rjc_api_client, workflow_workspace, workflow_file, workflow_parameters)
    publisher.publish_workflow_status(workflow_uuid, 2)


run_snakemake_workflow = create_workflow_engine_command(
    run_snakemake_workflow_engine_adapter, engine_type="snakemake"
)
