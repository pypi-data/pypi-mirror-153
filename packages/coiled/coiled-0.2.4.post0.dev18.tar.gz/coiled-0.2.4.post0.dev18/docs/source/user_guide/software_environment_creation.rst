.. _creating-software-environments:

==============================
Creating software environments
==============================

.. currentmodule:: coiled

Creating software environments with Coiled is handled by a single
:meth:`coiled.create_software_environment` function. You must provide each
software environment you create with a name (must be lowercase) to identify the
environment, the set of packages you want installed into the environment, and
(optionally) any additional setup steps that you want to run. Coiled will then
build a software environment for you which can be used locally or remotely on a
Dask cluster.

.. _software-specifications:

Software specifications
-----------------------

You can specify how to build a Coiled software environment in a variety of ways:
using conda, pip, and/or Docker images.

Conda
^^^^^

To create a software environment with conda packages installed, use the
``conda=`` keyword argument of ``coiled.create_software_environment``. The input
to ``conda=`` can be formatted in three different ways. First you can provide a
list of packages to be install into the environment. For example:

.. code-block:: python

    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray=0.15.1", "numba"]
    )

will build a software environment named "my-conda-env" and use conda to install
dask, version 0.15.1 of xarray, and numba from the ``defaults`` conda channel.
If the name of your environment contains uppercase characters, they will be
converted to lowercase.

Additionally, more complex package specifications, like installing packages from
additional conda channels, are supported by passing a dictionary to ``conda=``.
For example:

.. code-block::

    coiled.create_software_environment(
        name="my-conda-env",
        conda={"channels": ["conda-forge", "defaults"],
               "dependencies": ["dask", "xarray=0.15.1", "numba"]},
    )

will search for packages in both the ``conda-forge`` and ``defaults`` channels.
Equivalently, you can also provide an input conda environment YAML file:

.. code-block:: python

    coiled.create_software_environment(
        name="my-conda-env",
        conda="environment.yml",
    )

where ``environment.yml`` is a local file with the following content:

.. code-block:: yaml

    # environment.yml
    channels:
      - conda-forge
      - defaults
    dependencies:
      - dask
      - xarray=0.15.1
      - numba


Pip
^^^

To create a software environment with pip packages installed, use the ``pip=``
keyword argument of ``coiled.create_software_environment``. The input to
``pip=`` can be formatted in two different ways: a list of packages (on
`PyPI <https://pypi.org/>`_) to install or a pip requirements file.

For example:

.. code-block:: python

    coiled.create_software_environment(
        name="my-pip-env",
        pip=["dask[complete]", "xarray==0.15.1", "numba"],
    )

will build a software environment named "my-pip-env" and use pip to install
dask, version 0.15.1 of xarray, and numba.

Equivalently, you may specify a pip requirements file:

.. code-block:: python

    coiled.create_software_environment(
        name="my-pip-env",
        pip="requirements.txt",
    )

where ``requirements.txt`` is a local file with the following content:

.. code-block::

    # requirements.txt
    dask[complete]
    xarray==0.15.1
    numba

.. attention::

    Pip does not automatically install ``distributed`` along with ``dask``.
    Specify dask with ``dask[complete]`` or ``dask[distributed]`` as in the
    examples above to ensure that distributed is installed.


Private Repositories
""""""""""""""""""""

To use pip packages hosted in private repositories you must add a personal
access token to your Coiled profile, which allows Coiled to pip install these
packages on your behalf. To create a GitHub personal access token, follow the
steps in GitHub's
`Creating a personal access token guide <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_.
After you've created your access token, add it to your profile page at
https://cloud.coiled.io/profile.

When specifying a pip package from a private repository use the format:

.. code-block:: text

    git+https://GIT_TOKEN@github.com/<github_account>/<github_repo>.git

For example:

.. code-block:: python

    coiled.create_software_environment(
        name="my-pip-env",
        pip=[
            "dask[complete]",
            "xarray==0.15.1",
            "numba",
            "git+https://GIT_TOKEN@github.com/coiled/private_package.git",
        ],
    )

will build a software environment named "my-pip-env" and use pip to install
dask, version 0.15.1 of xarray, numba, and the pip package stored in the private
``coiled/private_package`` repository on GitHub.

.. attention::

    For security reasons, you should **not** use your actual personal access
    token when specifying pip requirements. Instead, use the literal string
    ``GIT_TOKEN`` which acts as a placeholder for your personal access token.
    Your actual access token will be populated when Coiled builds the
    corresponding software environment.


Note that you can also use the same ``GIT_TOKEN`` format for private packages in
a pip ``requirements.txt`` file.


Docker
^^^^^^

Any Docker image on `Docker Hub <https://hub.docker.com/>`_ can be used to build
a custom software environment for your cluster by using the ``container=``
keyword argument of of :meth:`coiled.create_software_environment`. For example:

.. code-block::

    coiled.create_software_environment(
        name="my-docker-env",
        container="rapidsai/rapidsai:latest",
    )

