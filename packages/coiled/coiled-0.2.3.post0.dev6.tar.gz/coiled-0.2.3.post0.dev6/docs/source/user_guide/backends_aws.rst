AWS Backend
===========

Using Coiled's AWS account
--------------------------

When you sign up for a Coiled Cloud account, your Dask clusters and computations
will run within Coiled's AWS account by default. This makes it easy for you to
get started quickly without having to set up any additional infrastructure or
AWS credentials.

.. figure:: images/backend-coiled-aws-vm.png
   :width: 100%

If you configured a different cloud backend option in your account at some
point, you can return to the default mode of running on Coiled's AWS account by
clicking on ``Account`` on the left navigation bar, then clicking on
``Reset to Default``.

.. figure:: images/cloud-backend-reset.png
   :width: 100%


Using your own AWS account
--------------------------

Alternatively, you can configure Coiled to create Dask clusters and run
computations entirely within your own AWS account. This allows you to make use
of security/data access controls, compliance standards, and promotional credits
that you already have in place within your AWS account.

.. figure:: images/backend-external-aws-vm.png
   :width: 100%

Note that when running Coiled on your AWS account, Coiled Cloud is only
responsible for provisioning cloud resources for Dask clusters that you create.
Once a Dask cluster is created, all computations, data transfer, and Dask
client-to-scheduler communication occurs entirely within your AWS account.

Step 1: Obtain AWS credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled provisions resources on your AWS account through the use of AWS security
credentials.

From your AWS Console, create a new (or select an existing) IAM user that will
be used with Coiled.

Once you have created or identified an IAM user for working with Coiled, you'll
need to create new (or use existing) AWS access keys. Follow the steps in the
`AWS documentation on programmatic access <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_
to obtain your access key ID and secret access key, which will be similar to the
following:

.. code-block:: text

   Example AWS Secret Access ID: AKIAIOSFODNN7EXAMPLE
   Example AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

Keep your security credentials handy since you'll configure them in Coiled Cloud
in a later step.

.. note::

    The AWS credentials you supply must be long-lived (not temporary) tokens.


Step 2: Configure AWS IAM policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _aws-iam-policy:

Coiled requires a limited set of IAM permissions to be able to provision
infrastructure and compute resources in your AWS account.

From your AWS Console, you can create new IAM policies by following the steps in
the
`AWS documentation on creating policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor>`_.
Specify IAM policy names such as ``coiled-setup`` and ``coiled-ongoing`` that
will be easy to locate in the next step.

When you arrive at the step to insert a JSON policy document, you can copy/paste
the following JSON policy documents that contain all of the permissions that
Coiled requires to be able to create and manage Dask clusters in your AWS
account:

.. dropdown:: AWS IAM Setup policy document (JSON)

  .. literalinclude:: ../../../../backends/policy/aws-required-policy-setup.json
    :language: json

.. dropdown:: AWS IAM Ongoing policy document (JSON)

  .. literalinclude:: ../../../../backends/policy/aws-required-policy-ongoing.json
    :language: json

.. note::

   During initial Coiled setup, you'll need to attach both of these policies to
   your IAM user in the following step. After the initial Coiled setup is
   complete and you've completed all of the steps on this documentation page,
   you can detach the Setup policy if you want to restrict Coiled to only be
   able to use the IAM permissions defined in the ongoing policy.


Step 3: Attach AWS IAM policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you've created an IAM policy to use with Coiled, attach the IAM policy to a
user, group, or role in your account by following the steps in the
`AWS documentation on adding IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console>`__.

However you choose to attach the IAM policy to a user, group, or role - be sure
to verify that that the AWS credentials that you configured earlier are attached
to your new IAM policy that will be used with Coiled.


.. _aws configure account backend:

Step 4: Configure Coiled Cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you're ready to configure the cloud backend in your Coiled Cloud account to
use your AWS account and AWS credentials.

To configure Coiled to use your AWS account, log in to your Coiled account and
access your dashboard. Click on ``Account`` on the left navigation bar, then
click the ``Edit`` button to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

.. note::

   You can configure a different cloud backend for each Coiled account (i.e.,
   your personal/default account or your :doc:`Team account <teams>`). Be sure
   that you're configuring the correct account by switching accounts at the top
   of the left navigation bar in your Coiled dashboard if needed.

On the ``Select Your Cloud Provider`` step, select the ``AWS`` option, then
click the ``Next`` button:

.. figure:: images/cloud-backend-provider.png
   :width: 100%

On the ``Configure AWS`` step, select the AWS region that you want to use by
default (i.e., when a region is not specified in the Coiled Python client),
choose the ``Launch in my AWS account`` option, input your ``AWS Access Key ID``
and ``AWS Secret Access Key`` from the earlier step, then click the ``Next``
button:

.. figure:: images/cloud-backend-credentials.png
   :width: 100%

On the ``Container Registry`` step, select whether you want to store Coiled
software environments in Amazon ECR or Docker Hub based on your preference, then
click the ``Next`` button:

.. figure:: images/cloud-backend-registry.png
   :width: 100%

Review the cloud backend provider options that you've configured, then click
the ``Submit`` button:

.. figure:: images/cloud-backend-review.png
   :width: 100%

On the next page, you will see the resources provisioned by Coiled in real time.
This initial process can take up to 20 minutes.

Coiled is now configured to use your AWS account!

From now on, when you create Coiled clusters, they will be provisioned in your
AWS account.


Step 5: Create a Coiled cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you've configured Coiled to use your AWS account, you can create a
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

At this point, Coiled will have created a new VPC, subnets, AMI, EC2 instances,
and other resources on your AWS account that are used to power your Dask
clusters. A more detailed description of those AWS resources is provided in the
next section.

.. warning::

  If you are trying to read from an S3 bucket and are getting permissions error
  you might need to attach S3 policies to the role that Coiled creates to be
  attached to EC2 instances.

  The role name that Coiled creates is the same as your account slug.


AWS resources
-------------

When you create a Dask cluster with Coiled on your own AWS account, Coiled will
provision the following resources on your AWS account:

.. figure:: images/backend-coiled-aws-architecture.png
   :width: 90%

   AWS resources for a Dask cluster with 5 workers

When you create additional Dask clusters with Coiled, then another scheduler VM
and additional worker VMs will be provisioned within the same public and private
subnets, respectively. As you create additional Dask clusters, Coiled will reuse
and share the existing VPC and other existing network resources that were
initially created.

.. seealso::

  If you encounter any issues when setting up resources, you can use the method
  :meth:`coiled.get_notifications` to have more visibility into this process.
  You might also be interested in reading our
  :doc:`Troubleshooting guide <troubleshooting/visibility_resource_creation>`.

.. seealso::

  You might be interested in reading the tutorial on
  :doc:`How to limit Coiled's access to your AWS resources <tutorials/aws_permissions>`.

  You might be interested in reading the tutorial on
  :doc:`Managing resources created by Coiled <tutorials/resources_created_by_coiled>`.


