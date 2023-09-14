# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2021 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA-Workflow-Engine-Snakemake utilities."""

from reana_commons.publisher import WorkflowStatusPublisher
from reana_commons.utils import build_progress_message
from snakemake.jobs import Job


def publish_workflow_start(
    workflow_uuid: str, publisher: WorkflowStatusPublisher, job: Job
):
    """Publish to MQ the start of the workflow."""
    job_count = len(
        [j for j in (job.dag._needrun | job.dag._finished) if not j.rule.norun]
    )
    total_jobs = {"total": job_count, "job_ids": []}
    status_running = 1
    publisher.publish_workflow_status(
        workflow_uuid,
        status=status_running,
        message={"progress": build_progress_message(total=total_jobs)},
    )


def publish_job_submission(
    workflow_uuid: str, publisher: WorkflowStatusPublisher, reana_job_id: str
):
    """Publish to MQ the job submission."""
    running_jobs = {"total": 1, "job_ids": [reana_job_id]}
    status_running = 1
    publisher.publish_workflow_status(
        workflow_uuid,
        status=status_running,
        message={"progress": build_progress_message(running=running_jobs)},
    )
