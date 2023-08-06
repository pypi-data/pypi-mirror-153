Web applications (Streamlit)
============================

`Streamlit <https://streamlit.io/>`_ is an open-source Python library that makes
it easy to create and share custom web apps for machine learning and data
science. Coiled helps scale Python workloads by provisioning cloud-hosted Dask
clusters on demand.

Coiled and Streamlit work great together - Streamlit handles the frontend layout
and interactivity of your web application while Coiled handles the backend
infrastructure for demanding computations.

.. figure:: ../images/coiled-streamlit-example.png
   :width: 100%

And because Coiled works anywhere that you can run Python, you can use Coiled
while developing Streamlit apps on your laptop or while interacting with a
hosted Streamlit application - all without having to download your data or
change the way you work.


Coiled + Streamlit
------------------

The example below uses Coiled and Streamlit to read more than 146 million
records from a data set and visualize locations of taxi pickups and dropoffs. It
does this by reading a number of CSV files from Amazon S3, breaking them into
many small chunks, filtering rows based on the values selected in the input
widgets, then displaying the results on a
`Folium map <https://python-visualization.github.io/folium/>`_ within the
Streamlit app.

We highlight some of the features that Coiled and Streamlit provide:

1. Use named clusters to start a new Coiled cluster or connect to an existing
   cluster from the Streamlit app. This also enables multiple viewers of a
   Streamlit app to share the same Coiled cluster backend.
2. Defer heavy computations to Coiled rather than running them on the machine
   where Streamlit is running.
3. Use interactive widgets in Streamlit that act as inputs to the data filtering
   operations that run on Coiled.
4. Display the results on a map using familiar data structures that are returned
   from the Dask computation.

.. literalinclude:: streamlit-example.py

Click :download:`here <streamlit-example.py>` to download the above example
script.


How Coiled helps
----------------

Coiled comes into play in these sections in the above code example:

.. code-block:: python

   # Start and connect to Coiled cluster
   [...]

   # Load data (runs on Coiled)
   [...]

   # Filter data based on inputs (runs on Coiled)
   [...]

where we setup and connect to a Coiled cluster, then run the requested
computations on the cluster. This lets us easily scale the resources available
to the Streamlit app on the backend.

Also notice that we loaded the data in a separate function/section and persisted
it in memory on the Coiled cluster. This helps to optimize performance of the
Streamlit app and avoids expensive computations from running each time the app
is updated. We'll discuss more best practices like this in the following
section.


Best practices
--------------

Notify when starting Coiled clusters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Streamlit provides methods to display placeholders and update status text in
your app. This is a good way to indicate to users that a :doc:`Coiled cluster is
being created <../cluster_creation>` in the background before the Streamlit app
starts to run computations.

Cache, reuse, and share Coiled clusters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By using ``@st.cache(allow_output_mutation=True)`` around the function creating
the Coiled cluster, the Streamlit app will reuse the same connection to the
cluster, instead of reconnecting every time the app's state changes. Refer to
`caching section <https://docs.streamlit.io/en/stable/caching.html>`__ in the
Streamlit documentation for more information on handling caching for open
connections.

Additionally, by passing a name to our Coiled cluster in
``cluster = coiled.Cluster(name="coiled-streamlit")``, we direct the Coiled
client to create a new named cluster or reconnect to an existing named cluster,
which is useful for :doc:`reusing clusters <../cluster_reuse>` as viewers of
your Streamlit app come and go. This also enables multiple viewers of a
Streamlit app to share the same Coiled cluster backend.

Coiled will automatically shut down your Dask cluster after 20 minutes of
inactivity by default. This helps save on compute costs when your Streamlit app
is not in use. However, if you use ``@st.cache`` on the Coiled cluster and
expect your Streamlit app to run for long time, you should add a
``if client.status == "closed"`` check as shown in the code example above, which
will recreate the cluster if it has shut down. If you don't use ``@st.cache``,
then this check is not necessary since a new Coiled cluster will be created
automatically when another user visits your Streamlit app.

Improve performance by persisting data and caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider which parts of your computation can be preloaded and precomputed, then
`persist that data in memory
<https://docs.dask.org/en/latest/best-practices.html#persist-when-you-can>`_ on
the Coiled cluster to avoid repeated computations when users interact with your
app. Also consider where you can use cache annotations in Streamlit via
``@st.cache`` to optimize performance when calling functions that preload or
precompute data with Dask or other computations that only need to run once.

Note that ``@st.cache`` does not know the best way to tell if two Dask
collections are identical. Therefore, to cache functions that return Dask
collections, you should use
``@st.cache(hash_funcs={dd.DataFrame: dask.base.tokenize})`` and replace
``dd.DataFrame`` with the appropriate datatype that the function returns. Refer
to the the
`caching section <https://docs.streamlit.io/en/stable/caching.html>`__ in the
Streamlit docs for more information on custom hash functions.

Manage software dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use :doc:`software environments <../software_environment>` in Coiled to make
required packages available on all of the Dask workers in your cluster. You can
use the same list of conda or pip packages that your Streamlit app depends on.

Notify on long-running computations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Streamlit provides spinners that can display a message while a block of code is
executing. This is a good way to indicate to users that a long-running
computation is running in the background.

Use Coiled only when needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using Coiled with Streamlit, the same
`best practices for Dask <https://docs.dask.org/en/latest/best-practices.html>`_
also apply. For example, use Coiled for large computations only when you need
to, then return to typical Python data structures before displaying or plotting
the results in Streamlit.
