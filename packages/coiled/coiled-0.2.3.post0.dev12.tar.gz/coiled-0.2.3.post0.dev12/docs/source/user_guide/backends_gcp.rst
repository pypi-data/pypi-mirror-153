GCP Backend
===========

Using Coiled with GCP
---------------------

You can configure Coiled to launch Dask clusters and run computations on Google
Cloud Platform (GCP), either within Coiled's GCP account or within your own GCP
account.

.. tip::

    In addition to the usual cluster logs, our current GCP backend support also
    includes system-level logs. This provides rich insight into any potential
    issues.


Using Coiled's GCP Account
--------------------------

You can configure Coiled to launch Dask clusters and run computations within
Coiled's Google Cloud account. This makes it easy for you to get started
quickly, without needing to set up any additional infrastructure outside of
Coiled.

.. figure:: images/backend-coiled-gcp-vm.png
   :width: 100%

To use Coiled on GCP, log in to your Coiled account and access your dashboard.
Click on ``Account`` on the left navigation bar, then click the ``Edit`` button
to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

On the ``Select Your Cloud Provider`` step, select the ``GCP`` option, then
click the ``Next`` button:

.. figure:: images/cloud-backend-provider-gcp.png
   :width: 100%

On the ``Configure GCP`` step, select the GCP region that you want to use by
default (i.e., when a region is not specified in the Coiled Python client).
Continue by selecting ``Launch in Coiled's GCP Account`` and clicking the
``Next`` button. Finally, select the registry you wish to use, then click the
``Submit`` button.

Coiled is now configured to use GCP!

From now on, when you create Coiled clusters, they will be provisioned in
Coiled's GCP account.


Using your own GCP Account
--------------------------

Alternatively, you can configure Coiled to create Dask clusters and run
computations entirely within your own GCP account (within a project of your
choosing). This allows you to make use of security/data access controls,
compliance standards, and promotional credits that you already have in place
within your GCP account.

.. figure:: images/backend-external-gcp-vm.png

Note that when running Coiled on your GCP account, Coiled Cloud is only
responsible for provisioning cloud resources for Dask clusters that you create.
Once a Dask cluster is created, all computations, data transfer, and Dask
client-to-scheduler communication occurs entirely within your GCP account.

.. note::

   The ability to configure Coiled to run in your own GCP account is currently
   only available to early-adopter users. Contact
   `Coiled Support <https://docs.coiled.io/user_guide/support.html>`_ to request
   access.

.. _step-one-gcp:

Step 1: Obtain GCP service account credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled provisions resources on your GCP account through the use of a service
account that is associated with a custom IAM role (which will be created in the
next step).

In this step, you can use the GCP Console to
`create a new service account <https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating>`_
(or select an existing service account) that will be used with Coiled.

Once you have created or identified a GCP service account for working with
Coiled, you’ll need to create a new (or use an existing) JSON service account
key. Follow the steps in the GCP documentation to
`create and manage a service account key <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys>`_.

After you create a JSON service account key, the key will be saved to your local
machine with a file name such as ``gcp-project-name-d9e9114d534e.json`` with
contents similar to:

.. code-block:: json

   {
     "type": "service_account",
     "project_id": "project-id",
     "private_key_id": "25a2715d43525970fe7c05529f03e44a9e6488b3",
     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhki...asSSS5J4526eqmrkb1OA=\n-----END PRIVATE KEY-----\n",
     "client_email": "service-account-name@project-name.iam.gserviceaccount.com",
     "client_id": "102238688522576776582",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account-name%40project-name.iam.gserviceaccount.com"
   }

Keep your JSON service account key handy since you’ll use it in Coiled Cloud in
a later step.

.. _gcp-policy-doc:

Step 2: Create a custom IAM role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled requires a limited set of IAM permissions to be able to provision
infrastructure and compute resources in your GCP account. You'll need to create
a new IAM role and assign the appropriate set of permissions to it.

In this step, you'll create a new IAM role by following the steps in the GCP
documentation on
`creating a custom role <https://cloud.google.com/iam/docs/creating-custom-roles#creating_a_custom_role>`_.
Specify an IAM role name such as ``coiled`` that will make it easy to locate in
the next step.

Rather than manually adding each permission in the GCP console interface, we
recommend that you use the
`gcloud command-line tool <https://cloud.google.com/sdk/gcloud/>`_ to create a
custom role using a YAML file, which is described in the dropdown below.


