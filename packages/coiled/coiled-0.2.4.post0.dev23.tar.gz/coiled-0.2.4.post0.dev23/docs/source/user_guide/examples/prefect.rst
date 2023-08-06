Workflow automation (Prefect)
=============================

Prefect automates data engineering workflows. Coiled helps scale Prefect on
cloud resources. It's easy to use both together.


Prefect in a nutshell
---------------------

`Prefect <https://www.prefect.io/>`_ is a popular workflow management system.
At it's core, Prefect has the concept of a ``Task``, ``Flow``, and ``Executor``:

- A `Task <https://docs.prefect.io/core/concepts/tasks.html>`_ is an individual
  step in a Prefect workflow
- A `Flow <https://docs.prefect.io/core/concepts/flows.html>`_ is a collection
  of tasks that represent the entire workflow
- An `Executor <https://docs.prefect.io/core/concepts/engine.html#executors>`_
  is a class that's responsible for running a ``Flow``

In the following sections, we'll explore different ways that Coiled and Prefect
can work together. At a more granular level, we'll call Coiled from one or more
Prefect tasks. At a higher level, we'll configure Coiled to act as a Dask
Executor to run all Prefect tasks in a flow.


Using Coiled with Prefect
-------------------------

There are different ways of using Coiled with Prefect. Two common methods are:

- Calling Coiled from within a Prefect task
   - Prefect tasks execute on existing compute resources until Coiled is needed
   - Coiled cluster only runs when needed
- Running all Prefect Tasks on Coiled
   - Prefect tasks execute on worker nodes in a Coiled cluster
   - All Prefect tasks within a flow run on a Coiled cluster

We'll explore these two methods in more detail in the following sections.


Calling Coiled from a Prefect Task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you only need to call out to Coiled to run some large distributed
computations, then you can create a Coiled cluster and run your computations
from within a Prefect task, then proceed to subsequent Prefect tasks.

.. figure:: ../images/coiled-prefect-task.png
   :width: 100%

The example below defines two Prefect tasks: one task that uses Coiled to handle
a large computation, and a second task that takes the result from the first and
performs a simpler computation.

.. literalinclude:: prefect-task.py

Click :download:`here <prefect-task.py>` to download the above example script.

Coiled comes into play in these lines:

.. code-block:: python

    import coiled
    import dask.dataframe as dd
    from dask.distributed import Client

    [...]

    cluster = coiled.Cluster(n_workers=10)
    client = Client(cluster)

    df = dd.read_csv([...]).persist()

    [...]

    result = df.groupby("passenger_count").tip_amount.mean().compute()

where we create a Coiled cluster, run a large computation, then continue on to
subsequent Prefect tasks without Coiled. This lets you easily scale the
resources available to specific computations with Prefect tasks when running
your workflow.


Running all Prefect Tasks on Coiled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using Prefect's ``DaskExecutor``, you can run all tasks from a workflow on a
Dask cluster, including Coiled clusters.

.. figure:: ../images/coiled-prefect-executor.png
   :width: 100%

The example below uses Prefect and Coiled to read NYC Taxi data and find some of
the most generous tippers in historical data. It does this by reading a CSV file
on Amazon S3, breaking it into many small pieces (one DataFrame for each hour of
data), cleans the data, and then finds rows in the data with exceptional values
for tipping and logs those rows.

We highlight a few of the features that Prefect provides:

1.  We intentionally add some random failures into the cleaning process to show
    off how Prefect can provide automatic retry logic
2.  We return lists of objects to show how Prefect can map over collections of
    outputs
3.  At the end of the computation we send a report to a public Slack channel
    (sign up for the
    `Coiled Community Slack <https://join.slack.com/t/coiled-users/shared_invite/zt-gqiukhua-rJ4QKxJyO3OYTPR7w_xeOQ>`_
    and then navigate to the ``prefect-example`` channel to see results)
4.  Easy scalability by connecting with a Dask cluster, in this case provided by
    Coiled.

.. literalinclude:: prefect-executor.py


Click :download:`here <prefect-executor.py>` to download the above example
script.

Coiled comes into play in these lines:

.. code-block:: python

    import coiled

    executor = DaskExecutor(
        cluster_class=coiled.Cluster,
        cluster_kwargs={
            "software": "jrbourbeau/prefect",
            "shutdown_on_close": False,
            "name": "prefect-executor",
        },
    )

where we setup a ``DaskExecutor`` so Prefect can run our workflow on a
``coiled.Cluster`` with the provided arguments. This lets us easily scale the
resources available to Prefect for running our workflow.


Best practices
--------------

Software environments
~~~~~~~~~~~~~~~~~~~~~

You will want to make sure that the Coiled cluster running on the cloud has
Prefect installed, along with any other libraries that you might need in order
to complete the work, like Pandas or S3Fs in this case. For more information on,
see
:doc:`documentation on constructing software environments <../software_environment>`.

Reusing clusters
~~~~~~~~~~~~~~~~

It's also common to run several flows one after the other. For example we may
want to run this same flow on data for many months of data, rather than just the
one file in this example.

In this case spinning up a new Coiled cluster for every flow may be cumbersome
(it takes about a minute to start a cluster). Instead, we recommend using the
``shutdown_on_close=False`` keyword, along with a specific name for your
cluster, like ``prefect-task`` or ``production``. This tells Coiled that you
want to :doc:`reuse a specific cluster <../cluster_reuse>` for many different
workflows.

Idle timeouts
~~~~~~~~~~~~~

By default, Coiled will automatically shut down your cluster after 20 minutes of
inactivity. You can run your Prefect flow again after this period, but you will
need to wait for a new Coiled cluster to be provisioned.

Alternatively, you can specify a custom idle timeout when creating a cluster.
Refer to the documentation on :ref:`customizing clusters <customize-cluster>`
for more information on how to set idle timeouts.
