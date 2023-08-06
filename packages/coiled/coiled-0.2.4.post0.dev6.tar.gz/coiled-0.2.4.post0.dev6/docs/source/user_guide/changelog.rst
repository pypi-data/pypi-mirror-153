.. changelog:

===========================
Coiled Client Release Notes
===========================

These release notes are related to updates to the ``Coiled`` Python package.

0.2.2
======

- (Coiled v2) ``backend_options`` now lets you specify multiple CIDR blocks to open for ingress
  to your scheduler using the ``ingress`` keyword; see :doc:`tutorials/configuring_firewalls`
  for more information.

0.2.1
======

- Relaxes the version constraint on ``click`` in the ``coiled`` package's dependencies.

0.2.0
======
Released May 5th, 2022

This version switches to using v2 clusters (see :doc:`v2`).

0.0.78
======
Released April 28, 2022

- (Coiled v2) You can now use the ``worker_class`` argument when creating a Cluster to change the workers
  class of the workers created by Coiled.
- (Coiled v2) You can now ask for AWS Spot instances When creating a cluster.
- (Coiled v2) Various improvements to the Cluster widget.
- The ``coiled`` package now supports Python 3.10. Note that Python 3.10 is not recommended if you ar
  using the ``coiled-runtime`` package which includes a Dask version (2022.1.0) that does not support
  Python 3.10.
- The CLI command ``coiled env create`` used to create software environments,
  now accepts an ``--account`` option to specify the account to use for the
  creation of that software environment.

0.0.72
=======

Released March 29, 2022

- No user-facing changes

0.0.70
=======

Released March 22, 2022

- Added deprecation warning for cluster configurations. This feature will soon be deprecated

0.0.69
=======

Released March 17, 2022

- No user-facing changes included in this release.


0.0.68
======

Released March 9, 2022

- Sometimes fetching account credentials would fail if the server responded with a brief error code.
  The code will now retry to fetch Coiled credentials for your user if the server responds with an error code.
- The command :meth:`coiled.list_instance_types()` will now accept exact values or a range of values for `cores`,
  `memory` and `gpus`. You can specify a range by passing a list of two values, for example: 
  `coiled.list_instance_types(cores=[2, 8])`.
- When fetching instance types with the command `coiled.list_instance_types()` you can now specify memory values as
  you would when creating Clusters. For example: `coiled.list_instance_types(memory="8GiB")`.

0.0.67
======

Released February 25, 2022

- Release is the same as 0.0.66, this new version was released to address some versioning issues
  that the team found.

0.0.66
======

Released February 23, 2022

- When creating a Cluster, if you specify an account with the keyword argument ``account=`` that is
  not valid, the request will fail earlier. The error message will also contain the account name that
  you specified.
- Updated the error message that the command ``coiled.delete_software_environment()`` returns if the
  software environment doesn't exist. The error message will now contain the name of the software
  environment and the account.

0.0.65
======

Released February 11, 2022

- Fix misleading error message warning about not getting workers, when workers don't connect
  to the scheduler once ``wait_for_workers`` completes.

0.0.64
======

Released February 10, 2022

- This commit was stale and removed

0.0.63
======

Released February 9, 2022

- Clusters created with the ``coiled.Cluster`` will now wait for 30% of the requested workers
  before returning the prompt back to the user. Please refer to the documentation on
  :ref:`waiting for workers <wait-for-workers>`.
- The method :meth:`coiled.Cluster()` accepts a ``wait_for_workers`` keyword argument that allows
  you to increase/decrease the number of workers that need to be created before returning the
  prompt back. Additionally, the option to wait for workers can be toggled off.
- Improved validation for instance types when creating a Cluster
- Added a warning message informing users to run ``coiled.get_notifications(level="ERROR")``
  when no workers have connected to the scheduler after 10 minutes.
- If a Cluster can't get any workers due to availability issues or any other reason, the
  ``coiled.Cluster()`` constructor will now return the last error message when Coiled tried to
  create the worker (you need to have ``wait_for_workers`` enabled).

