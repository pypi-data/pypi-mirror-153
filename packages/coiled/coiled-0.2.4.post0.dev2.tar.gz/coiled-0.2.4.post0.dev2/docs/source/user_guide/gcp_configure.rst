Configuring GCP
===============

This guide assumes you have already `created your Coiled account <https://cloud.coiled.io/signup>`_
and created a Google Cloud Platform (GCP) account. If you don't have a GCP account, you can
`sign up for a Free Tier account <https://cloud.google.com/free>`_. You should also make
sure you already have the `gcloud CLI installed <https://cloud.google.com/sdk/docs/install>`_.

In this guide you will configure Coiled to run Dask computations entirely within
your own GCP account. This includes the following steps:

1. Sign in to the console
2. Create an IAM custom role
3. Create a service account
4. Create a service account key
5. Optional: Create a second service account for instances
6. Configure Google Artifact Registry
7. Configure Coiled cloud backend

.. Watch the video below to follow along:

.. .. raw:: html

..     <div style="display: flex; justify-content: center;" title="How to create an IAM user">
..     <iframe width="560" height="315" src="https://www.youtube.com/embed/BsQK5_y1nvE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
..     </div>

1. Sign in to the console
^^^^^^^^^^^^^^^^^^^^^^^^^
Sign in to the `Cloud Console <https://console.cloud.google.com/>`_.
See this `Google Cloud console reference <https://cloud.google.com/storage/docs/cloud-console>`_ for the different ways to access the Cloud console.

.. _gcp-iam-role:

2. Create an IAM custom role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Coiled requires a limited set of IAM permissions to provision
infrastructure and compute resources in your GCP account. We recommend
creating a IAM custom role to align with the principle of least privilege
(see the `Google Cloud documentation on understanding IAM custom roles <https://cloud.google.com/iam/docs/understanding-custom-roles>`_).

.. important::
    Ask your administrator to grant you the Role Administrator IAM role (``roles/iam.roleAdmin``)
    for a project or Organization Role Administrator IAM role (``roles/iam.organizationRoleAdmin``) for an organization
    (see the `Google Cloud documentation on required roles <https://cloud.google.com/iam/docs/creating-custom-roles#required-roles>`_).

Follow the steps in the Google Cloud documentation on
`creating a custom role <https://cloud.google.com/iam/docs/creating-custom-roles#creating_a_custom_role>`_.
Select the ``gcloud`` tab and follow the instructions using the gcloud CLI to
create a custom role using a YAML file using the YAML file in dropdown below:

.. dropdown:: Create an IAM custom role using a YAML file
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
``PROJECT-ID`` of your choosing:

.. code-block:: text

   gcloud iam roles create coiled --project=<PROJECT-ID> --file=coiled.yaml

.. _create-service-account:

3. Create a service account
^^^^^^^^^^^^^^^^^^^^^^^^^^^
A service account provides the necessary identity and authentication for running Coiled (see the `Google Cloud documentation on service accounts best practices <https://cloud.google.com/iam/docs/best-practices-for-using-and-managing-service-accounts>`_).
In this step you will create a service account. During this process, you will also grant the IAM role you created in the previous step to this service account.
Follow the steps in the Google Cloud documentation on `creating a service account <https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating>`_, selecting the ``Console`` tab.

.. important::
    Ask your administrator to grant you the Service Account Admin (``roles/iam.serviceAccountAdmin``) IAM role on the project
    (see the `Google Cloud documentation on permissions <https://cloud.google.com/iam/docs/creating-managing-service-accounts#permissions>`_).

When you get to step 6 "Optional: Choose one or more IAM roles to grant to the service account on the project", choose the ``coiled`` IAM custom role you just created.

.. note::
    You can also bind the service account to the IAM custom role at any time using the 
    `Console <https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-console>`_ or `gcloud CLI <https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-gcloud-manual>`_:

    .. code-block:: bash

        gcloud projects add-iam-policy-binding <PROJECT-ID> \
            --member=serviceAccount:<CLIENT-EMAIL> \
            --role=projects/<PROJECT-ID>/roles/coiled

4. Create a service account key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once you have a service account for working with
Coiled, you will need to create a JSON service account
key. Follow the steps in the Google Cloud documentation to
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