will build a software environment named "my-docker-env" using latest RAPIDS
Docker image.

You can also use Coiled to convert conda/pip environments into Docker images stored
in your Docker Hub or other container registry. See the 'Backend options' section
below for more information.

.. _minimal-docker:

Building a minimal Docker image
"""""""""""""""""""""""""""""""

As a bare minimum Coiled needs a Python interpreter with the ``dask``, ``distributed``,
``pandas`` and ``bokeh`` packages installed. Here's a minimal ``Dockerfile`` that meets
these requirements:

.. code-block::

    FROM python:3.8.12

    RUN pip install pandas dask distributed bokeh

It is recommended to specify package versions to avoid version mismatches between the worker
and client environments. For example, if the local environment you're running the client in
has Python 3.8, ``pandas`` version 1.3.3 ``dask`` version 2021.11.2, ``distributed`` version
2021.11.2, you could build a Docker image that matches your local environment with this
``Dockerfile``:

.. code-block::

    FROM python:3.8.12

    RUN pip install pandas==1.3.3 dask==2021.11.2 distributed==2021.11.2 bokeh>=2.1.1

.. note::

    This minimal recipe will not work if you try to install extra dependencies with the command
    ``coiled.create_software_environment()``, if you wish to install extra dependencies with
    this command, you need to install conda in the docker image.



Post build commands
-------------------

Sometimes installing packages with pip and conda isn't enough to fully set up
the software environment you want. For example, JupyterLab extensions sometimes
require additional command(s) to be run as part of their installation. To
support these use cases, ``coiled.create_software_environment`` has a
``post_build=`` keyword argument for running a series of commands after conda
and pip packages have been installed.

For example, the following creates a software environment with conda packages
for Dask, JupyterLab, Node.js, and the
`Dask JupyterLab extension <https://github.com/dask/dask-labextension>`_
installed, then runs two additional commands to complete the JupyterLab
extension installation:

.. code-block::

    coiled.create_software_environment(
        name="my-jupyterlab-env",
        conda=["dask", "jupyterlab", "nodejs", "dask-labextension"],
        post_build=["jupyter labextension install dask-labextension",
                    "jupyter serverextension enable dask_labextension"],
    )

Note that the commands listed in ``post_build`` are assumed to be POSIX shell
compatible.


Environment Variables
---------------------

To add environment variables to your software environments, use the ``environ``
keyword argument of ``coiled.create_software_environment``. The input of ``environ``
should be a dictionary.

.. code-block::

    coiled.create_software_environment(
        name="my-jupyterlab-env",
        conda=["dask", "jupyterlab", "nodejs", "dask-labextension"],
        environ={"DASK_COILED__ACCOUNT": "alice",
                 "DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING": True,
                 "DASK_DISTRIBUTED__LOGGING__DISTRIBUTED": "info"},
    )

.. attention::

    Environment variables are not encrypted and will be available as plain text.
    For security reasons, you should **not** use environment variables to store secrets
    in your software environments.

.. attention::

   Environment variables currently do not work with container only software environments.


Backend options
---------------

Depending on where you're running Coiled, there may be backend-specific options
(e.g. which AWS region or which container registry to use) that you can specify to customize Coiled's behavior. 

By default, Coiled software environments are stored as Docker images to the container registry of the cloud service provider you are using (e.g. ECR for AWS). You can change this in your `Coiled Cloud dashboard <https://cloud.coiled.io/>`_ "Account" settings. For example, you can use Coiled to create Docker images from conda/pip environments that are then saved to your Docker Hub registry. 

For more information on what options are available, see the
:doc:`backends` documentation.


Composing software specifications
---------------------------------

As discussed in the :ref:`software-specifications` section, you can use conda,
pip, and Docker images together to construct a software environment. However,
there are some assumptions that are made during the build process, in particular
when using a custom Docker image, that are important to know about.

Conda and pip packages are installed in a fairly straightforward way. First, if
any conda packages are specified, they are installed into a conda environment.
Next, if any pip packages are specified, they are pip installed. Note that if
any conda packages were installed, then pip packages will also be installed into
the same conda environment -- otherwise they will be installed using the default
Python environment.

Finally, when using a custom Docker image as a base for the software
environment, conda must be installed, and on the current ``PATH``, in order to
install conda packages. Likewise, pip must be installed, and on the current
``PATH``, for pip packages to be installed. By default conda packages will be
installed into a conda environment named ``"coiled"``. If you would like conda
packages to be installed into a different conda environment (e.g. you're using a
custom Docker image which uses a environment not named ``"coiled"``), then you
may pass the name of the conda environment to the ``conda_env_name=`` keyword
for ``coiled.create_software_environment``.


.. _software-visibility:

Visibility
----------

By default, software environments can be viewed and used by any coiled user. If
you want a software environment to be visible only to members of your account,
call :meth:`coiled.create_software_environment` with ``private=True``

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="my-docker-env",
       container="rapidsai/rapidsai:latest",
       private=True,
   )