0.0.62
======

Released January 26, 2022

- The command ``coiled.list_instance_types`` now returns a list of all available instance
  types that your cloud provider allows.
- You can now specify a minimum number of memory, cores and gpus when using the command
  :meth:`coiled.list_instance_types`.

0.0.61
======

Released January 12, 2022

- Fixed issue with setting loop when using a Dask version higher than 2021.11.2

0.0.60
======

Released December 15, 2021

- ``set_backend_options`` no longer accepts arguments related to Azure backends.
- ``coiled.Cluster`` now accepts a ``use_scheduler_public_ip`` to configure the scheduler address the Coiled client connects to.

0.0.59
======

Released December 13, 2021

- Pin ``Dask.distributed`` to a version prior to ``2021.12.0`` since this introduced an incompatibility with ``coiled``.

0.0.58
======

Released December 03, 2021

- Fix a bug that prevented users' AWS credentials from being sent to clusters.

0.0.57
======

Released December 01, 2021

- Add support for managing long lived API access tokens via the Coiled client.
- Coiled client is tested and supported for Python version 3.7, 3.8 and 3.9.
  Coiled client raises an exception if you attempt to install in an environment with
  python versions below 3.7 or version 3.10
- Removed functionality associated with Coiled Notebooks and Coiled Jobs since they
  have been deprecated.

0.0.56
======

Released November 22, 2021

- Users can specify during cluster creation whether to use the public address or
  the private address of the scheduler to connect to the cluster.
- Python client will raise an ``AccountFormatError`` if the account is not a combination
  of lowercase letters, numbers or hyphens.


0.0.55
======

Released November 11, 2021

- Fixed issue that when using the command ``coiled login --token`` in the terminal, would
  show an error message saying that you have run out of credits.
- Updated connection timeout, which should mitigate the timeout error that sometimes was ocurring
  when launching clusters.
- You can now customize the firewall/security group that Coiled uses by adding a ``firewall`` dictionary
  and pass it to the ``backend_options`` keyword argument for the ``coiled.Cluster`` constructor.


0.0.54
======

Released October 17, 2021

- You can now specify a list of instance types with the 
  ``scheduler_vm_types``/``worker_vm_types`` when creating a cluster
  using the ``coiled.Cluster()`` constructor.
- You can now select a GPU type by using the keyword argument ``gpu_type`` from
  the ``coiled.Cluster()`` constructor.
- Added a new command ``coiled.list_instance_types()`` to the Coiled Client which
  returns a list of allowed instance types that you can use while creating your
  Cluster.
- Added a new command ``coiled.list_gpu_types()`` to the Coiled Client which returns
  a list of allowed GPU types that you can use while creating your cluster.
- You can now specify ``enable_public_http``, ``enable_public_ssh`` and ``disable_public_ingress``
  when using the :meth:`coiled.set_backend_options` to have more control on the security group
  that Coiled created with AWS.
- You can now use the Clusters private IP address when interacting with your cluster by
  using ``backend_options={"disable_public_ingress": True}`` when creating a cluster with
  the ``coiled.Cluster()`` constructor or when setting your backend with the command
  :meth:`coiled.set_backend_options`.
- You can now remove port 22 from the AWS security group that Coiled creates in your
  account by setting the ``enable_public_ssh`` flag to False used with either the
  ``backend_options`` or when setting your backend with the command
  :meth:`coiled.set_backend_options`.

  

0.0.53
======

Released October 13, 2021


- Environment variables sent to the Cluster with the ``environ=`` keyword argument
  are now converted to strings.
- Added a depagination method so our list commands (for example 
  ``coiled.list_cluster_configurations()``) will now return all of the items instead
  of only the last 50.


0.0.52
======

Released September 16, 2021

- ``coiled.set_backend_options()`` no longer supports the deprecated ECS backend.


0.0.51
======

Released September 1, 2021

- Coiled clusters now support adaptive scaling. To enable it, create
  a cluster, then run ``cluster.adapt(maximum=max_number_of_workers)``.
