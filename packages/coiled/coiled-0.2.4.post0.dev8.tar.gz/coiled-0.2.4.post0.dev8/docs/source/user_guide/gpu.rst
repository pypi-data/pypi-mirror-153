.. _gpus:

GPUs
====

Coiled supports running computations with GPU-enabled machines. In principle, 
doing this is as simple as setting ``worker_gpu=1`` in the ``coiled.Cluster()`` 
constructor:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(
       ...,
       worker_gpu=1,
   )

.. note::

    When asking for GPU enabled workers, Coiled will always use on demand instances
    instead of the default Spot instances. If you want to use spot instances you can
    add ``backend_options={"spot": True}`` to the ``coiled.Cluster`` constructor.

But in practice there are additional considerations.

Getting Started 
---------------

First, note that free individual cloud accounts do not 
have GPU access enabled (see Account Access, below).

Next, you will need a suitable software environment. The specifics will vary
with your need.  An example suitable for some initial work and testing is given 
here:

.. code-block:: python

   import coiled

   # Create a software environment with GPU accelerated libraries
   # and CUDA drivers installed
   coiled.create_software_environment(
       name="gpu-test",
       container="gpuci/miniconda-cuda:11.2-runtime-ubuntu20.04",
       conda={
           "channels": [
               "rapidsai",
               "conda-forge",
               "defaults",
           ],
           "dependencies": [
               "dask",
               "dask-cuda",
               "cupy",
               "cudatoolkit=11.2",
           ],
       },
   )

More information on GPU software environments is given below.

With a suitable software environment, creating a cluster is straightforward.
Simply set ``worker_gpu=1``. Currently, Coiled only supports a single GPU per worker.

.. code-block:: python

   # Create a Coiled cluster that uses
   # a GPU-compatible software environment
   cluster = coiled.Cluster(
       scheduler_cpu=2,
       scheduler_memory="4 GiB",
       worker_cpu=4,
       worker_memory="16 GiB",
       worker_gpu=1,
       worker_class="dask_cuda.CUDAWorker",
       software="gpu-test",
   )

Notice that in this cluster configuration we set ``worker_class="dask_cuda.CUDAWorker"``. By 
doing this, the Client will automatically launch one worker on each GPU available as 
well as enabling several unique features unavailable to Distributed. For further details on 
these features check the `Dask-CUDA motivation <https://docs.rapids.ai/api/dask-cuda/stable/index.html#motivation>`_ 
documentation.

If desired, the cluster specified above can be tested with the following computation:

.. code-block:: python

    from dask.distributed import Client


    def test_gpu():
        import numpy as np
        import cupy as cp

        x = cp.arange(6).reshape(2, 3).astype("f")
        return cp.asnumpy(x.sum())


    client = Client(cluster)

    f = client.submit(test_gpu)
    f.result()

If successful, this should return ``array(15., dtype=float32)``.

You can also verify that workers are using GPUs with the following command:

.. code-block:: python

    cluster.scheduler_info["workers"]

.. note::

    If you are a member of more than one team (remember, you are automatically a
    member of your own personal account), you must specify the team under which
    to create the cluster (defaults to your personal account). You can do this
    with either the ``account=`` keyword argument, or by adding it as a prefix
    to the name of the cluster, such as ``name="<account>/<cluster-name>"``.
    Learn more about :doc:`teams <teams>`.


Software Environments
---------------------

When creating a software environment for GPUs, you will need to install the GPU
accelerated libraries needed (e.g. PyTorch, RAPIDS, XGBoost, Numba,
etc.) and also ensure that the container in use has the
correct CUDA drivers installed.

Coiled deploys instances with with recent NVIDIA drivers and CUDA version 11.x.
You should use a software environment which includes ``cudatoolkit`` version 11,
for instance, ``cudatoolkit=11.6``.

Current Hardware
----------------

Currently Coiled mostly deploys cost efficient T4 GPUs by default. If you are
interested in using higher performance GPUs then please `contact us`_.

Account Access
--------------

Free individual accounts do not have GPU access turned on by default. If you are
interested in testing out GPU access then please `contact us`_.

If you have been granted access it may be as part of a team account. If so,
please be aware that you will have to specify the account under which you want
to create your cluster in the ``coiled.Cluster`` constructor:

.. code-block:: python

   cluster = coiled.Cluster(
       scheduler_cpu=2,
       scheduler_memory="4 GiB",
       worker_cpu=4,
       worker_memory="16 GiB",
       worker_gpu=1,
       software="gpu-test",
       account="MY-TEAM-ACCOUNT",
   )

.. _contact us: sales@coiled.io
