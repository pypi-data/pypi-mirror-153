Data sources (MongoDB)
========================

.. note::

   The ``dask-mongo`` connector is currently in beta.

`MongoDB <https://www.mongodb.com/>`_ is a document database MongoDB designed
for ease of development and scaling. Coiled helps scale Python workloads by
provisioning cloud-hosted Dask clusters on demand.

Coiled and MongoDB work great together - MongoDB handles the data storage and
indexing while Coiled handles the backend infrastructure for dealing with large
computations in Python.

Loading data from MongoDB into Python or Dask typically involves the use of
`PyMongo <https://github.com/mongodb/mongo-python-driver>`_ to interact with
data in MongoDB. This works well for small datasets, but can be a limiting
factor when working with larger datasets and more complex queries.

The `dask-mongo <https://github.com/coiled/dask-mongo>`_ connector enables
parallel reads and writes between MongoDB and Dask clusters in Coiled. This
example walks through the use of the ``dask-mongo`` connector and the steps to
configure Coiled to read and write large datasets in parallel and then perform
typical distributed computations on that data with Dask.


Prerequisites
^^^^^^^^^^^^^

- An account on Coiled Cloud to provision Dask clusters
- A local Python environment that can connect to and read from MongoDB
- A cluster hosted on MongoDB Atlas with the ``sample_airbnb`` sample data set
  loaded


Step 1: Install dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In your development environment, install the following dependencies:

.. code-block:: text

   pip install -U \
        "dask[distributed, diagnostics, dataframe]" \
        "coiled" \
        "pymongo[srv]" \
        "git+https://github.com/coiled/dask-mongo.git"


Step 2: MongoDB cluster
^^^^^^^^^^^^^^^^^^^^^^^

For this example, we'll create a hosted database cluster using MongoDB Atlas and
then load sample data into the cluster. If you're already running your own
MongoDB instance with your own data, then you can proceed to the next step.

- Create a MongoDB Atlas cluster by following the documentation steps to
  `Get Started with Atlas <https://docs.atlas.mongodb.com/getting-started/>`_.
- For the purposes of this example, when you configure network access, you can
  allow connections from any IP address to allow the Dask workers from Coiled to
  connect to your MongoDB instance.
- When you create a database user, be sure to save your credentials, which
  you'll use in a connection string with Dask in a later step.
- Follow the steps to
  `Load Sample Data <https://docs.atlas.mongodb.com/sample-data/>`_ that
  includes the ``sample_airbnb`` data set into your MongoDB cluster.


Step 3: Create environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a software environment called ``coiled-mongodb`` that contains the
required dependencies:

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="coiled-mongodb",
       pip=[
           "dask[distributed, diagnostics, dataframe]",
           "pymongo[srv]",
           "git+https://github.com/coiled/dask-mongo.git",
       ],
   )

Note that we specified the same dependencies that you installed in your local
development environment, which ensures consistency between your local
environment and the remote Coiled cluster.

When you create a cluster that uses this environment, these dependencies will be
made available on all of the Dask workers in your cluster. Refer to the
documentation on
:doc:`creating software environments <../software_environment_creation>` for
more information on handling dependencies on your Coiled cluster.


Step 4: Coiled cluster
^^^^^^^^^^^^^^^^^^^^^^

Create a Dask cluster with Coiled that uses your new software environment:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(
       name="coiled-mongodb",
       software="coiled-mongodb",
       n_workers=10,
   )

   from dask.distributed import Client

   client = Client(cluster)
   print("Dashboard:", client.dashboard_link)

The above code example also connects Dask to your Coiled cluster and prints a
link to the Dask dashboard, which you can use later to view the progress of
parallel reads and writes to MongoDB.

The ``software="coiled-mongodb"`` parameter instructs your cluster to use the
software environment that you creates with the ``dask``, ``dask-mongo``, and
other packages included as dependencies.


Step 5: Read data in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you've installed the necessary dependencies for working with Dask and
MongoDB and you have a running Coiled cluster, you can use ``dask-mongo`` and
the ``read_mongo`` functionality to read the sample data in parallel with
Dask/Coiled:

.. code-block:: python

   from dask_mongo import read_mongo

   # Replace the username, password, and cluster address with your own connection details
   host_uri = "mongodb+srv://<username>:<password>@<mongodb-cluster-address>/myFirstDatabase?retryWrites=true&w=majority"

   bag = read_mongo(
       connection_kwargs={"host": host_uri},
       database="sample_airbnb",
       collection="listingsAndReviews",
       chunksize=500,
   )

   bag.take(1)

After a few seconds, you should see the first record from the dataset. As usual, Dask only loads the
data that it needs, and operations in Dask are lazy until computed. You can now
work with Dask as usual to perform computations in parallel.


Step 6: Work with Dask
^^^^^^^^^^^^^^^^^^^^^^

After you've loaded data on to your Coiled cluster, you can perform typical Dask
operations:

.. code-block:: python

   bag.pluck("property_type").frequencies().compute()

After the computation completes, you should see output similar to the following:

.. code-block:: text

   [('House', 606),
   ('Apartment', 3626),
   ('Condominium', 399),
   ('Loft', 142),
   ('Guesthouse', 50),
   ('Hostel', 34),
   ('Serviced apartment', 185),
   ('Bed and breakfast', 69),
   ('Treehouse', 1),
   ('Bungalow', 14),
   ...
   ('Casa particular (Cuba)', 9),
   ('Barn', 1),
   ('Hut', 1),
   ('Camper/RV', 2),
   ('Heritage hotel (India)', 1),
   ('Pension (South Korea)', 1),
   ('Campsite', 1),
   ('Houseboat', 1),
   ('Castle', 1),
   ('Train', 1)]

Let's perform a more complex groupby operation:

.. code-block:: python

   def process(record):
       try:
           yield {
               "accomodates": record["accommodates"],
               "bedrooms": record["bedrooms"],
               "price": float(str(record["price"])),
               "country": record["address"]["country"],
           }
       except KeyError:
           pass


   # Filter only apartments
   b_flattened = (
       bag.filter(lambda record: record["property_type"] == "Apartment")
       .map(process)
       .flatten()
   )
   b_flattened.take(3)

   ddf = b_flattened.to_dataframe()
   ddf
   ddf.head()

   ddf.groupby(["country"])["price"].mean().compute()

After the computation completes, you should see output similar to the following:

.. code-block:: text

   country
   Australia        168.174174
   Brazil           485.767033
   Canada            84.860814
   Hong Kong        684.622120
   Portugal          66.112272
   Spain             91.846442
   Turkey           366.143552
   United States    137.884228
   China            448.300000
   Name: price, dtype: float64

You can monitor the progress of the parallel read operations while they run by
viewing the Dask dashboard.


Step 7: Write data in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can write data back to MongoDB in parallel using the ``to_mongo``
functionality:

.. code-block:: python

   import dask.bag as db
   from dask_mongo import to_mongo

   new_bag = db.from_delayed(
       ddf.map_partitions(lambda x: x.to_dict(orient="records")).to_delayed()
   )

   new_bag.take(1)

   to_mongo(
       new_bag,
       database="new_database",
       collection="new_collection",
       connection_kwargs={"host": host_uri},
   )

You can run through the example again and explore other parts of the sample
dataset or scale up your Coiled cluster. This is also good point to try loading
other datasets that you have stored in MongoDB.


Complete example code
^^^^^^^^^^^^^^^^^^^^^

Click :download:`here <mongodb-example.py>` to download a script that contains
all of the Python code that was used in this example.