- Removed an unused ``region`` parameter from ``coiled.Cluster()``.
  Cloud provider regions can be set using ``backend_options=``.
- ``coiled.create_notebook()`` now takes an optional ``account=`` parameter
  like the rest of the API. If there is a conflict between the account
  specified via the name and the account specified via tha ``account`` parameterm
  an error is raised.


0.0.50
======

Released August 24, 2021

- Another ``aiobotocore``-related fix.


0.0.49
======

Released August 20, 2021

- Hotfix to support ``aiobotocore==1.4.0``.


0.0.48
======

Released August 17, 2021

- Hotfix to relax the dependency on ``typing_extensions`` in order to conflict less
  with third-party packages.


0.0.47
======

Released August 13, 2021

- ``coiled.set_backend_options()`` has changed several parameter names, and it is now
  possible to specify a gcp zone. A VPC will now be created if credentials are provided.
- ``'vm_aws'`` is now the default backend for ``coiled.set_backend_options()`` in
  preparation for the deprecation of the ``'ecs'`` backend.


0.0.46
======

Released August 2, 2021.

- Hotfix to better-specify typing-extensions dependency.


0.0.45
======

Released July 28, 2021.

- ``coiled.set_backend_options()`` now supports specifying a Google Artifact Registry
  for storing software environments.
- Cluter protocols (currently either ``tls`` or ``wss``) can now be configured using
  the dask configuration system under ``coiled.protocol``.
- Cluster scheduler and worker options can now be configured using the dask configuration
  system under ``coiled.scheduler-options`` and ``coiled.worker-options``.


0.0.44
======

Released July 15, 2021.

- Users with customer-hosted accounts on Google Cloud Platform can now provide a region
  (``gcp_region_name``) to ``coiled.set_backend_options()``.
- Users can now specify a ``protocol`` when creating a Coiled cluster. By default,
  clusters communicate over TLS (``"tls"``), but in some restricted environments it
  can be useful to direct traffic through the Coiled web application over websockets
  (``"wss"``).
- The command line interface for creating a software environment (``conda env create``)
  now accepts an optional ``--conda-env-name`` parameter to specify the name of the
  conda environment into which packages will be installed (defaults to ``coiled``).

0.0.43
======

Released June 29, 2021.

- Hotfix to remove aiostream dependency


0.0.42
======

Released June 29, 2021.

- ``coiled.set_backend_options()`` now supports configuring your Coiled account to
  run in your own Google Cloud Plaform account.


0.0.41
======

Released June 9, 2021.

- New function ``coiled.set_backend_options()`` which allows users to set the options
  for an account (e.g., cloud provider, region, docker registry) from the Python
  client. Previously this was only available using the Coiled web application.
- Fixed a bug in ``coiled.performance_report()`` that was preventing performance data
  from being captured.
- Fixed an issue where an error building software environments could result in hanging
  client sessions.
- ``coiled.Cluster()``, ``coiled.start_job()``, ``coiled.create_software_environment()``,
  and ``coiled.create_notebook()`` can now take an optional ``environ`` dictionary as
  an argument, allowing users to pass in environment variables to clusters, jobs,
  software environments, and notebooks.  These environment variables are not encrypted,
  and so should not be used to store credentials or other sensitive information.
- ``coiled.list_core_usage()`` now shows additional information about how many credits
  your account has used for the current program period.
- ``coiled.Cluster()`` no longer raises a warning if no AWS credentials can be found,
  since a given cluster may not want or need to use them.


0.0.40
======

Released May 18, 2021.

- New functions ``coiled.performance_report()`` and ``coiled.list_performance_reports()``.
  ``coiled.performance_report()`` is a context manager which captures cluster computation
  as a dask performance report, uploads it to Coiled, and hosts it online for later viewing.
- New function ``coiled.get_notifications()`` returns notifications from resource
  creation steps in your chosen cloud provider. This can be useful in debugging when
  resources do not launch as intended.
