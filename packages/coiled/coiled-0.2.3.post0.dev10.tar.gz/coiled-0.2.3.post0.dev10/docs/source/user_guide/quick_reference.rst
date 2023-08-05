Quick Reference
===============

Creating Dask clusters
----------------------

.. list-table::
   :widths: 30 70

   * - Create a Dask cluster with 10 workers (:doc:`Learn more <cluster_creation>`)
     - .. code-block:: python

          import coiled
          cluster = coiled.Cluster(n_workers=10)
   * - Create a Dask cluster with a custom software environment (:doc:`Learn more <cluster_creation>`)
     - .. code-block:: python

          import coiled
          cluster = coiled.Cluster(software="my-pip-env")
   * - Create a Dask cluster with 1 GPU per worker (:doc:`Learn more <gpu>`)
     - .. code-block:: python

          import coiled
          cluster = coiled.Cluster(worker_gpu=1)
   * - Create a Dask cluster in a Team account (:doc:`Learn more <teams>`)
     - .. code-block:: python

          import coiled
          cluster = coiled.Cluster(account="my-team-account-name")

Working with Dask clusters
--------------------------

.. list-table::
   :widths: 30 70

   * - Connect to a cluster (:doc:`Learn more <cluster_creation>`)
     - .. code-block:: python

          from dask.distributed import Client
          client = Client(cluster)
          print('Dashboard:', client.dashboard_link)
   * - Once connected, run a Dask computation as usual (`Learn more <https://examples.dask.org>`_)
     - .. code-block:: python

          import dask.dataframe as dd
          df = dd.read_csv(...).persist()
          df.groupby(...).tip_amount.mean().compute()
   * - Scale the number of workers (:doc:`Learn more <api>`)
     - .. code-block:: python

          cluster.scale(15)
   * - Reuse an existing cluster (:doc:`Learn more <cluster_reuse>`)
     - .. code-block:: python

          cluster = coiled.Cluster(name="existing-cluster-name")
   * - Generate a performance report (:doc:`Learn more <performance_reports>`)
     - .. code-block:: python

          from coiled import performance_report

          with performance_report(filename="dask-report.html"):
              df.groupby(...).value.mean().compute()  ## Your dask computation(s)
   * - Terminate a cluster (:doc:`Learn more <cluster_management>`)
     - .. code-block:: python

          client.close()  # if shutdown_on_close=True

       or

       .. code-block:: python

          coiled.delete_cluster(name="my-cluster")

Packages and environments
-------------------------

.. list-table::
   :widths: 30 70

   * - Create a software environment from a list of ``conda`` packages (:doc:`Learn more <software_environment_creation>`)
     - .. code-block:: python

          coiled.create_software_environment(
              name="my-conda-env",
              conda={
                  "channels": ["conda-forge", "defaults"],
                  "dependencies": ["dask", "xarray=0.15.1", "numba"],
              },
          )
   * - Create a software environment from an ``environment.yml`` file (:doc:`Learn more <software_environment_creation>`)
     - .. code-block:: python

          coiled.create_software_environment(
              name="my-conda-env",
              conda="environment.yml",
          )
   * - Create a software environment from a list of ``pip`` packages (:doc:`Learn more <software_environment_creation>`)
     - .. code-block:: python

          coiled.create_software_environment(
              name="my-pip-env",
              pip=["dask[complete]", "xarray==0.15.1", "numba"],
          )
   * - Create a software environment from a ``requirements.txt`` file (:doc:`Learn more <software_environment_creation>`)
     - .. code-block:: python

          coiled.create_software_environment(
              name="my-pip-env",
              pip="requirements.txt",
           )
   * - Create a software environment from an existing Docker image (:doc:`Learn more <software_environment_creation>`)
     - .. code-block:: python

          coiled.create_software_environment(
              name="my-docker-env",
              container="rapidsai/rapidsai:latest",
          )
