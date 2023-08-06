==================
Security & Privacy
==================

This page outlines Coiled's security and privacy policies.


Security policies
-----------------

Coiled credentials
^^^^^^^^^^^^^^^^^^

You can create an API token at https://cloud.coiled.io/profile. There you can 
view details of tokens you've created, or revoke them. When you create the token,
you can optionally specify a number of days until the token expires.

Note that while you can view a list of tokens you've already created, 
you cannot view the token itself. We can only show that to you once when you 
create the token. 

When you :ref:`set up Coiled <coiled-setup>` with the ``coiled login`` command
line utility, your account username and token are stored in a local
configuration file at ``~/.config/dask/coiled.yaml``.

This username and token combination gives access to run
computations from a Coiled account and should be treated like a password.



Communication
^^^^^^^^^^^^^

Coiled generates TLS certificates on a per-cluster basis which are used to
manage access to each cluster's Dask scheduler and workers. These certificates
are stored encrypted in our database. Additionally, the scheduler and workers
for a cluster use
`secure communication between them <https://distributed.dask.org/en/latest/tls.html>`_
and are isolated by AWS networking security groups.

If a higher level of security is required for your application, please contact
sales@coiled.io to inquire about deploying Coiled on your internal systems.

Run in your infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^

For additional security, you can configure Coiled to deploy compute resources on
infrastructure that you control (e.g., within your own AWS account). In this
configuration, the control plane is still managed by Coiled, but all compute
resources, access to sensitive data, storage of software environment images, and
system logs will happen entirely within your cloud account.

Refer to the :ref:`data handling <data-handling>` and :doc:`backends <backends>`
sections in our documentation for more information.

AWS credentials
^^^^^^^^^^^^^^^

Often Dask workers in a cluster will need AWS permissions to access private data
or private AWS services. To address this need, Coiled will use the AWS
credentials from your account to generate a session token and then forward that
token to the Dask workers in your cluster.

Note that having local AWS credentials is not required to use use Coiled.
However, in this case only publicly accessible data and services will be
available to your cluster.

.. _network-architecture:

Network security and architecture
---------------------------------

Coiled was designed with secure network communication and data security in mind
based on many years of experience of working with Dask users in enterprise
environments. This section describes the network communication paths, ports, and
protocols that are used when creating and using Dask clusters that are managed
by Coiled.

The network architecture is described below in terms of two different contexts:

1. Communication related to users, the Coiled control plane, and your cloud
   provider account
2. Communication related to the Dask client, scheduler, workers, and data
   sources

Note that these network communication paths are mostly relevant when you have
configured Coiled to run in your :doc:`own cloud provider account <backends>`.
If you are using Coiled-hosted Dask clusters, then the Dask scheduler and
workers reside on Coiled-managed infrastructure, and all relevant network
communication with the Dask cluster occurs on Coiled-managed infrastructure.

Communication with Coiled Control plane
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Network communication with the Coiled control plane occurs when users log in to
Coiled Cloud, view their cluster or analytics dashboard, or request Dask
clusters. When a user requests the creation of a Dask cluster, then the Coiled
control plane communicates with your cloud provider's API to provision the
necessary cloud resources in your cloud provider account.

The Coiled control plane does not require direct connectivity to cloud resources
within your cloud provider account. Rather, all communication from the Coiled
control plane to your cloud provider account happens via the cloud provider's
API. Therefore, there is no requirement to open ports or to whitelist network
traffic originating from the Coiled control plane at https://cloud.coiled.io.

.. figure:: images/networking-coiled.png
   :width: 100%

============================== ====================================== =============== ===========================================================
Source                         Target                                 Protocol (Port) Description
============================== ====================================== =============== ===========================================================
User (browser)                 Coiled control plane (cloud.coiled.io) HTTPS (443)     Users accessing cluster dashboard, analytics, etc.
User (Coiled client)           Coiled control plane (cloud.coiled.io) HTTPS (443)     Users creating clusters, environments, etc.
Coiled control plane           Cloud provider APIs (AWS and GCP)      HTTPS (443)     Creation and management of cloud infrastructure
Dask scheduler                 Coiled control plane                   HTTPS (443)     Runtime analytics and performance metrics for Dask clusters
============================== ====================================== =============== ===========================================================