- ``coiled.create_software_environment()`` now has an optional argument ``force_rebuild``,
  defaulting to ``False``, which forces a rebuild of the software environment, even
  if one matching the given specification already exists. There is a new corresponding
  flag ``--force-rebuild`` in the ``coiled env create`` command line command. 
- New functions ``coiled.cluster_logs()`` and ``coiled.job_logs()`` return logs from
  Coiled clusters and Coiled jobs, respectively. ``Cloud.logs()`` has been renamed to
  ``Cloud.cluster_logs()`` to better distinguish it from ``Cloud.job_logs()``.
- New function ``coiled.get_software_info()`` returns detailed information about a
  Coiled software environment specification.
- ``coiled.info()`` has been renamed to ``coiled.diagnostics()``, and now always returns
  JSON-formatted diagnostic information.
- New function ``coiled.list_user_information()`` provides information about the
  currently logged-in user.
- New function ``cloud.health_check()`` checks the user's connection with the Coiled
  Cloud application.
- ``coiled login --server <url-for-your-coiled-deployment>`` now works if there is a
  trailing slash in the URL.
- ``coiled login --account <team_slug>`` sets the user's specified account as a config value.
- Previously, some ``coiled`` functions accepted ``account`` as an optional parameter,
  and others did not. Now the entire API consistently allows users to specify
  their account with an ``account=`` keyword argument. The priority order for
  choosing an account to make API requests is:

  #. Accounts specified via a resource name (where applicable), e.g. ``name = <account-name>/<software-environment-name>``
  #. Accounts specified via the ``account=`` keyword argument
  #. Accounts specified in your Coiled configuration file (i.e. ``~/.config/dask/coiled.yaml``)
  #. The default account associated with your username (as determined by the token you use to log in)

- Most of the resource creation functions in the ``coiled`` API (e.g.,
  ``coiled.Cluster()`` or ``coiled.create_software_environment()``) can take a lot of
  optional arguments. The order of these arguments in their function invocations
  is not important, and so they have been turned into keyword-only arguments.


0.0.39
======

Released on May 3, 2021.

- Following dask/distributed, we have dropped support for Python 3.6
- The arguments for ``coiled.Cluster()`` are now keyword-only.
- ``coiled`` is now more fully type annotated, allowing for better type checking
  and editor integration.
- ``coiled.Cloud.logs()`` now has ``account`` as an optional second parameter instead of
  a required first parameter to be more consistent with the rest of the API.
- Fixed a bug where updating the software environment in a cluster configuration
  did not work.
- Add a ``--private`` flag to the command line interface for ``coiled env create``.
- Fixed a bug where the ``rich`` console output from ``coiled`` did not work well with
  the Spyder editor.
- Fixed a bug where the ``coiled.Cloud.close()`` did not properly clean up threads.


0.0.38
======

Released on March 25, 2021.

- Improve connection error when creating a ``coiled.Cluster`` where the local
  and remote versions of ``distributed`` use different protocol versions
- Return the name of newly started jobs for use in other API calls


0.0.37
======

Released on March 2, 2021.

- Add core usage count interface
- Make startup error more generic and hopefully less confusing
- Filter clusters by descending order in ``coiled.list_clusters()``
- Add messages to commands and status bar to cluster creation
- Don't use coiled default if software environment doesn't exist
- Handle case when trying to create a cluster with a non-existent software environment
- Set minimum ``click`` version
- Several documentation updates


0.0.36
======

Released on February 5, 2021.

- Add backend options docs
- Fix CLI command install for python < 3.8
- Add color to coiled login output
- Fix bug with ``coiled.Cluster(account=...)``
- De-couple container registry from backends options


0.0.35
======

Released on January 29, 2021.

- Flatten json object if error doesn't have ``"message"``
- Enable all Django middleware to run ``async``
- Remove redundant test with flaky input mocking
- Use util ``handle_api_exception`` to handle exceptions


0.0.34
======

Released on January 26, 2021.