.. dropdown:: Create a custom IAM role for Coiled using a YAML file
   :title: bg-white

      
   Save the below YAML to a file on your local machine called ``coiled.yaml``:

   .. code-block:: yaml

      title: coiled
      description: coiled-externally-hosted
      stage: GA
      includedPermissions:
      - bigquery.datasets.create
      - bigquery.jobs.create
      - bigquery.datasets.get
      - bigquery.datasets.update
      - compute.acceleratorTypes.list
      - compute.addresses.list
      - compute.disks.create
      - compute.disks.delete
      - compute.disks.list
      - compute.disks.useReadOnly
      - compute.firewalls.create
      - compute.firewalls.delete
      - compute.firewalls.get
      - compute.firewalls.list
      - compute.globalOperations.get
      - compute.globalOperations.getIamPolicy
      - compute.globalOperations.list
      - compute.images.create
      - compute.images.delete
      - compute.images.get
      - compute.images.list
      - compute.images.setLabels
      - compute.images.useReadOnly
      - compute.instances.create
      - compute.instances.delete
      - compute.instances.get
      - compute.instances.getSerialPortOutput
      - compute.instances.list
      - compute.instances.setLabels
      - compute.instances.setMetadata
      - compute.instances.setServiceAccount
      - compute.instances.setTags
      - compute.instanceTemplates.create
      - compute.instanceTemplates.delete
      - compute.instanceTemplates.get
      - compute.instanceTemplates.useReadOnly
      - compute.machineTypes.get
      - compute.machineTypes.list
      - compute.networks.create
      - compute.networks.delete
      - compute.networks.get
      - compute.networks.list
      - compute.networks.updatePolicy
      - compute.projects.get
      - compute.projects.setCommonInstanceMetadata
      - compute.regionOperations.get
      - compute.regionOperations.list
      - compute.regions.get
      - compute.regions.list
      - compute.routers.create
      - compute.routers.delete
      - compute.routers.get
      - compute.routers.list
      - compute.routers.update
      - compute.routes.delete
      - compute.routes.list
      - compute.subnetworks.create
      - compute.subnetworks.delete
      - compute.subnetworks.get
      - compute.subnetworks.getIamPolicy
      - compute.subnetworks.list
      - compute.subnetworks.use
      - compute.subnetworks.useExternalIp
      - compute.zoneOperations.get
      - compute.zoneOperations.list
      - compute.zones.list
      - iam.serviceAccounts.actAs
      - logging.buckets.create
      - logging.buckets.get
      - logging.buckets.list
      - logging.logEntries.create
      - logging.logEntries.list
      - logging.sinks.create
      - logging.sinks.get
      - logging.sinks.list
      - storage.buckets.create
      - storage.buckets.get
      - storage.objects.create
      - storage.objects.get
      - storage.objects.list
      - storage.objects.update

   Then, use the ``gcloud`` command to create your custom IAM role in a
   ``PROJECT-ID`` of your choosing, as in:

   .. code-block:: text

      gcloud iam roles create coiled --project=<PROJECT-ID> --file=coiled.yaml


Step 3: Connect the service account to the role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you’ve created a service account and a custom IAM role to use with Coiled,
you can bind the service account to the custom role via the
`GCP Cloud Console <https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-console>`_
or
`using the gcloud command-line tool <https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-gcloud-manual>`_,
in a terminal, as in:

.. code-block:: text

    gcloud projects add-iam-policy-binding <PROJECT-ID> \
        --member=serviceAccount:<CLIENT-EMAIL> \
        --role=projects/<PROJECT-ID>/roles/coiled


Step 4: Configure Google Artifact Registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to store the Docker containers for your software environments in
your own GCP account, Coiled stores them in the
`Google Artifact Registry (GAR) <https://cloud.google.com/artifact-registry>`_.
If you want to store your software environments in Docker Hub or another
external Docker registry, you can skip this step and configure the registry
settings in the next step.

In this step, you'll enable the Google Artifact Registry API, create a GAR
repository for Coiled, and create an IAM policy binding that grants limited
access to the service account for Coiled. Using this configuration, Coiled will
not have access to any other repositories in your GCP account, and Coiled does
not require admin-level permissions to enable APIs or create repositories.

To
`enable the Google Artifact Registry API <https://cloud.google.com/endpoints/docs/openapi/enable-api>`_,
run the following ``gcloud`` command in a terminal:

.. code-block:: text

   gcloud services enable --project=<PROJECT_ID> artifactregistry.googleapis.com

`Create a GAR repository <https://cloud.google.com/artifact-registry/docs/manage-repos#create>`_
for Coiled to use by running the following command in a terminal. Note that the
repository must be named ``coiled`` exactly as shown, and that the location should
be one that we currently support: ``us-east1`` or ``us-central1``.
If you'd like to use a different region, please get in touch with
`Coiled Support <https://docs.coiled.io/user_guide/support.html>`_.

