=====================
Configuring firewalls
=====================

By default, when you create a Dask cluster with Coiled, it is configured to
allow incoming network connections on the default Dask ports from any source
network for the sake of convenience. For additional security, you can restrict
incoming connections to Dask clusters using the ``ingress`` option. This option
can be used to specify the account-level default firewall settings for all newly
created clusters via ``set_backend_options``, or this option can be used when
creating a cluster via the ``backend_options`` in ``coiled.Cluster``.

Opening ports for a specific CIDR block
---------------------------------------

If you need more control over the security groups or firewalls for Dask clusters
created by Coiled, use the ``ingress`` argument to specify ingress rules for a
source ``cidr`` block for a specified list of ``ports``. If you configure the
``ingress`` setting, then Coiled will use these firewall rules as each new Dask
cluster and its associated security group are created.

Note that ``ingress`` is a list, so you can open different ports to different CIDR blocks.
This can be useful if (for instance) you need to open access to a VPN with one CIDR and a
paired VPC with a different CIDR block.

For example, you can use ``backend_options`` to specify Coiled account-level
default firewall settings:

.. code-block:: python

  import coiled

  coiled.set_backend_options(
      backend="aws",
      aws_access_key_id="<your-access-key-id-here>",
      aws_secret_access_key="<your-access-key-secret-here>",
      customer_hosted=True,
      ingress=[{"ports": [8786, 8787], "cidr": "10.1.0.2/16"}],
      account="my-team-account-name",  # if you are using a Coiled team account
  )

which will result in the following ingress rules configured for all newly
created Dask clusters in your Coiled account:

.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - Protocol
      - Port
      - Source
    * - tcp
      - 8787
      - ``10.1.0.2/16``
    * - tcp
      - 8786
      - ``10.1.0.2/16``

You can also use the ``backend_options`` option to modify the firewall settings
for a specific cluster. Here's an example with also demonstrates opening multiple
CIDR blocks:

.. code-block::

    import coiled

    coiled.Cluster(
        backend_options={
            "ingress": [
                {
                    "ports": [8786],  # client -> scheduler
                    "cidr": "10.1.0.2/16"
                },
                {
                    "ports": [8787],  # scheduler dashboard
                    "cidr": "10.32.0.0/16"
                },
            ]
        }
    )

Or, you can specify ``ingress`` settings in your
:ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        ingress: [{
                "ports": [8786, 8787],
                "cidr": "10.1.0.2/16"
            }]

Connecting on a private IP address
----------------------------------

By default the Coiled client will attempt to connect to the Dask scheduler using its public IP address, which causes
traffic to be routed over the public internet. If you wish traffic between the Coiled client and the Dask scheduler to
be routed over a private network you can pass the ``use_scheduler_public_ip`` argument to ``coiled.Cluster`` calls:

.. code-block:: python

    import coiled

    coiled.Cluster(use_scheduler_public_ip=False)

If you wish to set this behaviour as default, you can set this in your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      use_scheduler_public_ip: false



Custom networking setups
------------------------

If you have more complex security or networking requirements and prefer to use
an existing VPC, subnets, and security groups, refer to the the
:doc:`bring your own network functionality <bring_your_own_network>`.
