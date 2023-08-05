.. cloud_changelog:

==========================
Coiled Cloud Release Notes
==========================

These release notes are related to updates for `cloud.coiled.io <https://cloud.coiled.io>`_.

20 May 2022
===========

Enhancements
++++++++++++

- Coiled v2 now supports GPU instances on both AWS and GCP. Only a single GPU per instance is currently utilized.
  For AWS, simple use an instance type with attached GPU; for GCP, you'll need to use ``n1`` family instance and
  attach guess accelerator using ``worker_gpu_type`` keyword when creating a cluster.
  See :doc:`tutorials/select_gpu_type` for more information.

April 2022
==========

Enhancements
++++++++++++

- Coiled v2 Beta clusters now accept the ``environ`` and ``worker_class`` keyword argument.
- Fixed a bug in v2 clusters affecting instance type selection while creating clusters in an account that's different from your user's default account.
- You can now specify an extra service account when configuring your GCP cloud backend. For Coiled v2, this service account will be attached to the instances that Coiled 
  creates so it can access resources in your GCP account.

29 March 2022
=============

Enhancements
++++++++++++
- Signing up for a pro account now requires account verification

22 March 2022
=============

Deprecated
++++++++++

- Creating cluster configurations from the UI are longer available in preparation for deprecation

Documentation
+++++++++++++

- Documentation related to creating cluster configuration has been removed in preparation for the deprecation of custom cluster configurations

17 March 2022
=============

Enhancements
++++++++++++

- Some internal changes to improve stability and reliability.

9 March 2022
============

Enhancements
++++++++++++

- Updated style and wording in the activation banner that new accounts see when they login to Coiled and their account
  isn't activated yet.
- You can now request your account activation directly from the activation banner, by clicking the `Activate Coiled Now!`
  button.


23 February 2022
================

Enhancements
++++++++++++

- Improved error message when asking for a Cluster that's over your account node limit. This error message will now
  contain the number of nodes requested, the account limit, and the cores limit for that account.

Fixes
+++++

- Fixed issue where accounts created using social login could get an invalid slug. Accounts created using social login
  will now always get a valid slug.
- Fixed issue where the core count in the usage tab of the clusters dashboard wouldn't update once the cluster scales up/down.

9 February 2022
===============

Fixes
+++++

- Fixed issue where the core count wasn't being appropriately counted if users specified instance types.

Enhancements
++++++++++++

- Core count will now get the number of cores from the instance vCPU and update the count as workers start
  connecting to the scheduler.

Documentation
+++++++++++++

- Added section for the new keyword argument :ref:`wait_for_workers <wait-for-workers>` that the ``coiled.Cluster()`` constructor
  is using. This argument is used to make sure that the Cluster is ready to start a computation and return more information
  back to the user when the Cluster can't get workers.
- Added a section on :ref:`minimal-docker` to be used with Coiled when creating software environments.


26 January 2022
===============

Fixes
+++++

- Fixed an issue that was causing the ``reset password`` page to reload continuously, preventing users from choosing a new password.
- Fixed issue that was causing clusters not to stop when requested by the user, if the cluster was created in a different availability
  zone than the default one.

Enhancements
++++++++++++

- You are now able to specify any instance type available from your cloud provider of choice. You might wish to run the command 
  ``coiled.get_notifications(level="ERROR")`` if you have issues creating clusters with the specified instance types.

Documentation
+++++++++++++

- Updated activation email for users requiring account activation to activate@coiled.io.


12 January 2022
===============

Fixes
+++++

- Fixed issue where setting ``nthreads`` when launching a cluster wasn't respected. You can override worker
  ``worker_options={"nthreads": <number of threads>}`` passed to the ``coiled.Cluster`` constructor.
- Removed references to Azure from Coiled Cloud

Enhancements
++++++++++++

- For AWS, VPC creation that runs when you set your backend options to run Coiled on your cloud provider of choice will now
  create one subnet for each Availability Zone in the region you chose to run Coiled.
- You can now specify an Availability Zone when creating a cluster (you might need to rerun the VPC creation process).
- Periodic cleanup will now cleanup resources in different Availability Zones.

Documentation
+++++++++++++

- Added warning in the Firewall and Networking section of the cloud providers documentation that this feature is under
  active development and is in an experimental phase.

15 December 2021
================

Fixes
+++++

- Fixed a frontend issue where a customer's payment info was not showing up even though it had been entered.
- Fixed an intermittent issue where users for some credit cards were unable to enter their security code. This has
  been fixed and all credit cards should work consistently.

Enhancements
++++++++++++

- Dask workers now use public IPs so that NAT Gateway is no longer needed;
  ingress to workers is still blocked. :doc:`tutorials/bring_your_own_network` can disable
  public IPs for workers by setting the the `give_workers_public_ip` option.
- Added a UI for :doc:`bring your own network <tutorials/bring_your_own_network>` so
  network options can also be configured through the UI when selecting your backend.
- Free tier account usage is still on an opt-in model.
  If you are a new user please contact support@coiled.io to enable software
  environments and cluster creations.
- Azure functionality has been removed and disabled for users. Users previously
  hosted on Coiled-hosted Azure have been migrated to the AWS backend.

Documentation
+++++++++++++

- Fixed a couple of broken links in the documentation on teams :doc:`teams`.
- Added more examples to the :doc:`bring your own network <tutorials/bring_your_own_network>`
  documentation.

01 December 2021
================


Enhancements
++++++++++++

- Added ability to manage API access tokens using (optional) expiration dates or
  manual revocation. Added support for managing API tokens via the Coiled Python
  client.
