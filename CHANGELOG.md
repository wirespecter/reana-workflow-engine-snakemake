# Changelog

## [0.95.0](https://github.com/wirespecter/reana-workflow-engine-snakemake/compare/0.9.3...0.95.0) (2024-08-16)


### ⚠ BREAKING CHANGES

* **python:** drop support for Python 3.6 and 3.7

### Build

* **docker:** fix XRootD repository location ([#95](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/95)) ([69fea32](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/69fea329dd9bf91ff9eb1de9ac741262512a872a))
* **docker:** pin setuptools to v70 ([#100](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/100)) ([2dd079e](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/2dd079e3289181e75ebd9fc11193397e8407b8ec))
* **docker:** upgrade to Ubuntu 24.04 and Python 3.12 ([#99](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/99)) ([6aae67f](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/6aae67f78f089215bb0b3f54079cd0d4b0a09077))
* **python:** add minimal `pyproject.toml` ([#100](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/100)) ([01883da](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/01883da42bc2f77c0e3e59dfbca54682a2f51405))
* **python:** avoid using requirements.in ([#93](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/93)) ([b3e4727](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/b3e47271929763a57793319d65a1d67559dc4e4f))
* **python:** drop support for Python 3.6 and 3.7 ([#94](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/94)) ([3ef33c3](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/3ef33c3192d70b64d7f13a213186dd449fc8cb42))
* **python:** remove deprecated `pytest-runner` ([#100](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/100)) ([14dec1b](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/14dec1b96cb9be542a4e99a84dfc85819eae5c1f))
* **python:** use optional deps instead of `tests_require` ([#100](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/100)) ([9f37894](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/9f37894a1faf9ef60cb62d8a50471ad89a8fb6b9))


### Bug fixes

* **executor:** override default resources to remove mem/disk ([#91](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/91)) ([572a83f](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/572a83f5190c7cae95a4607b792f4b6e0c39262c)), closes [#90](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/90)


### Continuous integration

* **actions:** update GitHub actions due to Node 16 deprecation ([#89](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/89)) ([b0e3669](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/b0e366922073e359c8b740696179e23d9daa4033))
* **commitlint:** check PR number presence in merge commits ([#101](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/101)) ([b0fca51](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/b0fca51de2d39fb31a9009e962f8c57f1448d5fe))
* **commitlint:** do not check merge commit's ancestors ([#92](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/92)) ([690dfc2](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/690dfc2668aea85549e6dbaad131e15afb1ecb21))
* **pytest:** invoke `pytest` directly instead of `setup.py test` ([#100](https://github.com/wirespecter/reana-workflow-engine-snakemake/issues/100)) ([7ad6738](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/7ad6738610f0cf80989eed308eda773a3610b202))


### Chores

* **master:** release 0.95.0-alpha.1 ([998ced1](https://github.com/wirespecter/reana-workflow-engine-snakemake/commit/998ced1869aabad2c37fe7a1c3f32cc6eb4b58f1))

## [0.9.3](https://github.com/reanahub/reana-workflow-engine-snakemake/compare/0.9.2...0.9.3) (2024-03-04)


### Build

* **docker:** install correct extras of reana-commons submodule ([#79](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/79)) ([fd9b88a](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/fd9b88a857ba016343d956e42a49b6fbc906f068))
* **docker:** non-editable submodules in "latest" mode ([#73](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/73)) ([c3595c2](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/c3595c297e90f74a9215fd76c6d6b5f69d640440))
* **python:** bump all required packages as of 2024-03-04 ([#85](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/85)) ([66e81e2](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/66e81e2148ad4ba72099a90dbb556454df3cfc99))
* **python:** bump shared REANA packages as of 2024-03-04 ([#85](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/85)) ([d07f91f](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/d07f91f6f725050c681c66ec920727f26db3fdbf))


### Features

* **config:** get max number of parallel jobs from env vars ([#84](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/84)) ([69cfad4](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/69cfad460b240e5dbafea42137d891d6fea607a5))
* **executor:** upgrade to Snakemake v7.32.4 ([#81](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/81)) ([4a3f359](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/4a3f3592c8dd3f323e81850f5bdfae45ea893825))


### Bug fixes

* **progress:** handle stopped jobs ([#78](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/78)) ([4829d80](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/4829d80a5e03ab5788fb6646bd792a7345abe14a))


### Code refactoring

* **docs:** move from reST to Markdown ([#82](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/82)) ([31de94f](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/31de94f79b1955328961d506ce9d8d4efbe7227f))


### Continuous integration

* **commitlint:** addition of commit message linter ([#74](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/74)) ([145b7e7](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/145b7e716a784c340e2ecdca5619b3ed97325b1b))
* **commitlint:** allow release commit style ([#86](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/86)) ([fd032db](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/fd032db1605ac1a295a0eac5c32799707d78cd6b))
* **commitlint:** check for the presence of concrete PR number ([#80](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/80)) ([b677913](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/b677913aef2df090103d461bc71dc2cde42b4212))
* **release-please:** initial configuration ([#74](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/74)) ([9b16bd0](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/9b16bd052903be4a8c567b2e71f7b56a601982b4))
* **release-please:** update version in Dockerfile ([#77](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/77)) ([3c35a67](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/3c35a67db7c181e23f28fda6152f40c8251f9b74))
* **shellcheck:** fix exit code propagation ([#80](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/80)) ([ad15c0d](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/ad15c0d0e2020fd874a9eed5c4b36e320129b9eb))


### Documentation

* **authors:** complete list of contributors ([#83](https://github.com/reanahub/reana-workflow-engine-snakemake/issues/83)) ([4782678](https://github.com/reanahub/reana-workflow-engine-snakemake/commit/478267864a20da6ab4d7f99be5592fcf19a20ca1))

## 0.9.2 (2023-12-12)

- Adds automated container image building for amd64 architecture.
- Adds metadata labels to Dockerfile.
- Fixes creation of image thumbnails for output files in Snakemake HTML execution reports.
- Fixes container image building on the arm64 architecture.

## 0.9.1 (2023-09-27)

- Changes remote storage file support to use XRootD 5.6.0.
- Fixes the reported total number of jobs for restarted workflows by excluding cached jobs that were simply reused from previous runs in the workspace and not really executed by Snakemake.
- Fixes an issue where workflows could get stuck waiting for already-finished jobs.
- Fixes container image names to be Podman-compatible.

## 0.9.0 (2023-01-19)

- Adds support for specifying `slurm_partition` and `slurm_time` for Slurm compute backend jobs.
- Adds support for XRootD remote file locations in workflow specification definitions.
- Adds support for Kerberos authentication for workflow orchestration.
- Adds support for Rucio authentication for workflow jobs.
- Changes global setting of maximum number of parallel jobs to 300.
- Changes the base image of the component to Ubuntu 20.04 LTS and reduces final Docker image size by removing build-time dependencies.
- Fixes progress reporting for failed workflow jobs.

## 0.8.1 (2022-02-07)

- Adds support for specifying `kubernetes_job_timeout` for Kubernetes compute backend jobs.
- Adds polling job-controller to determine job statuses instead of checking files.

## 0.8.0 (2021-11-22)

- Adds initial REANA Snakemake executor implementation.
- Adds support for snakemake reports generation.
- Adds support for REANA custom resources.
- Adds support for parallel job execution.
