Changes
=======

Version 0.9.1 (2023-09-27)
--------------------------

- Changes remote storage file support to use XRootD 5.6.0.
- Fixes the reported total number of jobs for restarted workflows by excluding cached jobs that were simply reused from previous runs in the workspace and not really executed by Snakemake.
- Fixes an issue where workflows could get stuck waiting for already-finished jobs.
- Fixes container image names to be Podman-compatible.

Version 0.9.0 (2023-01-19)
--------------------------

- Adds support for specifying ``slurm_partition`` and ``slurm_time`` for Slurm compute backend jobs.
- Adds support for XRootD remote file locations in workflow specification definitions.
- Adds support for Kerberos authentication for workflow orchestration.
- Adds support for Rucio authentication for workflow jobs.
- Changes global setting of maximum number of parallel jobs to 300.
- Changes the base image of the component to Ubuntu 20.04 LTS and reduces final Docker image size by removing build-time dependencies.
- Fixes progress reporting for failed workflow jobs.

Version 0.8.1 (2022-02-07)
--------------------------

- Adds support for specifying ``kubernetes_job_timeout`` for Kubernetes compute backend jobs.
- Adds polling job-controller to determine job statuses instead of checking files.

Version 0.8.0 (2021-11-22)
--------------------------

- Adds initial REANA Snakemake executor implementation.
- Adds support for snakemake reports generation.
- Adds support for REANA custom resources.
- Adds support for parallel job execution.
