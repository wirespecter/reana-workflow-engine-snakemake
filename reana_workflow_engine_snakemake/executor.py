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
from functools import partial
from collections import namedtuple

from snakemake import snakemake
from snakemake import logging
from snakemake.common import get_uuid
from snakemake.exceptions import WorkflowError
from snakemake.executors import GenericClusterExecutor
from snakemake.logging import logger
from snakemake import scheduler  # for monkeypatch


GenericClusterJob = namedtuple(
    "GenericClusterJob",
    "job jobid callback error_callback jobscript jobfinished jobfailed",
)


class REANAClusterExecutor(GenericClusterExecutor):
    """REANA Cluster Snakemake executor implementation."""

    def run(self, job, callback=None, submit_callback=None, error_callback=None):
        """."""
        # Override submit callback to enable `update_resources`
        submit_callback = partial(
            submit_callback.func,
            update_dynamic=False,
            print_progress=False,
            update_resources=True,
            handle_job_success=False,
        )

        super()._run(job)
        jobid = job.jobid

        jobscript = self.get_jobscript(job)
        jobfinished = os.path.join(self.tmpdir, "{}.jobfinished".format(jobid))
        jobfailed = os.path.join(self.tmpdir, "{}.jobfailed".format(jobid))
        # self.write_jobscript(
        #     job, jobscript, jobfinished=jobfinished, jobfailed=jobfailed
        # )

        envvars = " ".join(
            "{}={}".format(var, os.environ[var]) for var in self.workflow.envvars
        )

        exec_job = self.format_job(
            self.exec_job,
            job,
            _quote_all=True,
            use_threads="--force-use-threads" if not job.is_group() else "",
            jobfinished=jobfinished,
            jobfailed=jobfailed,
            envvars=envvars,
        )

        if self.statuscmd:
            ext_jobid = self.dag.incomplete_external_jobid(job)
            if ext_jobid:
                # Job is incomplete and still running.
                # We simply register it and wait for completion or failure.
                logger.info(
                    "Resuming incomplete job {} with external jobid '{}'.".format(
                        jobid, ext_jobid
                    )
                )
                submit_callback(job)
                with self.lock:
                    self.active_jobs.append(
                        GenericClusterJob(
                            job,
                            ext_jobid,
                            callback,
                            error_callback,
                            jobscript,
                            jobfinished,
                            jobfailed,
                        )
                    )
                return

        # deps = " ".join(
        #     self.external_jobid[f] for f in job.input if f in self.external_jobid
        # )
        # try:
        #     submitcmd = job.format_wildcards(
        #         self.submitcmd, dependencies=deps, cluster=self.cluster_wildcards(job)
        #     )
        # except AttributeError as e:
        #     raise WorkflowError(str(e), rule=job.rule if not job.is_group() else None)

        try:
            # TODO: Call rjc_api_client
            logger.info(f"Job '{job.name}' received, command: {exec_job}")
            logger.info(f"Environment: {job.container_img_url}")
            ext_jobid = (
                subprocess.check_output(
                    "mkdir -p results && echo hello > results/test.txt",
                    # '{submitcmd} "{jobscript}"'.format(
                    #     submitcmd=submitcmd, jobscript=jobscript
                    # ),
                    shell=True,
                )
                .decode()
                .split("\n")
            )
        except subprocess.CalledProcessError as ex:
            logger.error(
                "Error submitting jobscript (exit code {}):\n{}".format(
                    ex.returncode, ex.output.decode()
                )
            )
            error_callback(job)
            return
        if ext_jobid and ext_jobid[0]:
            ext_jobid = ext_jobid[0]
            self.external_jobid.update((f, ext_jobid) for f in job.output)
            logger.info(
                "Submitted {} {} with external jobid '{}'.".format(
                    "group job" if job.is_group() else "job", jobid, ext_jobid
                )
            )
            self.workflow.persistence.started(job, external_jobid=ext_jobid)

        submit_callback(job)

        with self.lock:
            self.active_jobs.append(
                GenericClusterJob(
                    job,
                    ext_jobid,
                    callback,
                    error_callback,
                    jobscript,
                    jobfinished,
                    jobfailed,
                )
            )


def run_jobs(rjc_api_client, workflow_workspace, workflow_file, workflow_parameters):
    """Run Snakemake jobs using custom REANA executor."""
    # Monkeypatch KubernetesExecutor class in `scheduler` module
    REANAClusterExecutor.rjc_api_client = rjc_api_client
    scheduler.GenericClusterExecutor = REANAClusterExecutor

    workflow_file_path = os.path.join(workflow_workspace, workflow_file)
    snakemake(
        workflow_file_path,
        printshellcmds=True,
        cluster="source",
        config=workflow_parameters,
        workdir=workflow_workspace,
        immediate_submit=True,
        notemp=True,
    )
