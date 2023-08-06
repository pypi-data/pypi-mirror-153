Selecting Instance Types
========================

An instance is a server hosted by a cloud provider and instance types
(or machine types) are defined by combinations of CPU, memory, storage, and networking capacity
(see `GCP supported instance types`_ and `AWS supported instance types`_ for more details). 
When creating a cluster, Coiled will find all available instance types with the
requirements that you specify for CPU, memory, and GPU.
To allow for more fine-grain control of the type of cluster you create, you can
provide a list of instance types for the scheduler and workers
using the ``scheduler_vm_types`` and ``worker_vm_types`` keyword arguments.
For example:

.. code:: python

  import coiled

  cluster = coiled.Cluster(
      scheduler_vm_types=["t3.large", "t3.xlarge"],
      worker_vm_types=["m5n.large", "m5zn.large"],
  )

It's recommended you specify more than one instance type in your list to
avoid instance availability issues in the cloud provider and region that
you are using Coiled.

If you provide a list of specific instance types, Coiled will prioritize them in order of decreasing priority. 
If you instead specify the number of CPUs or memory, compatible instance types are prioritized in order of lowest to highest estimated cost.


Allowable Instance Types
-------------------------

You can use :meth:`coiled.list_instance_types()` to see a list of all
allowed instance types for your configured cloud provider. For example:

.. code:: python

  import coiled

  coiled.list_instance_types()

For more details on supported instance types see 

You can specify a single keyword argument or a combination (e.g. ``cores``, ``memory`` and
``gpus``) to filter the results.

.. code:: python

  import coiled

  # Filter instances that have 4 cores only
  coiled.list_instance_types(cores=4)

  # Filter instances by cores and memory
  coiled.list_instance_types(cores=2, memory="8 Gib")

You can also provide ``list_instance_types`` with a range of values, for example:

.. code:: python

  import coiled

  coiled.list_instance_types(cores=[2, 8])

You might be also interested in the tutorial on :doc:`select_gpu_type`.

.. _GCP supported instance types: https://cloud.google.com/compute/docs/machine-types
.. _AWS supported instance types: https://aws.amazon.com/ec2/instance-types/
