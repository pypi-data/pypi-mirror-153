==================================================
How to limit Coiled's access to your AWS resources
==================================================

This article aims to provide you with some guidance on how to limit our access
to your AWS resources and handle permissions in different phases of your
pipeline. We will also talk briefly about the permissions you configured
initially (see :doc:`../aws_configure`).

Permissions
-----------

On the backends, AWS documentation, you can find an IAM policy template under
:ref:`Using your AWS account <aws-iam-policy>`, this template contains two
sets of permissions - **Setup** and **Ongoing**.

The Setup set is used to set up all the network resources and roles that Coiled
will use when launching a cluster in your AWS account. Once you've input your
credentials and successfully created a Coiled cluster in your AWS account,
you can remove this set of permissions in the future once Coiled has created
all the needed resources for you.

The Ongoing set contains the permissions that Coiled needs to launch clusters in
your account.  Here you find permissions related to software environments, getting
logs and so on.

.. note::

  Most of the resources that Coiled creates will contain the tag ``owner: coiled``
  to allow you to identify what we created.

Giving access
-------------

If you use your AWS credentials, data is run within your VPC as described in our
:doc:`Security section <../security>`. If you want to limit Coiled's access to
your AWS resources even further, you can do this with users and roles.

By `creating a user <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html>`_
within your AWS account, you can give access to only those resources that you are comfortable
sharing. Then you can `create different roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_
that have a more restricted set of permissions.

.. note::

  If you have an AWS Organization, you might need to follow the
  `AWS documentation <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html>`_
  on creating an account in your organization.

Example: S3 restrictions
^^^^^^^^^^^^^^^^^^^^^^^^

Let's assume that you have created a ``coiled`` user in your AWS account. This
user has read permissions to an S3 bucket that you own, but you created a role
that doesn't allow access to the bucket.

.. code:: python

    import coiled
    import dask.dataframe as dd
    from dask.distributed import Client

    cluster = coiled.Cluster()
    client = Client(cluster)

    df = dd.read_csv("s3://your-s3-url-here")

If you switch to the role that doesn't allow access to S3,  the code above will
fail with a permissions error.