.. code-block:: text

  gcloud artifacts repositories create coiled \
    --project=<PROJECT_ID> \
    --repository-format=docker \
    --location=<REGION>

Finally, grant access to the repository we just created:

.. code-block:: text

   gcloud artifacts repositories add-iam-policy-binding coiled \
      --project=<PROJECT_ID> \
      --location=<REGION> \
      --member=serviceAccount:<CLIENT-EMAIL> \
      --role=roles/artifactregistry.repoAdmin

.. note::

   Ensure that the region specified in the ``location`` option is the same
   region that you will use when configuring your Coiled Cloud backend in the
   next step. If you want to store software environments in multiple regions,
   then you can repeat these commands with the desired ``REGION``.

.. note::

   We've noted that it can take a few minutes for the policy binding to propagate
   (anecdotally, about 2 to 5 minutes). Keep this in mind if you quickly complete
   the next step and get an error related to Google Artifact Registry.


Optional step: Create a second service account for instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the resources you need to access while running your computation are all publicly available, then you can skip this step. If, however, you require access to private resources (e.g. BigQuery or Cloud Storage buckets), then read on.

.. warning::

   The service account that you specify when configuring your Coiled Cloud backend
   will have an unrestricted scope attached to it. Access permissions should be
   configured with IAM permissions.

By default, Coiled uses the service account that you created in the
:ref:`first step <step-one-gcp>` and attaches it to each instance created while launching
a Dask cluster. This primary service account requires a number of permissions that you configured in :ref:`step 2 <gcp-policy-doc>`, including network-related resources, firewall-related resources, and access to Cloud Storage.
Therefore, it is recommended you create a second service account (referred to as the instance service account) with permissions to
only access the resources that you need while running your computation,
such as access to BigQuery, GCP Storage buckets and so on.

.. note:: 

   If you decide to create a specific service account to be used as the
   instance service account, you should grant it the ``logging.logEntries.create``
   permission so logs can be exported from the instance to GCP Logging.

Then in the next step, when you are configuring your Coiled Cloud backend,
you can provide the email of this instance service account, and Coiled will
use this service account and attach it to each instance created.

We recommend not using the same service account as the one you provide us to create clusters, since it's best practice to grant your cluster the "least privilege" it needs and the primary service account you provide us has much stronger permissions than is needed by the code running on your cluster.


Step 5: Configure Coiled Cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you're ready to configure the cloud backend in your Coiled Cloud account to
use your GCP account and GCP service account credentials.

To configure Coiled to use your GCP account, log in to your Coiled account and
access your dashboard. Click on ``Account`` on the left navigation bar, then
click the ``Edit`` button to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

.. note::

   You can configure a different cloud backend for each Coiled account (i.e.,
   your personal/default account or your :doc:`Team account <teams>`). Be sure
   that you're configuring the correct account by switching accounts at the top
   of the left navigation bar in your Coiled dashboard if needed.

On the ``Select Your Cloud Provider`` step, select the ``GCP`` option, then
click the ``Next`` button:

.. figure:: images/cloud-backend-provider-gcp.png
   :width: 100%

On the ``Configure GCP`` step, select the GCP region that you want to use by
default (i.e., when a region is not specified in the Coiled Python client). Then
choose the ``Launch in my GCP account`` option, add your JSON service account
key file, then click the ``Next`` button.

.. figure:: images/cloud-backend-credentials-gcp.png
   :width: 100%

On the ``Container Registry`` step, select where you want to store Coiled
software environments, then click the ``Next`` button:

.. figure:: images/cloud-backend-registry-gcp.png
   :width: 100%

Review the cloud backend provider options that you've configured, then click on
the ``Submit`` button:

.. figure:: images/cloud-backend-review-gcp.png
   :width: 100%

Coiled is now configured to use your GCP Account!

From now on, when you create Coiled clusters, they will be provisioned in your
GCP account.


Step 6: Create a Coiled cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you've configured Coiled to use your GCP account, you can create a
cluster to verify that everything works as expected.

To create a Coiled cluster, follow the steps listed in the quick start on your
Coiled dashboard, or follow the steps listed in the
:doc:`Getting Started <getting_started>` documentation, both of which will walk
you through installing the Coiled Python client and logging in, then running a
command such as:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=1)

   from dask.distributed import Client

   client = Client(cluster)
   print("Dashboard:", client.dashboard_link)

.. note::

  If you're using a :doc:`Team account <teams>` in Coiled, be sure to specify
  the ``account=`` option when creating a cluster, as in:

  .. code-block:: python

     cluster = coiled.Cluster(n_workers=1, account="my-team-account-name")

  Otherwise, the cluster will be created in your personal/default account in
  Coiled, which you can access by switching accounts at the top of the left
  navigation bar in your Coiled dashboard.

