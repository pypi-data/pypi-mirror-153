======================================
Setting Backend Options via Python API
======================================

This article will show you how you can use the Python API to set backend
options.

Coiled allows users to configure the cloud computing resources they wish
to use (their "backend") via the ``set_backend_options()`` function. This
function returns the current account username when invoked
and controls backend settings via keyword arguments.  Backend options,
when changed via the Python api will be reflected in the Coiled Cloud
UI, and will persist until changed again via the UI or via
``coiled.set_backend_options()``.

Using coiled.set_backend_options
--------------------------------

This function is fully documented in the `API Reference  <https://docs.coiled.io/user_guide/api.html#>`_ section
of the Coiled documentation; this tutorial provides some example usage as a
supplement to that.

Called without arguments, it returns the current username, and will apply
default keyword arguments.

.. code:: python

    import coiled

    coiled.set_backend_options()

In this case, that will set ``backend='aws'``, ``registry_type='ecr'``
and ``aws_region='us-east-1'``.

Note that these currently differ slightly from the the default Coiled Cloud
backend options when they are configured via the Cloud UI.
(see ``use_coiled_defaults`` below).

To set all backend options to correspond to the Coiled Cloud UI backend defaults,
selecting the AWS VM backend with ECR registry, use:

.. code:: python

    coiled.set_backend_options(backend="aws")


Note that this will also reset other keyword arguments with defaults,
most notably ``registry_type='ecr'``.

To set all backend options to correspond to the Coiled Cloud UI backend defaults, 
selecting the AWS VM backend with ECR registry, use:

.. code:: python

    coiled.set_backend_options(use_coiled_defaults=True)

To specifically set the backend to the Coiled-hosted AWS VM backend:

.. code:: python

    coiled.set_backend_options(backend="aws")

To set the backend to use user-provided credentials in an AWS VM backend:

.. code:: python

    coiled.set_backend_options(
        backend="aws",
        customer_hosted=True,
        aws_access_key_id="#-your-access-key-ID#",
        aws_secret_access_key="######-your-aws-secret-access-key-######",
    )


Use care with any code including private credentials in plain text. 
Note that it is important to include ``customer_hosted=True`` as it will
otherwise default to ``False``, and leave the backend within the 
Coiled-hosted AWS VM account.


Additional settings
-------------------

Regions
^^^^^^^

Other settings can be changed via ``coiled.set_backend_options``. For instance,
AWS regions can also be set:

.. code:: python

    coiled.set_backend_options(aws_region="us-west-1")

For a list of supported regions, see the 
`AWS backend documentation  <https://docs.coiled.io/user_guide/backends_aws.html>`_.

Container Registries
^^^^^^^^^^^^^^^^^^^^

It is also possible to specify a Docker registry for your software
environments. For example, to use Docker Hub:

.. code:: python

    coiled.set_backend_options(
        registry_type="docker_hub",
        registry_uri="docker.io",
        registry_username="your-registry-username",
        registry_access_token="#######-registry-access-token-######",
    )

In using the preceding, keep in mind default Python behavior, which will reset
keyword arguments ``backend='aws'``, ``registry_type='ecr'``,
``aws_region='us-east-1'`` and ``registry_uri='docker.io'`` if they are not
explicitly included in the call.  So, if the goal is to use a user specified
Docker Hub container registry while working in GCP, that keyword argument must
also be set:

.. code:: python

    coiled.set_backend_options(
        backend="gcp",
        registry_type="docker_hub",
        registry_username="your-registry-username",
        registry_access_token="#######-registry-access-token-######",
    )

Networking
^^^^^^^^^^

.. note::
  This feature is available to all cloud providers that Coiled supports.

You can configure custom networking options when Coiled is configured to run in
your own AWS account. This allows you to customize the security group ingress
rules for resources that Coiled creates in your cloud provider account. 
For example, you have fine-grain control over the security
group by specifying which ports and CIDR block to use when Coiled creates a
security group.:

.. code:: python

    coiled.set_backend_options(
        backend="aws",
        aws_access_key_id="<your-access-key-id-here>",
        aws_secret_access_key="<your-access-key-secret-here>",
        customer_hosted=True,
        ingress=[{"ports": [100, 8754], "cidr": "10.0.5.1/16"}],
    )

For more details on AWS networking, refer to the networking section of the
:doc:`../backends_aws`


