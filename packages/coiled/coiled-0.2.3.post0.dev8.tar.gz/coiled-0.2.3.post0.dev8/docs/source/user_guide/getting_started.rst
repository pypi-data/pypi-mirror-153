.. _getting-started:

===============
Getting Started
===============

Welcome to the getting started guide for Coiled! This page covers installing and
setting up Coiled as well as running your first computation. In this page you will:

    - Spin up a remote Dask cluster by creating a :class:`coiled.Cluster` instance.
    - Connect a Dask ``Client`` to the cluster.
    - Submit a Dask DataFrame computation for execution on the cluster.
    - Stop a running cluster.
    - Close the Dask ``Client``.

The video below will walk you through installing and setting up Coiled on your machine.

.. raw:: html

   <div style="display: flex; justify-content: center;">
       <iframe width="560" height="315" src="https://www.youtube.com/embed/BsQK5_y1nvE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>


Install
-------

Coiled can be installed from PyPI using ``pip`` or from the conda-forge channel
using ``conda``:


.. panels::
    :body: text-center
    :header: text-center h5 bg-white

    Install with pip
    ^^^^^^^^^^^^^^^^

    .. code-block:: bash

        pip install coiled

    ---

    Install with conda
    ^^^^^^^^^^^^^^^^^^

    .. code-block:: bash

        conda install -c conda-forge coiled     
        
.. _coiled-setup:

Setup
-----

Coiled comes with a ``coiled login`` command line tool to configure your account
credentials. From the command line enter:

.. code-block:: bash

    $ coiled login

You'll then be asked to login to the Coiled web UI, and navigate to 
https://cloud.coiled.io/profile where you can create and manage API tokens.

.. code-block:: bash

    Please login to https://cloud.coiled.io/profile to get your token
    Token:

Upon entering your token, your credentials will be saved to Coiled's local
configuration file. Coiled will then pull credentials from the configuration
file when needed.

.. dropdown:: For windows users
    :container: mb-2 border-0
    :title: bg-white text-left h6 mb-3
    :body: bg-white mb-3
    :animate: fade-in

    Unless you are using WSL, you will need to go to a command 
    prompt or PowerShell window within an appropriate environment (i.e. 
    that includes coiled) to login via ``coiled``.
    
    However, because the Windows clipboard will not be active at 
    the 'Token:' prompt, users should provide the token as an argument:
    ``coiled login --token [your-token-here]``.
    Alternatively, users can use ``!coiled login --token [your-token-here]``
    from a Jupyter notebook.

.. _first-computation:

Run your first computation
--------------------------

When performing computations on remote Dask clusters, it's important to have the
same libraries installed both in your local Python environment (e.g. on your
laptop), as well as on the remote Dask workers in your cluster.

Coiled helps you seamlessly synchronize these software environments (see the
:doc:`software_environment` section for more details). For now, we'll do this
from the command line, relying on the coiled-runtime metapackage
(see the :ref:`overview on coiled-runtime <coiled-runtime>`):

.. code-block:: bash

    $ conda create -n coiled-default-py39 python=3.9 coiled-runtime -c conda-forge
    $ conda activate coiled-default-py39
    $ ipython

The above snippet will create a local conda environment named
"coiled-default-py39", activate it, and then launch an IPython session.
Note that even though we're creating a local software environment, all Dask computations
will happen on remote Dask workers on AWS, *not* on your local machine (for more
information on why local software environments are needed, see our
:ref:`FAQ page <why-local-software>`).

Now that we have our local software environment set up, we can walk through the
following example:

.. code-block:: python

    # Create a remote Dask cluster with Coiled
    import coiled

    cluster = coiled.Cluster(software="coiled/default-py39")

    # Connect Dask to that cluster
    import dask.distributed

    client = dask.distributed.Client(cluster)
    print("Dask Dashboard:", client.dashboard_link)

Make sure to check out the
`cluster dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
(link can be found at ``client.dashboard_link``) which has real-time information
about the state of your cluster including which tasks are currently running, how
much memory and CPU workers are using, profiling information, etc.

.. note::

    When creating a ``coiled.Cluster``, resources for our Dask cluster
    are provisioned on AWS. This provisioning process takes about a minute to
    complete.


.. code-block:: python

    # Perform computations with data on the cloud

    import dask.dataframe as dd

    df = dd.read_parquet(
        "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.parquet",
        columns=["passenger_count", "tip_amount"],
        storage_options={"anon": True},
    ).persist()

    df.groupby("passenger_count").tip_amount.mean().compute()

The Coiled dashboard also provides valuable information about your cluster and the computations it may be running. Learn more about it in the `Managing Clusters <https://docs.coiled.io/user_guide/cluster_management.html>`_ section of this user guide.


Stopping a Cluster
------------------

By default, clusters will shutdown after 20 minutes of inactivity. You can stop
a cluster by pressing the stop button on the
`Coiled dashboard <https://cloud.coiled.io/>`_. Alternatively, we can get a list
of all running clusters and use the cluster name to stop it. Read more about
:ref:`managing clusters <cluster-management>`.

.. code-block:: python

    coiled.list_clusters()

The command ``list_clusters`` returns a dictionary of running clusters. The
cluster name is used as the key. We can grab that and then call the command
``coiled.close()`` to stop the running cluster, and ``client.close()``
to close the client.

.. code-block:: python

    cluster.close()  # Close the cluster
    client.close()  # Close the client as well

You can now go back to the `Coiled dashboard <https://cloud.coiled.io/>`_ and
you will see that the cluster is now stopping/stopped.

Next steps
----------

After you get started, take a look at the :doc:`next_steps` page to learn more
about what you can do with Coiled.