- Update AWS IAM docs
- Add ``--retry``/``--no-retry`` option to ``coiled login``
- Update default conda env to ``coiled`` instead of ``base``
- Add ``worker_memory < "16 GiB"`` to GPU example
- Fix small issues in docs and add note for users in teams
- Do not add python via conda if ``container`` in software spec
- Use new ``Status`` ``enum`` in ``distributed``


0.0.33
======

Released on January 15, 2021.

- Update ``post_build`` to run as POSIX shell
- Fix errors due to software environment / account name capitalization mismatches
- Automatically use local Python version when creating a ``pip``-only software environment
- Improved support for custom Docker registries
- Several documentation updates


0.0.32
======

Released on December 22, 2020.

- Add ``boto3`` dependency


0.0.31
======

Released on December 22, 2020.

- Add ``coiled.backend-options`` config value
- Allow selecting which AWS credentials are used
- Don't initialize with ``account`` when listing cluster configurations
- Add support for using custom Docker registries
- Add ``coiled.cluster_cost_estimate``
- Several documentation updates


0.0.30
======

Released on November 30, 2020.

- Update API to support generalized backend options
- Enable ``coiled.inspect`` and ``coiled.install`` inside Jupyter


0.0.29
======

Released on November 24, 2020.

- Add informative error message when AWS GPU capacity is low
- Fix bug in software environment creation which caused conda packages to be uninstalled
- Add notebook creation functionality and documentation
- Generalize backend options
- Add support for AWS Fargate spot instances


0.0.28
======

Released on November 9, 2020.

- Expose ``private`` field in list/create/update
- More docs for running in users' AWS accounts
- Add Dask-SQL example
- Use examples account instead of coiled-examples
- Add list of permissions for users AWS accounts
- Add example to software environment usage section
- Update ``conda_env_name`` description
- Set default TOC level for sphinx theme


0.0.27
======

Released on October 9, 2020.

- Fix AWS credentials error when running in Coiled notebooks


0.0.26
======

Released on October 8, 2020.

- Handle AWS STS session credentials
- Fix coiled depending on older aiobotocore
- Only use proxied dashboard address in Jobs
- Improve invalid fargate resources error message
- Mention team accounts
- Support AWS credentials to launch resources on other AWS accounts
- Update FAQ with a note on notebooks and Azure support
- Add GPU docs
- Add jupyterlab example
- Add community page
- Add tabbed code snippets to doc landing page
- Ensure job configuration description and software envs are updated


0.0.25
======

Released on September 22, 2020.

- Handle redirecting from ``beta.coiled.io`` to ``cloud.coiled.io``
- Add Prefect example
- Update dashboards to go through our proxy
- Add descriptions to notebooks
- Update cluster documentation
- Add Optuna example


0.0.24
======

Released on September 16, 2020.

- Support overriding cluster configuration settings in ``coiled.Cluster``
- Don't require region on cluster creation
- Add links to OSS licenses
- Add ability to upload files
- Add access token for private repos


0.0.23
======

Released on September 4, 2020.

- Fixed bug where specifying ``name`` in a conda spec would cause clusters to not be launched
- Open external links in a separate browser tab in the docs
- Explicitly set the number of worker threads to the number of CPUs requested if not otherwise specified
- Improvements to Coiled login behavior
- Update to using ``coiled/default`` as our default base image for software environments
- Several documentation updates


0.0.22
======

Released on August 27, 2020.

- Add AWS multi-region support
- Log informative message when rebuilding a software environment Docker image
- Remove link to Getting Started guide from ``coiled login`` output
- Update ``distributed`` version pinning
- Add support for running non-Dask code through Coiled ``Jobs``
- Several documentation updates


0.0.21
======

- Add logs to web UI
- Verify worker count during cluster creation
- Raise more informative error when a solve conda spec is not available
- Improve docker caching when building environments


0.0.20
======

