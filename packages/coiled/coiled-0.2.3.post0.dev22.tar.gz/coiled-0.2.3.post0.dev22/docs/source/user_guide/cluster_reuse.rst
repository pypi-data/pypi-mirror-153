.. _cluster-reuse:

================
Reusing clusters
================

.. currentmodule:: coiled

Once you're created a cluster, it's sometimes useful to be able to connect to
the same running cluster in a different Python process. This can be done by
specifying a unique name for the cluster and whether or not to shutdown a
cluster by providing the following keyword arguments to the
:class:`coiled.Cluster()` constructor:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Parameter
     - Description
     - Default
   * - ``name``
     - Name to use for identifying this cluster
     - Randomly generated name
   * - ``shutdown_on_close``
     - Whether or not to shut down the cluster when it finishes
     - ``True`` unless ``name`` points to an existing cluster

For example, the following creates a cluster named "production":

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(
        name="production",
        n_workers=5,
        worker_cpu=2,
        worker_memory="8 GiB",
    )

which we can then, say in another Python session, connect to the same running
"production" cluster by passing ``name="production"`` to
:class:`coiled.Cluster()`:

.. code-block:: python

    import coiled

    # Connects to the existing "production" cluster
    cluster = coiled.Cluster(
        name="production",
    )
