==============================
How to upload a file to Coiled
==============================

When you launch a Cluster to run a computation, you might need to upload
some files to the cluster or perhaps the library requires you to run some
command to download extra files. In this article, we will show you different
ways how you can upload a file to Coiled.

Using the post_build command
----------------------------

When you create a :doc:`software environment <../software_environment_creation>`
you can use the keyword argument ``post_build`` to run a command or adding a path
to a local executable script.

Let's assume that you will use the `spaCy <https://spacy.io/>`_ library in your
computations. You can run the command ``python -m spacy download en_core_web_sm``
to download and install a trained pipeline. You can do this with the ``post_build``
command, for example:

.. code:: python

    import coiled

    coiled.create_software_environment(
        name="spacy",
        conda=["distributed", "dask"],
        pip=["spacy"],
        post_build=["python -m spacy download en_core_web_sm"],
    )

The post build command will run after the conda and pip have installed all
the dependencies.

Using Dask's upload_file command
--------------------------------

Dask allows you to upload a file using the Distributed Client method 
`upload_file <https://distributed.dask.org/en/latest/api.html?highlight=upload_file#distributed.Client.upload_file>`_.
Let's assume that you have a python script that you would like to have 
access while your cluster is running.

.. code:: python

    import coiled
    from dask.distributed import Client

    cluster = coiled.Cluster()
    client = Client(cluster)

    client.upload_file("my_script.py")

As you can see, using the ``upload_file`` allows you to upload a file to a running
cluster, while using the ``post_build`` command can only be used when we rebuild your
software environment.

.. note::

  Using the ``upload_file`` method will also upload the file to all workers.

Using Dask's PipInstall Plugin
------------------------------

If you have a module in GitHub/GitLab you can install this module using Dask's
`PipInstall plugin <https://distributed.dask.org/en/latest/plugins.html?highlight=PipInstall#distributed.diagnostics.plugin.PipInstall>`_
to install your module. This is a great way to upload modules that are in development
or aren't in Conda/Pypi but live in private repositories.

You can upload a public module in GitHub like this

.. code-block:: python

  from dask.distributed.diagnostics.plugin import PipInstall

  plugin = PipInstall(packages=["git+<github url>"])
  client.register_worker_plugin(plugin, name="<dependency name>")

If you want to install from a private repository you need to have a GitHub token set
in your account by either have signed in with GitHub or by 
:doc:`adding your GitHub token to your profile <github_tokens>`.

.. code-block:: python

  from dask.distributed.diagnostics.plugin import PipInstall

  plugin = PipInstall(packages=["git+https://{GITHUB_TOKEN}@github.com/<repo>"])
  client.register_worker_plugin(plugin, name="<dependency name>")

.. note::

   Using the ``name=`` argument will allow you to call ``PipInstall`` more than
   one time, otherwise you might see a message from workers similar to:
   ``{'tls://10.4.1.170:38403': {'status': 'repeat'}``
  
Using Dasks's UploadDirectory Plugin
------------------------------------

Similar to the PipInstall Plugin, you can upload a local directory to your
cluster by using the
`UploadDirectory plugin <https://distributed.dask.org/en/latest/plugins.html?highlight=PipInstall#built-in-nanny-plugins>`_.

You can upload a local directory from your machine to the cluster using:

.. code-block:: python

  from distributed.diagnostics.plugin import UploadDirectory

  client.register_worker_plugin(UploadDirectory("/path/to/directory"), nanny=True)

.. note::

  If you use any of the Dask Plugins to upload directories/modules, new workers
  that are created after > the call, will get the directory/module that you
  uploaded before?

Creating a docker image
-----------------------

Let's assume that you have many files that you would like to include when using Coiled.
Perhaps it would make sense to build a custom docker image containing all the files you
might need. 

When you build a software environment with Coiled, you can use the keyword argument 
``container=`` to include your custom image.

.. code-block:: python

    import coiled

    coiled.create_software_environment(
        name="custom-container",
        container="user/custom-container:latest",
        conda=["distributed", "dask"],
    )

Note that you can also include dependencies to your docker container so you don't have to
install everything using the ``conda`` or ``pip`` keyword argument.
