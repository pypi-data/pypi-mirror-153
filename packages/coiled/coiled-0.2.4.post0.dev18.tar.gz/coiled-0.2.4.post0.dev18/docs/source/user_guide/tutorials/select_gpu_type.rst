Selecting GPU Types
===================

Coiled supports running computations with GPU-enabled machines in all
the supported cloud providers, please refer to the
:doc:`GPUs documentation <../gpu>` for more information.

In AWS, the GPU selection is tied to the instance type that you request. For
example, in AWS if you select the instance type ``g4dn.xlarge``, this instance
type contains an Nvidia Tesla T4 GPU.

The cloud provider that works a bit differently is the Google Cloud
Platform (GCP). In GCP, you can attach different GPUs to ``n1``
instances.

The rest of the article will assume that you are using the GCP cloud
provider for your account.

You can select the GPU type by using the ``worker_gpu_type`` keyword argument in
the :meth:`coiled.Cluster` constructor. For example:

.. code:: python

  import coiled

  cluster = coiled.Cluster(
      worker_gpu_type="nvidia-tesla-t4", worker_vm_types=["n1-standard-2"]
  )