Keep your JSON service account key handy since you will use it to configure the Coiled Cloud backend in the last step.

5. Optional: Create a second service account for instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the resources you need to access while running your computation are publicly available, then you can skip this step.
If, however, you require access to private resources (e.g. BigQuery or Cloud Storage buckets), then read on.

By default, Coiled uses the service account that you created in the
:ref:`previous step <create-service-account>` and attaches it to each instance created while launching
a Dask cluster. This primary service account requires a number of permissions that you configured in
:ref:`gcp-iam-role`, including network-related resources, firewall-related resources, and access to Cloud Storage.
Therefore, it is recommended you create a second service account (referred to as the instance service account) with permissions to
only access the resources that you need while running your computation, such as access to BigQuery, Cloud Storage buckets and so on.

.. note:: 
   If you decide to create a specific service account to be used as the
   instance service account, you should grant it the ``logging.logEntries.create``
   permission so logs can be exported from the instance to GCP Logging.

Then in the step where you :ref:`configure your Coiled Cloud backend <coiled-cloud-backend>`,
you can provide the email of this instance service account, and Coiled will
use this service account and attach it to each instance created.

We recommend not using the same service account as the one you provide us to create clusters,
since it's best practice to grant your cluster the "least privilege" it needs and the primary service account
you provide us has much stronger permissions than is needed by the code running on your cluster.

6. Configure Google Artifact Registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to store the Docker containers for your software environments in
your own GCP account, Coiled stores them in the
`Google Artifact Registry (GAR) <https://cloud.google.com/artifact-registry>`_.
If you want to store your software environments in Docker Hub or another
external Docker registry, you can skip this step and configure the registry
settings when you :ref:`configure your Coiled Cloud backend <coiled-cloud-backend>`.

In this step, you'll enable the Google Artifact Registry (GAR) API, create a GAR
repository for Coiled, and create an IAM policy binding that grants limited
access to the service account for Coiled. Using this configuration, Coiled will
not have access to any other repositories in your GCP account, and Coiled does
not require admin-level permissions to enable APIs or create repositories.

To
`enable the Google Artifact Registry API <https://cloud.google.com/endpoints/docs/openapi/enable-api>`_,
run the following ``gcloud`` command in a terminal:

.. code-block:: bash

   gcloud services enable --project=<PROJECT_ID> artifactregistry.googleapis.com

`Create a GAR repository <https://cloud.google.com/artifact-registry/docs/manage-repos#create>`_
for Coiled to use by running the following command in a terminal. Note that the
repository must be named ``coiled`` exactly as shown, and that the location should
be one that we currently support: ``us-east1`` or ``us-central1``.
If you'd like to use a different region, please get in touch with
`Coiled Support <https://docs.coiled.io/user_guide/support.html>`_.

.. code-block:: bash

  gcloud artifacts repositories create coiled \
    --project=<PROJECT_ID> \
    --repository-format=docker \
    --location=<REGION>

Finally, grant access to the repository we just created:

.. code-block:: bash

   gcloud artifacts repositories add-iam-policy-binding coiled \
      --project=<PROJECT_ID> \
      --location=<REGION> \
      --member=serviceAccount:<CLIENT-EMAIL> \
      --role=roles/artifactregistry.repoAdmin

.. note::
   Ensure that the region specified in the ``location`` option is the same
   region you use when you
   :ref:`configure your Coiled Cloud backend <coiled-cloud-backend>`.
   If you want to store software environments in multiple regions,
   then you can repeat these commands with the desired ``REGION``.

It can take a few minutes for the policy binding to propagate.
Keep this in mind if you quickly complete the next step and get
an error related to Google Artifact Registry.

.. _coiled-cloud-backend:

7. Configure Coiled Cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now you're ready to configure the cloud backend in your Coiled Cloud account to
use your GCP account and GCP service account credentials.

To configure Coiled to use your GCP account, log in to your Coiled account and
access your dashboard. Click on ``Setup`` on the left navigation bar, then
click the ``Edit`` button to configure your Cloud Provider Configuration:

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

Next Steps
^^^^^^^^^^
Congratulations, Coiled is now configured to use your GCP account!

Follow the :doc:`Getting Started tutorial <getting_started>` to create a Coiled
cluster and run a computation. See :doc:`gcp_reference` for a more detailed
description and additional configuration options.