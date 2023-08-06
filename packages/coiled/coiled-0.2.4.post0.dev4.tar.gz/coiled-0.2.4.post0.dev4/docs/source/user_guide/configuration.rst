.. _configuration:

=============
Configuration
=============

The ``coiled login`` command line tool automatically creates and populates the ``~/.config/dask/coiled.yaml`` configuration file for you. This page covers going beyond the default configuration settings for users who require more customization.

Coiled uses Dask's built in configuration system. For a comprehensive overview on
configuration options see the `Dask documentation on configuration <https://docs.dask.org/en/latest/configuration.html>`_. Namely, configuration settings can be set:

- In the configuration file ``~/.config/dask/coiled.yaml``
- Using environment variables like ``DASK_COILED__ACCOUNT="alice"``
- Configured directly in Python code using ``dask.config.set``

Specifying configuration settings
---------------------------------

You can use a YAML file to specify configuration settings (see the `Dask documentation configuring with YAML files <https://docs.dask.org/en/stable/configuration.html#yaml-files>`_). The snippet below shows some possible configuration options and their default values:

.. code-block:: yaml

    coiled:
      account: null                      # Default account
      backend-options: null              # Default backend_options
      server: https://cloud.coiled.io    # Default server
      token: ""                          # Default token
      user: ""                           # Default username

Configuration options can also be set using environment variables prefixed with ``DASK_COILED__``. Dask uses all environment variables starting with ``DASK_`` and interprets a double underscore as nested access (see the `Dask documentation on configuring with environment variables <https://docs.dask.org/en/stable/configuration.html#environment-variables>`_).

The ``dask.config.set`` function can also be used to set configuration values; it accepts a dictionary and will interpret a period as nested access (see the `Dask documentation on configuring within Python <https://docs.dask.org/en/stable/configuration.html#directly-within-python>`_).

.. list-table:: Equivalent ways of setting commonly used configuration values 
   :widths: 15 25 15 50
   :header-rows: 1

   * - YAML Key
     - Environment variable
     - ``dask.config.set``
     - Description
   * - ``account``
     - ``DASK_COILED__ACCOUNT``
     - ``dask.config.set({"coiled.account": <your-account-name>})``
     - The Coiled account you want to use.
   * - ``token``
     - ``DASK_COILED__TOKEN``
     - ``dask.config.set({"coiled.token": <your-token>})``
     - The Coiled token for your personal account.
   * - ``software``  
     - ``DASK_COILED__SOFTWARE``
     - ``dask.config.set({"coiled.software": <your-senv-name>})``
     - Name of the software environment to use.

The ``account`` option
^^^^^^^^^^^^^^^^^^^^^^

If you are part of a :doc:`teams account <teams>`, and you know that you will
launch clusters mostly in your team account, you can set the ``account`` option
to point to to your team slug (a human-readable unique identifier).
By setting this option, the default behavior of
launching clusters or any other service in your account is overwritten and will
use the team account instead.

You can pass your team account slug in the  ``coiled login`` command line tool
with the ``-a`` or ``--account`` flag as follows:

.. code-block:: bash

    $ coiled login --account team_slug


The ``account`` keyword argument is also accepted in most of our :doc:`API <api>`,
this keyword argument gives you the flexibility of switching between your team
and personal accounts when using the Coiled API.

.. note::

  You don't need a distinct token to use your team account -- please continue to
  use your personal token


The ``backend-options`` option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several :doc:`backend specific <backends>` options that you can
specify to customize Coiled's behaviour. For example, if you are using a
specific region to keep your assets and you want always to use this region when
using Coiled, then you could add it to this configuration file to overwrite
Coiled's default region choice.

.. code-block::yaml

    coiled:
      account: null
      backend-options:
        region: us-east-1
      server: https://cloud.coiled.io    # Default server
      token: ""                          # Default token
      user: ""


.. note::

  Make sure to check if your region is supported in the
  :doc:`backends documentation <backends>`. If your region is not supported you
  can :doc:`get in touch with us <support>`.
