Data sources (Snowflake)
========================

.. note::

   The ``dask-snowflake`` connector is currently in beta.

`Snowflake <https://www.snowflake.com/>`_ is is a leading cloud-based data data
warehouse, SQL query engine, and analytics service. Coiled helps scale Python
workloads by provisioning cloud-hosted Dask clusters on demand.

Coiled and Snowflake work great together - Snowflake handles the data storage
and SQL query processing while Coiled handles the backend infrastructure for
dealing with large computations in Python.

.. raw:: html

   <p align="center"><iframe width="560" height="315"
   src="https://www.youtube.com/embed/pinFo1YBD-0" title="YouTube video player"
   frameborder="0" allow="accelerometer; autoplay; clipboard-write;
   encrypted-media; gyroscope; picture-in-picture" allowfullscreen
   style="text-align:center;"></iframe></p>

Loading data from Snowflake into Python or Dask typically involves the use of
the
`Snowflake connector for Python <https://docs.snowflake.com/en/user-guide/python-connector-example.html>`_
to send SQL queries to Snowflake or an intermediate step of exporting data from
Snowflake into Parquet format. This works well for small datasets, but can be a
limiting factor when working with larger datasets and more complex queries.

The ``dask-snowflake`` connector along with added functionality in Snowflake for
distributed fetch enables parallel reads and writes between Snowflake and Dask
clusters in Coiled.

This example walks through the use of the ``dask-snowflake`` connector and the
steps to configure Coiled to read and write large data sets in parallel and then
perform typical distributed computations on that data with Dask.

Prerequisites
^^^^^^^^^^^^^

- An account on Coiled Cloud to provision Dask clusters
- A local Python environment that can connect to and read Snowflake data
- Snowflake credentials and permissions to create warehouses and databases


Step 1: Install dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In your development environment, install the following dependencies and
versions, which include the Snowflake connector for Python and the
``dask-snowflake`` connector. We'll use these dependencies throughout this
example and on the remote Dask cluster with Coiled:

.. code-block:: text

   pip install -U "dask[distributed, dataframe, diagnostics]" \
                  coiled \
                  snowflake-connector-python \
                  dask-snowflake



Step 2: Verify connectivity
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Define your Snowflake connection parameters as environment variables by running
the following Python code and replacing the user, password, and account with
your own values:

.. code-block:: python

   import os

   os.environ["SNOWFLAKE_USER"] = "SNOWFLAKE_USER"
   os.environ["SNOWFLAKE_PASSWORD"] = "SNOWFLAKE_PASSWORD"
   os.environ["SNOWFLAKE_ACCOUNT"] = "SNOWFLAKE_ACCOUNT"
   os.environ["SNOWFLAKE_WAREHOUSE"] = "dask_snowflake_wh"

You can leave the value of ``SNOWFLAKE_WAREHOUSE`` set to ``dask_snowflake_wh``
since we'll use that in a later step.

Verify that you can read Snowflake sample data locally by running the following
Python code:

.. code-block:: python

   import os
   import snowflake.connector

   ctx = snowflake.connector.connect(
       user=os.environ["SNOWFLAKE_USER"],
       password=os.environ["SNOWFLAKE_PASSWORD"],
       account=os.environ["SNOWFLAKE_ACCOUNT"],
   )

   cs = ctx.cursor()

   schema = "TPCDS_SF100TCL"
   table = "CALL_CENTER"

   cs.execute("USE SNOWFLAKE_SAMPLE_DATA")
   cs.execute("SELECT * FROM " + schema + "." + table)

   one_row = str(cs.fetchone())

   print(one_row)

If the connection and query were successful, then you should see output similar
to the following:

.. code-block::

   (1, 'AAAAAAAABAAAAAAA', datetime.date(1998, 1, 1), None, None, 2450952, 'NY
   Metro', 'large', 597159671, 481436415, '8AM-4PM', 'Bob Belcher', 6, 'More
   than other authori', 'Shared others could not count fully dollars. New
   members ca', 'Julius Tran', 3, 'pri', 6, 'cally', '730', 'Ash Hill',
   'Boulevard', 'Suite 0', 'Georgetown', 'Harmon County', 'OK', '77057', 'United
   States', Decimal('-6.00'), Decimal('0.11'))

.. note::

   In this example code, we defined the Snowflake username, password, account,
   and warehouse as environment variables and passed them to the Snowflake
   connector. You might be using a different method for passing your credentials
   or authenticating to Snowflake. In that case, you can modify the example code
   accordingly. Refer to the documentation on
   `Using the Snowflake connector for Python <https://docs.snowflake.com/en/user-guide/python-connector-example.html>`_
   for more information on options and configurations that it supports.


Step 3: Create environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a software environment called ``coiled-snowflake`` that contains the
required dependencies:

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="coiled-snowflake",
       pip=[
           "dask[distributed, dataframe, diagnostics]",
           "snowflake-connector-python",
           "dask-snowflake",
       ],
   )

