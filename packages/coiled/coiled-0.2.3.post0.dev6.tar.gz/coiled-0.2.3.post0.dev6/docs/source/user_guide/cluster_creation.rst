.. _cluster-creation:

=================
Creating clusters
=================

.. currentmodule:: coiled


Spinning up Dask clusters with Coiled is done by creating a
:class:`coiled.Cluster` instance. ``coiled.Cluster`` objects manage a Dask
cluster much like other cluster object you may have seen before like
:class:`distributed.LocalCluster` or :class:`dask_kubernetes.KubeCluster`.

The video below will walk you through the process of spinning up a simple custer.

.. raw:: html

   <div style="display: flex; justify-content: center;">
       <iframe
          width="560"
          height="315"
          src="https://youtube.com/embed/vWV_FF381qo"
          title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        >
        </iframe>
   </div>

Simple example
--------------

In a simple case, you can create a cluster with five Dask workers with:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(n_workers=5)


.. note::

    Creating a cluster involves provisioning various resources on cloud-based
    infrastructure. This process takes a couple of minutes in most cases.

Once a cluster has been created, you can connect Dask to the cluster by creating
a :class:`distributed.Client` instance:

.. code-block:: python

    from dask.distributed import Client

    client = Client(cluster)

To view the
`Dask diagnostic dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
for your cluster, navigate to the cluster's ``dashboard_link``:

.. code-block:: python

    cluster.dashboard_link

which should output a dashboard address similar to
``http://35.174.137.175:8787``.


.. tip::

    Any Coiled cluster you create will automatically shut down after 20 minutes
    of inactivity. No more large bills from leaving a cluster running over the
    weekend 🎉! You can also customize this idle timeout if needed -- see the
    :ref:`customize-cluster` section for an example that does this.


The ``coiled.Cluster`` class has several keyword arguments you can use to
further specify the details of your cluster. These parameters are discussed in
the following sections.


Hardware resources
------------------

The hardware resources your cluster is launched on (e.g. number of CPUs, amount
of RAM, etc.) can be configured with the following ``coiled.Cluster`` keyword
arguments:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``worker_cpu``
     - Number of CPUs allocated for each worker
     - ``None``
   * - ``worker_gpu``
     - Number of GPUs allocated for each worker. Note that GPU
       access is disabled by default. If you would like access to GPUs,
       please contact sales@coiled.io.
     - ``0``
   * - ``worker_memory``
     - Amount of memory to allocate for each worker
     - ``None``
   * - ``worker_vm_types``
     - Instance types allocated for the workers
     - ``t3-medium/e2-standard-e2``
   * - ``scheduler_cpu``
     - Number of CPUs allocated for the scheduler
     - ``None``
   * - ``scheduler_memory``
     - Amount of memory to allocate for the scheduler
     - ``None``
   * - ``scheduler_vm_types``
     - Instance types allocated to the scheduler
     - ``t3-medium/e2-standard-e2``


For example, the following creates a cluster with five workers, each with 2 CPUs
and 8 GiB of memory available, and a scheduler with 2 CPUs (default value) and
8 GiB of memory available:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        n_workers=5,
        worker_cpu=2,
        worker_memory="8 GiB",
        scheduler_memory="8 GiB",
    )

Note that while specifying ``worker_gpu`` will give your cluster workers access
to GPUs, there are some additional best practices to ensure GPU-accelerated
hardware is fully utilized. See the :doc:`GPU best practices <gpu>`
documentation for more information.

Software environment
--------------------

The scheduler and each worker in a Coiled cluster are all launched with the same
software environment. By default, they will use a software environment with
Python, Dask, Distributed, NumPy, Pandas, and a few more commonly used
libraries. This default environment is great for basic tasks, but you'll also
want to create your own custom software environments with the packages you need
on your cluster.

Coiled supports building and managing custom software environments using pip and
conda environment files. For more details on custom software environments, see
the :ref:`software-envs` documentation page. Once you have a custom software
environment you can use the ``software`` keyword argument for ``coiled.Cluster``
to use that software environment on your cluster.

.. admonition:: Note
    :class: note

    Software environments used in Coiled clusters must have
    ``distributed >= 2.23.0`` installed as
    `Distributed <https://distributed.dask.org>`_ is required to launch Dask
    scheduler and worker processes.

For example, the following uses a custom software environment with XGBoost
installed:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(software="examples/scaling-xgboost")


.. _customize-cluster:

Custom workers and scheduler
----------------------------

Dask supports using custom worker and scheduler classes in a cluster which
allows for increased flexibility and functionality in some use cases (e.g.
`Dask-CUDA <https://dask-cuda.readthedocs.io>`_'s ``CUDAWorker`` class for
running Dask workers on NVIDIA GPUs). Additionally, worker and scheduler classes
also have keyword arguments that can be specified to control their behavior (for
an example, see
`Dask's worker class API documentation <https://distributed.dask.org/en/latest/worker.html#distributed.worker.Worker>`_).