- Allow 'target' conda env in creating software environment (#664)
- Start EC2 instances in the right subnets (#689)


0.0.19
======

- Added support for installing pip packages with ``coiled install``
- Support Python 3.8 on Windows with explicit ``ProactorEventLoop``
- Updated default ``coiled.Cluster`` configuration to use the current Python version
- Updated dependencies to include more flexible version checking in ``distributed``
- Don't scale clusters that we're re-connecting to
- Added support for using custom worker and scheduler classes


0.0.18
======

Released August 8, 2020.

- Add ``--token`` option to ``coiled login``
- Add ``post_build=`` option to ``coiled.create_software_environment``
- Add back support for Python 3.6
- Remove extra newline from websocket output
- Remove ``coiled upload`` from public API
- Add ``coiled env`` CLI command group
- Several documentation updates


0.0.17
======

Released July 31, 2020.

- Move documentation page to docs.coiled.io
- Added ``--version`` flag to ``coiled`` CLI
- Raise an informative error when using an outdated version of the ``coiled`` Python API
- Several documentation updates
- Added ``coiled.Cluster.get_logs`` method
- Added top-level ``coiled.config`` attribute
- Use fully qualified ``coiled.Cluster`` name in the cluster interactive IPython repr


0.0.16
======

Released July 27, 2020.

- Added getting started video to docs.
- Added support GPU enabled workers.
- Added new documentation page on configuring JupyterLab.
- Added support for specifying pip, conda, and/or container inputs when creating software environments.
- Remove account argument from ``coiled.delete_software_environment``.
- Added cost and feedback FAQs.


0.0.15
======

Released July 22, 2020.

- Removed "cloud" namespace in configuration values.
- Several documentation updates.
- Added new security and privacy page to the docs.
- Added ``coiled upload`` command for creating a Coiled software environment
  from a local conda environment.
- Added tests for command line tools.


0.0.14
======

Released July 17, 2020.


0.0.13
======

Released July 16, 2020.

- Update "Getting Started" documentation page.
- Update ``coiled.create_software_environment`` to use name provided by ``conda=`` input, if provided.
- Send AWS credentials when making a ``Cluster`` object.


0.0.12
======

Released July 14, 2020.

- Switch to using full ``coiled`` Python namespace and rename ``CoiledCluster`` to ``coiled.Cluster``
- Raise informative error when attempting to create a cluster with a non-existent cluster configuration
- Bump supported ``aiobotocore`` version to ``aiobotocore>=1.0.7``
- Add ``coiled install`` command to create conda software environments locally
- Repeated calls to ``Cloud.create_cluster_configuration`` will now update an existing configuration

0.0.11
======

Released July 9, 2020.

-  Don't shut down clusters if we didn't create them
-  Slim down the outputs of ``list_software_environments`` and ``list_cluster_configurations``

0.0.10
======

Released July 8, 2020.

-  Use websockets to create clusters due to long-running requests
-  Avoid excess endlines when printing out status in the CLI
-  Allow calling coiled env create repeatedly on the same environment

0.0.9
=====

Released July 7, 2020.

-  Change default to coiled/default
-  Add ``coiled login`` CLI command
-  Use account namespaces everywhere, remove ``account=`` keyword
-  Allow the use of public environments and configurations

0.0.8
=====

Released on July 1, 2020.

- Update to use new API endpoint scheme
- Adds ``conda env create`` command line interface


0.0.7
=====

Released on June 29, 2020.

- Adds ``Cloud.create_software_environment``, ``Cloud.delete_software_environment``, and ``Cloud.list_software_environments`` methods
- Adds ``Cloud.create_cluster_configuration``, ``Cloud.delete_cluster_configuration``, and ``Cloud.list_cluster_configurations`` methods
- Update ``Cloud`` object to use a token rather than a password
- Changed name of package from ``coiled_cloud`` to ``coiled``


0.0.6
=====

Released on May 26, 2020.

- Includes ``requirements.txt`` in ``MANIFEST.in``


0.0.5
=====

Released on May 26, 2020.

- Includes versioneer in ``MANIFEST.in``


0.0.4
=====

Released on May 26, 2020.

- Adds ``LICENSE`` to project


0.0.3
=====

Released on May 21, 2020.

Deprecations
------------

- Renamed ``Cluster`` to ``CoiledCluster``
