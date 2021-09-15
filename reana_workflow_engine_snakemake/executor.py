# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2021 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA-Workflow-Engine-Snakemake executor."""

import os
import subprocess
import logging
from collections import namedtuple

from reana_commons.utils import build_progress_message
from snakemake import snakemake
from snakemake.executors import ClusterExecutor, GenericClusterExecutor
from snakemake.logging import logger
from snakemake import scheduler  # for monkeypatch


from reana_workflow_engine_snakemake.config import (
    DEFAULT_SNAKEMAKE_REPORT_FILENAME,
    LOGGING_MODULE,
    MOUNT_CVMFS,
)


log = logging.getLogger(LOGGING_MODULE)


REANAClusterJob = namedtuple(
    "REANAClusterJob",
    "job jobid callback error_callback jobscript jobfinished jobfailed",
)


class REANAClusterExecutor(GenericClusterExecutor):
    """REANA Cluster Snakemake executor implementation."""

    def run(self, job, callback=None, submit_callback=None, error_callback=None):
        """Override GenericClusterExecutor run method."""
        super()._run(job)
        jobid = job.jobid

        # Files needed for Snakemake (`GenericClusterExecutor._wait_for_jobs`)
        # to check if a job finished successfully.
        jobscript = self.get_jobscript(job)
        jobfinished = os.path.join(self.tmpdir, "{}.jobfinished".format(jobid))
        jobfailed = os.path.join(self.tmpdir, "{}.jobfailed".format(jobid))
        self.write_jobscript(
            job, jobscript, jobfinished=jobfinished, jobfailed=jobfailed
        )

        workflow_workspace = os.getenv("workflow_workspace", "default")
        try:
            job.reana_job_id = None
            logger.info(f"Job '{job.name}' received, command: {job.shellcmd}")
            logger.info(f"Environment: {job.container_img_url}")
            if job.is_shell:
                # Shell command
                workflow_uuid = os.getenv("workflow_uuid", "default")
                job_request_body = {
                    "workflow_uuid": workflow_uuid,
                    "image": job.container_img_url.replace("docker://", ""),
                    "cmd": f"cd {workflow_workspace} && {job.shellcmd} && touch {jobfinished} || (touch {jobfailed}; exit 1)",
                    "prettified_cmd": job.shellcmd,
                    "workflow_workspace": workflow_workspace,
                    "job_name": job.name,
                    "cvmfs_mounts": MOUNT_CVMFS,
                    "compute_backend": job.resources.get("compute_backend", ""),
                    "kerberos": job.resources.get("kerberos", False),
                    "unpacked_img": job.resources.get("unpacked_img", False),
                    "kubernetes_uid": job.resources.get("kubernetes_uid"),
                    "kubernetes_memory_limit": job.resources.get(
                        "kubernetes_memory_limit"
                    ),
                    "voms_proxy": job.resources.get("voms_proxy", False),
                    "htcondor_max_runtime": job.resources.get(
                        "htcondor_max_runtime", ""
                    ),
                    "htcondor_accounting_group": job.resources.get(
                        "htcondor_accounting_group", ""
                    ),
                }
                job_id = submit_job(
                    self.rjc_api_client, self.publisher, job_request_body
                )
                job.reana_job_id = job_id
                self.workflow.persistence.started(job, external_jobid=job.reana_job_id)
            elif job.is_run:
                # Python code
                logger.error("Python code execution is not supported yet.")

        except Exception as excep:
            logger.error(f"Error submitting job {job.name}: {excep}")
            error_callback(job)
            return
        # We don't need to call `submit_callback(job)` manually since
        # it would immediately check if the output files are present
        # and fail otherwise (3 sec timeout).

        if job.is_norun:
            job_id = "all"
            # Manually create the jobfinished for the root rule (`all`)
            # to mark it as successful.
            try:
                subprocess.check_output(
                    f"touch {jobfinished}", shell=True,
                )
            except subprocess.CalledProcessError as ex:
                logger.error(
                    "Error creating `all` jobfinished file (exit code {}):\n{}".format(
                        ex.returncode, ex.output.decode()
                    )
                )
                error_callback(job)
                return
        with self.lock:
            self.active_jobs.append(
                REANAClusterJob(
                    job,
                    job_id,
                    callback,
                    error_callback,
                    jobscript,
                    jobfinished,
                    jobfailed,
                )
            )

    def _handle_job_status(self, job, status):
        workflow_uuid = os.getenv("workflow_uuid", "default")
        job_id = job.reana_job_id
        log.info(f"{status} job: {job_id}")
        message = {
            "progress": build_progress_message(
                **{status: {"total": 1, "job_ids": [job_id]}}
            )
        }
        status_running = 1
        status_failed = 3
        status_mapping = {"finished": status_running, "failed": status_failed}
        self.publisher.publish_workflow_status(
            workflow_uuid, status_mapping[status], message=message
        )

    def handle_job_success(self, job):
        """Override job success method to publish job status."""
        # override handle_touch = True, to enable `touch()` in Snakefiles
        super(ClusterExecutor, self).handle_job_success(
            job, upload_remote=False, handle_log=False, handle_touch=True
        )

        self._handle_job_status(job, "finished")

    def handle_job_error(self, job):
        """Override job error method to publish job status."""
        super().handle_job_error(job)

        self._handle_job_status(job, "failed")


def submit_job(rjc_api_client, publisher, job_request_body):
    """Submit job to REANA Job Controller."""
    response = rjc_api_client.submit(**job_request_body)
    job_id = str(response["job_id"])

    log.info("submitted job:{0}".format(job_id))
    message = {
        "progress": build_progress_message(running={"total": 1, "job_ids": [job_id]})
    }
    status_running = 1
    publisher.publish_workflow_status(
        job_request_body["workflow_uuid"], status_running, message=message
    )
    return job_id

    # FIXME: Call `job_status = poll_job_status(rjc_api_client, job_id)` instead of
    # checking job success/failure via `jobfinished`/`jobfailed` files in .snakemake?
    # In that case we would probably need to implement our own `_wait_for_jobs` method.


def run_jobs(
    rjc_api_client,
    publisher,
    workflow_workspace,
    workflow_file,
    workflow_parameters,
    operational_options={},
):
    """Run Snakemake jobs using custom REANA executor."""

    def _generate_report(workflow_file_path):
        """Generate HTML report."""
        success = snakemake(
            workflow_file_path,
            config=workflow_parameters,
            workdir=workflow_workspace,
            report=operational_options.get("report", DEFAULT_SNAKEMAKE_REPORT_FILENAME),
        )
        if not success:
            logger.error("Error generating workflow HTML report.")

    # Inject RJC API client and workflow status publisher in the REANA executor
    REANAClusterExecutor.rjc_api_client = rjc_api_client
    REANAClusterExecutor.publisher = publisher
    # Monkeypatch GenericClusterExecutor class in `scheduler` module
    scheduler.GenericClusterExecutor = REANAClusterExecutor

    workflow_file_path = os.path.join(workflow_workspace, workflow_file)
    success = snakemake(
        workflow_file_path,
        printshellcmds=True,
        # FIXME: Can be anything as it's not directly used. It's supposed
        # to be the shell command to submit to job e.g. `condor_q`,
        # but we call RJC API client instead.
        cluster="reana",
        config=workflow_parameters,
        workdir=workflow_workspace,
        notemp=True,
        nodes=4,  # enables DAG parallelization
    )
    # Once the workflow is finished, generate the report,
    # taking into account the metadata generated.
    _generate_report(workflow_file_path)
    return success
