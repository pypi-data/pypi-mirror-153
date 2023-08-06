======================
Bring your own network
======================

.. note::
  This feature is currently experimental, with new features under active
  development.

Usually Coiled creates all the cloud networking resources required for running a cluster. For customers who are hosting Coiled in their own AWS or GCP account, we also provide the option to have Coiled use an existing network which you have created.

While this means you're responsible managing more aspects of hosting Coiled, it also enables you to run Coiled while meeting specific needs for network security or configuration, such as:

- you need to peer the VPC used for Coiled clusters with other networks
- you need to configure additional network security, for example, routing traffic through a customer-managed firewall or limiting inbound connections to a VPN
- you need to configure network access to your data sources, for example, using AWS PrivateLink
- you need to limit the IAM permissions that you grant to Coiled

If you provide a network for Coiled to use, you'll be responsible for:

- VPC
- subnet(s)
- routing and internet access (including NAT for VMs without public IP address)
- security groups (AWS) or firewall rules (GCP)

If you provide a network, Coiled will still be responsible for creating VMs (and associated storage, network interface, and public IPs) as well as machine images and Docker images (for your software environments).

You can configure Coiled to use your network when setting your **Cloud Backend Options**  on the **Account** page on `cloud.coiled.io <https://cloud.coiled.io>`_, or you can :ref:`byo-net-python-api` as explained below.


Network requirements
--------------------

See :ref:`network-architecture` for details about the networking needs of a Coiled cluster.

The network you provide for Coiled to use needn't match the networks we create by default, but they do need to meet some minimal requirements.

Our default network allows public ingress to the scheduler on ports 8786 and 8787. This isn't a requirement, so long as the machine running the Python client is able to connect to the scheduler. For instance, you could be running the client on a machine inside a paired VPC or go through a VPC which allows you to connect to private IP of the scheduler. Ports 8786, 8787 need to be open for ingress so that the client can connect to scheduler.

It's necessary that the scheduler and workers be able to download software (as well of course as any data used in your computations). This can be achieved by using a NAT Gateway which is set as next hop for outbound connections, but it can also be achieved by allowing us to assign public IP addresses for workers as well as the scheduler.


AWS example -- single, public subnet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One way to structure your network on AWS is to have a single public subnet that's used for both schedulers and workers. Scheduler and workers would all use public IP addresses, and you could use a Security Group to block ingress to the workers from outside the cluster.

The main components involved are:

- **VPC** with attached **Internet Gateway** and a **subnet** to use for Coiled clusters
- **Route Table** for the subnet with route for ``0.0.0.0/0`` to the Internet Gateway
- **Security Group** for scheduler(s) that allows ingress on ports 8786 and 8787 from the your Python client, which could be achieved by opening these ports to traffic from anywhere (``0.0.0.0/0``), or a more limited IP range such as a VPN you're using to connect to scheduler from Python client
- **Security Group** for entire cluster(s) that allows all ingress specifically from that Security Group, which allows scheduler and workers to connect to each other

When configuring Coiled to use your network, you'd specify the same subnet as both **scheduler subnet** and **worker subnet**. Since you aren't using NAT Gateway, you'll need to configure Coiled to give the workers **public IP addresses**.

AWS example -- public and private subnets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another way to structure your network on AWS is to have a public subnet for the scheduler, and to use a private subnet and NAT Gateway for the workers. In this case, the workers will use NAT Gateway for egress (they need to be able to download things).

The main components involved are:

- **VPC** with attached **Internet Gateway**
- One public **subnet** with **NAT Gateway** and a **route table** for the subnet with route for ``0.0.0.0/0`` to the Internet Gateway
- One private **subnet** with a **route table** with route for ``0.0.0.0/0`` to the NAT Gateway
- **Security Group** for scheduler(s) that allows ingress on ports 8786 and 8787 from the your Python client, which could be achieved by opening these ports to traffic from anywhere (``0.0.0.0/0``), or a more limited IP range such as a VPN you're using to connect to scheduler from Python client
- **Security Group** for entire cluster(s) that allows all ingress specifically from that Security Group, which allows scheduler and workers to connect to each other

The public subnet would be specified as the **scheduler subnet**, and the private subnet would be specified as the **worker subnet**.

Since the workers are in a private subnet and use NAT Gateway for egress, you can tell Coiled to not give the workers **public IP addresses**.

GCP example -- single, public subnet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One way to structure your network on GCP is to have a single public subnet that's used for both schedulers and workers. Scheduler and workers would all use public IP addresses, and you could use firewall rules to block ingress to the workers from outside the cluster.

The main components involved are:

- **VPC Network** with a **subnet** to use for Coiled clusters
- **Routes** which route traffic to the CIDR block of your VPC to the VPC and route traffic to ``0.0.0.0/0`` to the default internet gateway
- three **firewall rules**:

  - Allow egress to ``0.0.0.0/0`` for all ports. This will have two target tags, one which will be used as scheduler tag, one that will be used as cluster tag
  - Allow ingress on ports 8786 and 8787 from the your Python client, which could be achieved by opening these ports to traffic from anywhere (``0.0.0.0/0``), or a more limited IP range such as a VPN you're using to connect to scheduler from Python client. This will have target tag which will be used as scheduler tag.
  - Allow ingress for all ports with the *source* as the two target tags you're using, the scheduler tag and the cluster tag. This rule should target the cluster tag.

When configuring Coiled to use your network, you'd specify the same subnet as both **scheduler subnet** and **worker subnet**. Since you aren't using NAT Gateway, you'll need to configure Coiled to give the workers **public IP addresses**.


.. _byo-net-python-api:

Configure network using Python API
----------------------------------

While it's easiest to configure your network using the UI for your account on `cloud.coiled.io <https://cloud.coiled.io>`_, it's also possible to configure your backend options using our Python API.

If you want to have Coiled use a network you've created, you'll need to specify the ID for the VPC network, the scheduler and worker subnets (needn't be distinct), and the Security Groups (AWS) or target network tag for firewall rules (GPC).

Optionally, you can specify the ``give_workers_public_ip`` option (defaults to ``True``) to control whether workers get public IPs which they can use for egress without NAT. If you put workers in a private subnet and don't have them assigned public IP addresses, you'll need a route on that subnet that goes through NAT so they can still download required files over the internet.

AWS setup using Python API
~~~~~~~~~~~~~~~~~~~~~~~~~~

For AWS, the network configuration would look like this:

.. code-block::

  import coiled

  coiled.set_backend_options(
    backend="aws",
    customer_hosted=True,
    aws_access_key_id="...",
    aws_secret_access_key="...",
    network={
      "network_id":"vpc-12345678",
      "scheduler_subnet_id":"subnet-12345678",
      "worker_subnet_id":"subnet-87654321",
      "scheduler_firewall_id":"sg-12345678"  # security group used for scheduler
      "firewall_id":"sg-24680",  # security group used for whole cluster
      "give_workers_public_ip": True  # optional, defaults to True
    }
  )

The resource IDs are not the full ARN, just the ID. Specify the Security Group for the scheduler as ``scheduler_firewall_id`` and the Security Group for the whole cluster as ``firewall_id``.

GCP setup using Python API
~~~~~~~~~~~~~~~~~~~~~~~~~~

For GCP, you can provide credentials as a file with your key-pair (here ``/path/to/my-gcp-key.json``).

The VPC Network and subnets can either be specified by name (e.g., ``my-vpc-network-name``) or by the full "selfLink" URI (``https://www.googleapis.com/compute/v1/projects/my-project-name/global/networks/my-vpc-network-name``).

For firewall rules, you need to provide the target network tag for us to apply to scheduler as ``scheduler_firewall_id`` and the tag for us to apply to whole cluster as ``firewall_id``.

.. code-block::

  coiled.set_backend_options(
    backend_type="gcp",
    gcp_service_creds_file="/path/to/my-gcp-key.json",
    gcp_project_id="my-project-name",
    gcp_region="us-east1",
    gcp_zone="us-east1-c",
    registry_type="gar",
    customer_hosted=True,
    network={
      "network_id": "my-vpc-network-name",
      "scheduler_subnet_id": "my-subnet-name",
      "worker_subnet_id": "my-subnet-name",
      "scheduler_firewall_id": "my-scheduler-firewall-tag",
      "firewall_id": "my-cluster-firewall-tag",
      "give_workers_public_ip": True  # optional, defaults to True
    }
  )

If you were to use the full selfLink URI for network and subnets, the call would look like this:

.. code-block::

  coiled.set_backend_options(
    backend_type="gcp",
    gcp_service_creds_file="/path/to/my-gcp-key.json",
    gcp_project_id="my-project-name",
    gcp_region="us-east1",
    gcp_zone="us-east1-c",
    registry_type="gar",
    customer_hosted=True,
    network={
      "network_id": "https://www.googleapis.com/compute/v1/projects/my-project-name/global/networks/my-vpc-network-name",
      "scheduler_subnet_id": "https://www.googleapis.com/compute/v1/projects/my-project-name/regions/us-east1/subnetworks/my-subnet-name",
      "worker_subnet_id": "https://www.googleapis.com/compute/v1/projects/my-project-name/regions/us-east1/subnetworks/my-subnet-name",
      "scheduler_firewall_id": "my-scheduler-firewall-tag",
      "firewall_id": "my-cluster-firewall-tag",
      "give_workers_public_ip": True  # optional, defaults to True
    }
  )