Note that we specified the same dependencies and versions that you installed in
your local development environment, which ensures consistency between your local
environment and the remote Coiled cluster.

When you create a cluster that uses this environment, these dependencies will be
made available on all of the Dask workers in your cluster. Refer to the
documentation on
:doc:`creating software environments <../software_environment_creation>` for
more information on handling dependencies on your Coiled cluster.


Step 4: Create cluster
^^^^^^^^^^^^^^^^^^^^^^

Create a Dask cluster with Coiled that uses your new software environment:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(
       name="coiled-snowflake",
       software="coiled-snowflake",
   )

   from dask.distributed import Client

   client = Client(cluster)
   print("Dashboard:", client.dashboard_link)

The above code example also connects Dask to your Coiled cluster and prints a
link to the Dask dashboard, which you can use later to view the progress of
parallel reads and writes to Snowflake.

The ``software="coiled-snowflake"`` parameter instructs your cluster to use the
software environment that you creates with the ``dask``,
``snowflake-connector-python``, ``dask-snowflake``, and other packages included
as dependencies.


Step 5: Generate data
^^^^^^^^^^^^^^^^^^^^^

Run the following Python code to generate sample time series data with Dask:

.. code-block:: python

   import dask

   ddf = dask.datasets.timeseries(
       start="2021-01-01",
       end="2021-03-31",
   )

We'll use the ``dask-snowflake`` connector to load this sample data into
Snowflake in a later step.


Step 6: Create resources
^^^^^^^^^^^^^^^^^^^^^^^^

Create a test warehouse and database in Snowflake by running the following
Python code:

.. code-block:: python

   import os
   import snowflake.connector

   ctx = snowflake.connector.connect(
       user=os.environ["SNOWFLAKE_USER"],
       password=os.environ["SNOWFLAKE_PASSWORD"],
       account=os.environ["SNOWFLAKE_ACCOUNT"],
       warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
   )

   cs = ctx.cursor()

   cs.execute("CREATE WAREHOUSE IF NOT EXISTS dask_snowflake_wh")
   cs.execute("CREATE DATABASE IF NOT EXISTS dask_snowflake_db")
   cs.execute("USE DATABASE dask_snowflake_db")

We'll use this test warehouse and database in the following steps to write data
to and read data from Snowflake.


Step 7: Write data in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you've installed the necessary dependencies for working with Dask and
Snowflake and you have a running Coiled cluster, you can use ``dask-snowflake``
to write the sample data with Dask/Coiled in parallel via a distributed fetch:

.. code-block:: python

   from dask_snowflake import to_snowflake

   connection_kwargs = {
       "user": os.environ["SNOWFLAKE_USER"],
       "password": os.environ["SNOWFLAKE_PASSWORD"],
       "account": os.environ["SNOWFLAKE_ACCOUNT"],
       "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
       "database": "dask_snowflake_db",
       "schema": "PUBLIC",
   }

   to_snowflake(
       ddf,
       name="dask_snowflake_table",
       connection_kwargs=connection_kwargs,
   )

You can monitor the progress of the parallel write operation while it runs by
viewing the Dask dashboard. After about a minute, the sample data should appear
in your database in Snowflake. You just loaded about 7.7 million records into
Snowflake in parallel.


Step 8: Read data in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you have sample time series data stored in Snowflake, you can read the
data back into your Coiled cluster in parallel via a distributed fetch:

.. code-block:: python

   from dask_snowflake import read_snowflake

   ddf = read_snowflake(
       query="""
         SELECT *
         FROM dask_snowflake_table;
      """,
       connection_kwargs=connection_kwargs,
   )

   print(ddf.head())

After a few seconds, you should see the results. As usual, Dask only loads the
data that it needs, and operations in Dask are lazy until computed. You can now
work with Dask as usual to perform computations in parallel.


Step 9: Work with Dask
^^^^^^^^^^^^^^^^^^^^^^

After you've loaded data on to your Coiled cluster, you can perform typical Dask
operations:

.. code-block:: python

   result = ddf.X.mean()
   print(result.compute())

After the computation completes, you should see output similar to the following:

.. code-block:: text

   0.00020641088610962797

You can run through the example again and increase the size of the sample
dataset or scale up your Coiled cluster. This is also a good point to repeat the
previous step and try loading other datasets that you have stored in Snowflake.


Complete example code
^^^^^^^^^^^^^^^^^^^^^

Click :download:`here <snowflake-example.py>` to download a script that contains
all of the Python code that was used in this example.
