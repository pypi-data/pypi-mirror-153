Configuring AWS
===============

This guide assumes you have already `created your Coiled account <https://cloud.coiled.io/signup>`_
and created an AWS account. If you don't have an AWS account, you can sign up for
`AWS Free Tier <https://aws.amazon.com/free>`_.

In this guide you will configure Coiled to run Dask computations entirely within
your own AWS account. This includes the following steps:

1. Sign in to the Console
2. Create a new IAM user
3. Create IAM policies
4. Attach IAM policies
5. Obtain AWS credentials
6. Configure Coiled Cloud backend
   
.. Watch the video below to follow along:

.. .. raw:: html

..     <div style="display: flex; justify-content: center;" title="How to create an IAM user">
..     <iframe width="560" height="315" src="https://www.youtube.com/embed/BsQK5_y1nvE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
..     </div>

1. Sign in to the Console
^^^^^^^^^^^^^^^^^^^^^^^^^

Sign in to the `AWS console <https://console.aws.amazon.com>`_ as the root user (see `these instructions <https://docs.aws.amazon.com/IAM/latest/UserGuide/console.html#root-user-sign-in-page>`_ in the AWS documentation if you're having trouble).
To learn more, see the `AWS documentation on root users <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html>`_.

2. Create a new IAM user
^^^^^^^^^^^^^^^^^^^^^^^^

Follow the steps in the `AWS guide on creating a new IAM user <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console>`_. This IAM user must have `programmatic access <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_. Creating an IAM role with `temporary access keys <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#temporary-access-keys>`_ will not be sufficient.

.. _aws-iam-policy:

3. Create IAM policies
^^^^^^^^^^^^^^^^^^^^^^

Coiled requires a limited set of IAM permissions to provision
infrastructure and compute resources in your AWS account.
Follow the steps in the
`AWS user guide on how to create new IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor>`_. 

We'll create two policies, one for initial setup and another for ongoing use.
When you arrive at the step to insert a JSON policy document, copy and paste
the following JSON policy documents. You can name them ``coiled-setup`` and ``coiled-ongoing``,
respectively, to make them easy to locate in the next step.

.. dropdown:: AWS IAM Setup policy document (JSON)

  .. literalinclude:: ../../../../backends/policy/aws-required-policy-setup.json
    :language: json

.. dropdown:: AWS IAM Ongoing policy document (JSON)

  .. literalinclude:: ../../../../backends/policy/aws-required-policy-ongoing.json
    :language: json

4. Attach IAM policies
^^^^^^^^^^^^^^^^^^^^^^

Now that you have created the two IAM policies with all necessary permissions,
you can attach these policies to the IAM user you created in step 2. Follow the steps in the
`AWS user guide on attaching IAM identity permissions <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console>`__.

5. Obtain AWS credentials
^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled provisions resources on your AWS account through the use of AWS security
credentials. Select the user you created in step 2. Follow the steps in the
`AWS user guide on programmatic access <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_
to obtain (or create) your access key ID and secret access key. They will resemble the
following:

.. code-block:: text

   Example AWS Secret Access ID: AKIAIOSFODNN7EXAMPLE
   Example AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

Keep these credentials handy since you will configure them in Coiled Cloud
in the next step.

.. note::
    The AWS credentials you supply must be long-lived (not temporary) tokens.

.. _aws configure account backend:

6. Configure Coiled Cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you're ready to configure the cloud backend in your Coiled account to
use your AWS account.

First, `log in to your Coiled account <https://cloud.coiled.io/login>`_.
In the navigation bar on the left, click on ``Setup``. Select
``Cloud Backend Options``, then click the ``Edit`` button:

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

On the ``Configure AWS`` step, select your default AWS region
(i.e., when a region is not specified in the Coiled Python client).
Select the ``Launch in my AWS account`` option, input your ``AWS Access Key ID``
and ``AWS Secret Access Key`` from the previous step, then click the ``Next``:

.. figure:: images/cloud-backend-credentials.png
   :width: 100%

On the ``Container Registry`` step, select whether you want to store Coiled
software environments in Amazon ECR or Docker Hub, then click ``Next``:

.. figure:: images/cloud-backend-registry.png
   :width: 100%

Review your cloud backend provider options, then click the ``Submit`` button:

.. figure:: images/cloud-backend-review.png
   :width: 100%

On the next page, you will see the resources provisioned by Coiled in real time.
This initial process can take up to 20 minutes.

Next Steps
^^^^^^^^^^
Congratulations, Coiled is now configured to use your AWS account!

.. note::
   Now that you have completed these configuration steps, you can
   detach the ``coiled-setup`` policy to restrict Coiled to only
   use the IAM permissions defined in the ``coiled-ongoing`` policy.

Follow the :doc:`Getting Started tutorial <getting_started>` to create a Coiled
cluster and run a computation. When you create your first cluster,
Coiled will create a new VPC, subnets, AMI, EC2 instances,
and other resources on your AWS account that are used to power your Dask
clusters (see :doc:`aws_reference` for a more detailed description of these resources and additional configuration options).