- Added account limit alert when 99% of the quota is used and when your account
  has reached its quota limit.
- Changed the default to use on-demand VMs for Dask workers as opposed to ``spot`` or ``preemptible`` instances.
  Backend options can still be set to use ``spot`` or ``preemptible`` instances, see
  :ref:`AWS backend options<aws_backend_options>` or :ref:`GCP backend options<gcp_backend_options>`.
- Added ability to use pre-existing cloud resources (e.g., VPC, subnets,
  security groups) when running Coiled in your own cloud provider account.

Deprecated
++++++++++

- Coiled Notebooks and Coiled Jobs have been deprecated.


Documentation
+++++++++++++

- As part of upcoming deprecation of the Azure cloud provider backend, the
  documentation related to Azure has been removed.
- Coiled client version of 0.0.55 or higher is required - please update your client if needed.

10 November 2021
================

Fixes
+++++

- Dask workers will now use all CPU/Memory available for the instance type in which they have
  been created. In the past, workers would be limited by your CPU/Memory specification.


Enhancements
++++++++++++

- Moved the **Coiled Subscription** tab up on the account settings page to make it easier
  for you to see how many credits you have used so far.
- If you are using Coiled on your cloud provider, you can now
  customize ingress rules for the firewall/security group created by Coiled
  by specifying ingress ports and a CIDR block.

Deprecated
++++++++++

- Coiled Notebooks and Coiled Jobs were an experimental feature which is being deprecated.
  After December 1, 2021, these will no longer be available.


Documentation
+++++++++++++

- Updated the list of dependencies in the documentation page :doc:`software_environment_creation`
  to include ``dask[complete]`` while creating a software environment with pip.
- Added troubleshooting article for :doc:`repeated cluster timeout errors.
  <troubleshooting/repeated_timeout_errors>`.
- Embedded tutorial videos for `cluster configuration`
  and :ref:`software environments <software-envs>` documentation.

27 October 2021
===============

Fixes
+++++

- The route table for the private subnet that is created when Coiled creates a VPC
  in your AWS account, is now called ``coiled-vm-private-router`` instead of
  ``coiled-vm-public-router``.
- Mitigate Rate Limit exceptions when performing some actions like scaling clusters,
  which should improve cluster reliability.
- Software environment names must now be lowercase only.


Enhancements
++++++++++++

- Removed experimental warnings for GCP and Azure in the UI when choosing a
  backend option for an account.
- Removed fallback option to fetch logs from instances via SSH.


Documentation
+++++++++++++

- Removed experimental notes for GCP and Azure in the respective section of
  the documentation for these backends.
- Updated default ``worker_memory`` to ``8GiB`` in a few pages where it was
  saying that the default was ``16GiB``.
- Added a section about network architecture to the :doc:`security` page.
- Added a tutorial on :doc:`tutorials/select_instance_types`.
- Added a tutorial on :doc:`tutorials/select_gpu_type`.
- Added section on selecting instance types in the documentation page
  :doc:`cluster_creation`.
- Added a Networking section on the documentation page for the :doc:`backends_aws`
  that explains how you can specify your AWS security groups using the new arguments
  ``enable_public_http``, ``enable_public_ssh`` and ``disable_public_ingress``.


13 October 2021
===============

Fixes
+++++

* Environment variables sent to the Cluster with the keyword argument
  ``environ=`` are now being converted to strings, which fixes
  occasional failures when sending non-string values to the Cluster.

Enhancements
++++++++++++

* You can now use Coiled in your own GCP account. Please refer to the
  :doc:`backends_gcp` documentation.
* You can now use Coiled in your own Azure account.
* You can now select a ``region`` or ``zone`` when launching clusters in GCP.
* You can now create software environments using Docker images stored in your
  private ECR (AWS), ACR (Azure) or GAR (GCP) container registries, in addition
  to Docker Hub and other registries, by calling
  ``coiled.create_software_environment(container="<URI>")``.
* Coiled now collects statistical profiling data from your Dask clusters.
  This data is visualized as a flame graph on the Analytics page for
  individual clusters.
* You can now hide/show columns in the Clusters Dashboard. The options are: Id,
  Cluster Name, Created By, Status, Num Workers, Software Environment,
  Cost (current), Cost(total), Last Seen, Backend, Runtime, Spot/Preemptible.
* Improve log filtering for AWS when viewing logs in the Coiled UI.


Documentation
+++++++++++++

* Added a new example on using the :doc:`Dask Snowflake <examples/snowflake>`
  connector.
* Fix link to Coiled's privacy policy in the :doc:`security` page.
* Added new section in the :doc:`gpu` documentation to demonstrate the use how
  of GPUs with the Afar library to run remote commands.


28 September 2021
=================

Fixes
+++++

* Resolve error that was throwing an "Unable to stop cluster" error message in the Clusters
  Dashboard for users using the Azure backend.
* Fix issue with workers not being created when users create a new Cluster using the AWS backend.
* Resolve error that was causing Clusters to shut down immediately upon creation for users using the AWS backend.
* Fix issue that was causing the Cluster Dashboard table to show zero workers count even though the workers were
  created and connected to the scheduler.


Enhancements
++++++++++++

* Add label containing the instance name to notification when running ``coiled.get_notifications()``.


Documentation
+++++++++++++

* Fix typo in CLI command, documentation mentioned ``coiled inspect`` but the right command is ``coiled env inspect``.
* Update :doc:`teams` page to better explain the distinction between Accounts and Teams.