The worker and scheduler class used in a Coiled cluster, as well as the keyword
arguments, passed to those classes can be specified with the following
``coiled.Cluster`` keyword arguments:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``worker_class``
     - Class to use for cluster workers
     - ``"distributed.Nanny"``
   * - ``worker_options``
     - Mapping with keyword arguments to pass to ``worker_class``
     - ``{}``
   * - ``scheduler_class``
     - Class to use for the cluster scheduler
     - ``"distributed.Scheduler"``
   * - ``scheduler_options``
     - Mapping with keyword arguments to pass to ``scheduler_class``
     - ``{}``

For example, the following creates a cluster which uses Distributed's ``Worker``
class for workers (instead of the default ``Nanny`` class) and specifies
``idle_timeout="2 hours"`` when creating the cluster's scheduler:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        worker_class="distributed.Worker",
        scheduler_options={"idle_timeout": "2 hours"},
    )

Instance Types
--------------

Coiled will choose instance types that match your cluster CPU/Memory
requirements. If you wish, you can specify a list of instance types when
creating your cluster (see the tutorial on :doc:`tutorials/select_instance_types`).
Since cloud providers might have availability issues
for a specific instance type, it's recommended you specify more than one
type in the list.

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default [AWS/GCP]
   * - ``scheduler_vm_types``
     - List of instance types for the scheduler
     - ``["t3.medium/e2-standard-e2"]``
   * - ``worker_vm_types``
     - List of instance types for workers
     - ``["t3.medium/e2-standard-e2"]``

Backend options
---------------

Depending on where you're running Coiled, there may be backend-specific options
(e.g. which AWS region to use) that you can specify to customize Coiled's
behavior. For more information on what options are available, see the
:doc:`backends` documentation.


Environment Variables
---------------------

To add environment variables to your clusters, use the ``environ``
keyword argument of ``coiled.Cluster``. The input of ``environ``
should be a dictionary.

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        n_workers=5,
        software="examples/scaling-xgboost",
        environ={
            "DASK_COILED__ACCOUNT": "alice",
            "DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING": True,
            "DASK_DISTRIBUTED__LOGGING__DISTRIBUTED": "info",
        },
    )

.. attention::

    Environment variables are not encrypted and will be available as plain text.
    For security reasons, you should **not** use environment variables to add secrets
    to your clusters.


Communication Protocol
----------------------

Coiled uses ``tls`` by default, but in some restricted environments (corporate networks, Binder notebooks, etc.)
the default port (8786) may be blocked. Since the websocket protocol uses the standard port for secure web traffic, it's unlikely to be blocked.
This can be changed with the ``protocol`` parameter of ``scheduler_options`` and ``worker_options``.

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        n_workers=5,
        scheduler_options={"protocol": "wss"},
        worker_options={"protocol": "wss"},
    )


.. tip::

    Coiled provides a top level ``protocol`` keyword argument that acts as a shortcut for both these options.

    .. code-block:: python

        import coiled

        cluster = coiled.Cluster(
            n_workers=5,
            protocol="wss",
        )

.. _wait-for-workers:

Waiting for workers
-------------------

Usually, computations will run better if you wait for most works before submitting tasks to the cluster. By default,
Coiled will wait for 30% of the requested workers, before returning the prompt back to the user. You can override
this behaviour by using the ``wait_for_workers`` parameter.

If you use an int, the Coiled client will wait for that number of workers. Note that you can only wait for a number
between 0 and ``n_workers`` requested.

.. code-block:: python

  import coiled

  cluster = coiled.Cluster(n_workers=10, wait_for_workers=4)

Alternatively, you might want to use a fraction of workers instead. Note that you need to specify a number between 0.0
and 1.0.

.. code-block:: python

  import coiled

  cluster = coiled.Cluster(n_workers=60, wait_for_workers=0.5)

You can also set ``wait_for_workers`` to True if you want to wait for all the requested workers. This option should be used
with caution when requesting large clusters, due to availability issues from the chosen cloud provider.

.. code-block:: python

  import coiled

  cluster = coiled.Cluster(n_workers=25, wait_for_workers=True)

If you would rather get the prompt back as soon as the scheduler is up, you can set ``wait_for_workers`` to False or 0.

.. code-block:: python

  import coiled

  cluster = coiled.Cluster(n_workers=25, wait_for_workers=False)

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``wait_for_workers``
     - Number os workers to wait before running computations
     - ``0.3``

If you want to use the same value for the ``wait_for_workers`` parameter, then you can edit your
:ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      wait_for_workers: false