Once your Coiled cluster is up and running, you can run a sample calculation on
your cluster to verify that it's functioning as expected, such as:

.. code-block:: python

   df = dd.read_parquet(
       "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.parquet",
       columns=["passenger_count", "tip_amount"],
       storage_options={"anon": True},
   ).persist()

   df.groupby("passenger_count").tip_amount.mean().compute()

At this point, Coiled will have created resources within your GCP account that
are used to power your Dask clusters.


.. _gcp_backend_options:

Backend options
---------------

There are several GCP-specific options that you can specify (listed below) to
customize Coiled’s behavior. Additionally, the next section contains an example
of how to configure these options in practice.

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - ``region``
     - GCP region to create resources in
     - ``us-east1``
   * - ``zone``
     - GCP zone to create resources in
     - ``us-east1-c``
   * - ``preemptible``
     - Whether or not to use preemptible instances for cluster workers
     - ``False``
   * - ``firewall``
     - Ports and CIDR block for the security groups that Coiled creates -
       Under active development and should be considered to be in an early experimental/testing phase
     - ``{"ports": [22, 8787, 8786], "cidr": "0.0.0.0/0"}``

The GCP backend for Coiled uses
`preemptible instances <https://cloud.google.com/compute/docs/instances/preemptible>`_
for the workers by default. Note that GCP might stop preemptible instances at
any time and always stops preemptible instances after they run for 24 hours.


Example
^^^^^^^

You can specify backend options directly in Python:

.. code-block::

    import coiled

    cluster = coiled.Cluster(backend_options={"region": "us-central1", "preemptible": False})

Or save them to your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        region: us-central1

to have them used as the default value for the ``backend_options=`` keyword:

.. code-block::

    import coiled

    cluster = coiled.Cluster()


GPU support
-----------

This backend allows you to run computations with GPU-enabled machines if your
account has access to GPUs. See the :doc:`GPU best practices <gpu>`
documentation for more information on using GPUs with this backend.

Workers currently have access to a single GPU, if you try to create a cluster
with more than one GPU, the cluster will not start, and an error will be
returned to you.

.. _logs-gcp:

Coiled logs
-----------

If you are running Coiled on your GCP account, cluster logs will be saved within
your GCP account. Coiled will send logs to 
`GCP Logging <https://cloud.google.com/logging/>`_ and
`GCP BigQuery <https://cloud.google.com/bigquery/>`_ 
(if BigQuery is enabled in the project).

We send logs to GCP Logging so that you can easily view logs with GCP Logs Explorer,
and we use GCP Cloud Storage/GCP BigQuery to back the logs views we display on the
`Cluster Dashboard <https://cloud.coiled.io/>`_.

.. note::

   Coiled will only use BigQuery if you have BigQuery enabled in your project and if
   you have the following permissions in your service account: ``bigquery.datasets.create``,
   ``bigquery.datasets.get``, ``bigquery.datasets.update`` and ``bigquery.jobs.create``

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Log Storage
     - Storage time
   * - ``GCP Logging``
     - 30 days
   * - ``GCP Cloud Storage (Coiled v1)``
     - 90 days
   * - ``GCP BigQuery dataset (Coiled v2)``
     - 10 days

When you configure your backend to use GCP, Coiled creates a bucket
named ``coiled-logs`` GCP Logging.

Networking
----------

.. warning::

   The features below are currently under active development and should be
   considered to be in an early experimental/testing phase.

When Coiled is configured to run in your own GCP account, you can customize the
firewall ingress rules for resources that Coiled creates in your GCP
account.

By default, Dask schedulers created by Coiled will be reachable via ports 22,
8787 and 8786 from any source network. This is consistent with the default
ingress rules that Coiled configures for its GCP firewalls:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Protocol
     - Port
     - Source
   * - tcp
     - 8787
     - ``0.0.0.0/0``
   * - tcp
     - 8786
     - ``0.0.0.0/0``
   * - tcp
     - 22
     - ``0.0.0.0/0``

.. note::
    Ports 8787 and 8786 are used by the Dask dashboard and Dask protocol respectively.
    Port 22 optionally supports incoming SSH connections to the virtual machine.

Configuring firewall rules
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   This feature is currently under active development and should be considered
   to be in an early experimental/testing phase.

While allowing incoming connections on the default Dask ports from any source
network is convenient, you might want to configure additional security measures
by restricting incoming connections. This can be done by using
:meth:`coiled.set_backend_options` or by using the ``backend_options``.