Communication with Dask clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Network communication with Dask clusters occurs when users connect to Dask
clusters via the Dask client, submit Dask computations, and view the Dask
cluster status on the Dask dashboard. Users only communicate directly with the
Dask scheduler, then the scheduler handles all network communication to the Dask
workers and subsequent communication to data sources. Users are not required to
have direct network access to Dask workers or data sources since they are only
interacting with the Dask scheduler.

If you've configured Coiled to run on your own cloud provider account, then the
control plane is still managed by Coiled, but all compute resources used by Dask
clusters, Dask client-to-scheduler communication, access to sensitive data,
storage of software environment images, and system logging occurs entirely
within your cloud account. In other words, data from your data sources never
flows through the Coiled control plane at any time because all network traffic
related to the Dask client, scheduler, worker, and data access occurs outside of
the Coiled network and only on your private cloud/network.

.. figure:: images/networking-dask.png
   :width: 100%

============================== ============== ====================== ==============================================
Source                         Target         Protocol (Port)        Description
============================== ============== ====================== ==============================================
User (Dask client)             Dask scheduler TCP (8786)             Users submitting Dask computations
User (browser)                 Dask dashboard HTTP (8787)            Users accessing Dask status dashboard
Dask workers                   Dask scheduler TCP (8786)             Dask workers communicating with scheduler
Dask scheduler                 Dask workers   TCP (1024-65535)       Dask scheduler communicating with workers
Dask workers                   Dask workers   TCP (1024-65535)       Dask workers communicating with other workers
Dask workers                   Data sources   Depends on data source Reading and writing data for user computations
============================== ============== ====================== ==============================================

.. note::

   The ports that are used by the Dask scheduler and Dask workers (listed in the
   table above) for inter-cluster communication are defaults as described in the
   `Dask documentation <https://docs.dask.org/en/latest/how-to/deploy-dask/cli.html>`_.
   If desired, you can customize the ports used by the Dask scheduler and Dask
   workers by passing :ref:`custom worker options <customize-cluster>` when you
   create Dask clusters with Coiled.

   For example, instead of using random ports within the unprivileged port range
   for the Dask workers, you can configure the Dask workers to use port 8000 as
   the Dask nanny port and port 9000 as the Dask computation port by specifying
   the following ``worker_options`` when creating a cluster:

   .. code-block:: python

      import coiled

      cluster = coiled.Cluster(worker_options={"port": 8000, "worker_port": 9000})

   If you configure your clusters in this manner, then you'll need to update
   your firewall or security group rules to allow traffic on ports 8000 and 9000
   for scheduler-to-worker communication as well as worker-to-worker
   communication.

Privacy policies
----------------

Sharing by default
^^^^^^^^^^^^^^^^^^

Information such as your software environments and cluster configurations are
publicly accessible by default to promote sharing and collaboration. However,
you may also create private software environments if
you prefer. See the :ref:`software visibility <software-visibility>` sections for
more information on private software environments.

Note that information about any cluster running on your account is *not*
publicly accessible and is only available to users which are members of the
account.


.. _data-handling:

Data handling
^^^^^^^^^^^^^

Coiled stores basic user data when you create an account, such as your name,
email address, username, and social login. Additionally, Coiled stores metadata
from your Dask clusters such as task counts and memory usage, similar to the
diagnostic information that is displayed in the Dask dashboard.

There are a few different types of metadata that Coiled stores to be able to
create and manage Dask clusters. Depending on the data type, this metadata is
stored in secure systems that are maintained by Coiled. The retention of this
metadata varies depending on the data type and whether it is used on an ongoing
or temporary basis.

The following metadata is stored in an encrypted database and retained on an
ongoing basis until manually deleted:

- Account/team metadata (e.g., username, email address, team accounts quotas)
- Cluster metadata (e.g., cluster size, task counts, compute time, memory usage)
- Software environment metadata (e.g., Docker image URLs, Python package
  dependencies)

The following metadata is stored in an encrypted cloud-logging service and
retained on a temporary basis then removed after 30 days:

- Cluster metadata (e.g., cluster size, task counts, compute time, memory usage)
- Software environment metadata (e.g., Docker image URLs, Python package
  dependencies)

A full description of what information is collected, as well as how we use and
do not use this information, is listed on our
`Privacy Policy <https://coiled.io/privacy-policy>`_.


Reporting
---------

Any security-related concerns can be reported to security@coiled.io.