.. _aws_backend_options:

Backend options
---------------

There are several AWS-specific options that you can specify (listed below) to
customize Coiled's behavior. Additionally, the next section contains an example
of how to configure these options in practice.

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - ``region``
     - AWS region to create resources in
     - ``us-east-1``
   * - ``zone``
     - AWS Availability Zone to create cluster
     - depends on region
   * - ``spot``
     - Whether or not to use spot instances for cluster workers
     - ``False``
   * - ``firewall``
     - Ports and CIDR block for the security groups that Coiled creates -
       Under active development and should be considered to be in an early experimental/testing phase
     - ``{"ports": [22, 8787, 8786], "cidr": "0.0.0.0/0"}``


The currently supported AWS regions are:

* ``us-east-1``
* ``us-east-2``
* ``us-west-1``
* ``us-west-2``
* ``ap-southeast-1``
* ``ca-central-1``
* ``ap-northeast-1``
* ``ap-northeast-2``
* ``ap-south-1``
* ``ap-southeast-1``
* ``ap-southeast-2``
* ``eu-central-1``
* ``eu-north-1``
* ``eu-west-1``
* ``eu-west-2``
* ``eu-west-3``
* ``sa-east-1``

.. note::

  Coiled will choose the ``us-east-1`` region by default. If you don't
  wish to use this region, you should provide a different region.

.. _backend_options_example:

Example
^^^^^^^

You can specify backend options directly in Python:

.. code-block::

    import coiled

    cluster = coiled.Cluster(backend_options={"region": "us-west-1"})

Or save them to your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        region: us-west-1

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
returned.

.. _logs-aws:

Coiled logs
-----------

If you are running Coiled on your own AWS account, cluster logs will be saved
within your AWS account. Coiled will use
`CloudWatch <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html>`_
to store logs.

Coiled will create a log group with your account name and add a log stream for
each instances that Coiled creates. These logs will be stored for 30 days.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Log Storage
     - Storage time
   * - ``Cloudwatch``
     - 30 days


Availability Zone
-----------------

.. warning::

   The features below are currently under active development and should be
   considered to be in an early experimental/testing phase.

The availability of different VM instance types varies across AZs, so choosing a different AZ may make it easier to create a cluster with the desired number and type of instances.

This option allows you to pick the `Availability Zone <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-availability-zones>`_ (AZ) to use for a cluster. Each AZ is one or more distinct data centers located within a region. For example, the ``us-east-1`` region contains the ``us-east-1a`` zone, (as well as ``b``, ``c``, ``d``, and ``f`` zones).

You can specify the zone to use when creating an individual cluster like so:

.. code-block::

    cluster = coiled.Cluster(backend_options={'zone':'us-east-1b'})

In order to create a Dask cluster in a given AZ, we need a subnet for that specific zone.

When you configure Coiled to use your AWS account (as described :ref:`above <aws configure account backend>`), Coiled attempts to create a subnet for every zone in the selected region instead of just the default zone (note that there are no additional AWS or Coiled costs associated with each subnet).

When creating a Dask cluster, you can specify the zone to use for that cluster. Ideally the specified zone already has the required subnet (created when you configured Coiled to use your AWS account) but if not, we'll attempt to create a subnet at cluster-creation time. This may fail if Coiled no longer has "setup" IAM permissions; you'll get an error message if we are unable to find or create a subnet in the specified zone.

Assuming we are able to find or create the required subnet, then we'll then create your Coiled cluster in the specified availability zone.

If no zone is specified when creating an individual cluster, we'll use the ``zone`` set at the account level (currently this can only be set if you configure your account backend using the the Python API), and if that isn't set, we'll use the default zone for the region your account is configured to use.

Refer to the AWS documentation on `Regions and Availability Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html>`_ for additional information.

Networking
----------

.. warning::

   The features below are currently under active development and should be
   considered to be in an early experimental/testing phase.

When Coiled is configured to run in your own AWS account, you can customize the
security group ingress rules for resources that Coiled creates in your AWS
account.

By default, Dask schedulers created by Coiled will be reachable via ports 22,
8787 and 8786 from any source network. This is consistent with the default
ingress rules that Coiled configures for its AWS security groups:

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
