=============================
How to change backend regions
=============================

Coiled's default backend region might not be the one that you wish to use. 
Maybe you are closer to a different region; perhaps you have data you would
like to access in a specific region.

There are different ways that you can change your region. This article, 
will show you what these different ways are and their benefits.

Changing region per Cluster basis
---------------------------------

Let's assume that you have ``AWS (VM)`` as your backend. This backend, by default,
will use the  ``us-east-1`` region. You can change this behaviour by passing
the keyword argument ``backend_options`` to the ``coiled.Cluster`` constructor.

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(backend_options={"region_name": "us-east-2"})


This example will create a cluster in AWS ``us-east-2`` region and use Coiled's
default cluster configuration. 

.. note::

    Any options specified with the ``backend_options`` will take precedence over 
    those stored in the ``coiled.backend-options`` configuration value.

Changing region on your Account
-------------------------------

Let's assume that you have all your data in ``us-west-1``, and you will always 
want to use this region when creating clusters and running computations. We can 
save your desired region so you don't have to use the keyword argument ``backend_options``
from the ``coiled.Cluster`` constructor all the time.

To change the region on your Account, head over to your account page on `cloud.coiled.io <https://cloud.coiled.io>`_, 
then in the **Cloud Provider Configuration** click the **EDIT** button and select a different
region from the **region** dropdown menu.

Changing region on your local configuration file
------------------------------------------------

This method is similar to changing regions on your Account, but requires you to edit 
the ``coiled.yaml`` configuration file that lives in ``~/.config/dask/coiled.yaml``. 
If you open this file, you will see something like this:

.. code-block:: yaml

    coiled
      account: null
      backend-options: null
      server: https://cloud.coiled.io
      token: <your token>
      user: <your username>


We can edit the ``backend-options`` to include your desired region, for example:

.. code-block:: yaml

    coiled
      account: null
      backend-options:
        region: us-east-2
      server: https://cloud.coiled.io
      token: <your token>
      user: <your username>

.. note::
    Indentation is done with two spaces because this configuration file is a ``yaml`` file.