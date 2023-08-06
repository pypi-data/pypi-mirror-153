.. _jupyterlab-guide:

==========
JupyterLab
==========

Coiled integrates with the tools you already use. When it comes to using Coiled
with `JupyterLab <https://jupyterlab.readthedocs.io/en/latest/>`_, there are a
few useful open source JupyterLab extensions that we recommend trying out:

- :ref:`Dask JupyterLab extension <jupyterlab-extension>`
- :ref:`nb_conda_kernels extension <nb_conda_kernels>`
- :ref:`Ipywidgets extension <ipywidgets-extension>`


.. _jupyterlab-extension:

Dask JupyterLab extension
-------------------------

The Dask community maintains a
`JupyterLab extension <https://github.com/dask/dask-labextension>`_ which allows
`Dask dashboard plots <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
to be embedded directly into a JupyterLab session. Viewing diagnostic plots in
JupyterLab, instead of in a separate browser tab or window, is often a pleasant
user experience if you find yourself working in JupyterLab a lot.

The Dask JupyterLab extension can be installed with:

.. code-block:: bash

    conda install -c conda-forge jupyterlab nodejs dask-labextension
    jupyter labextension install dask-labextension
    jupyter serverextension enable dask_labextension


Now when you launch JupyterLab there will be a tab with the orange Dask logo in
the left sidebar. You can connect the extension to your Coiled cluster by
copying the Dask dashboard URL for your ``coiled.Cluster`` (available via the
``Cluster.dashboard_link`` attribute) into the Dask tab in the JupyterLab left
sidebar.

.. figure:: images/labextension.png


Dashboard plots are now available for you to embed directly into your JupyterLab
session! Plots are accessible by clicking the orange button with each plot's
name like "Progress" or "Task Stream". You can then click and drag the tabs of
those new windows to construct your ideal workspace. We recommend starting with
the "Task Stream" and "Progress" charts.


.. _nb_conda_kernels:

Conda kernels extension
-----------------------

The
`nb_conda_kernels extension <https://github.com/Anaconda-Platform/nb_conda_kernels>`_
enables you to access other conda environments on your machine from Jupyter
Notebook or JupyterLab. This allows you to smoothly switch between different
Coiled software environments you've installed locally. You can install the
``nb_conda_kernels`` extension with:

.. code-block:: bash

    conda install -c conda-forge nb_conda_kernels


Note that any other environments you wish to access must have a kernel package,
e.g. ``ipykernel``, installed in them. By default any Coiled software
environment you've installed locally with ``coiled install`` will have
``ipykernel`` automatically installed to enable use with ``nb_conda_kernels``.

To select the conda environment to use with a notebook in JupyterLab, click the
text indicating the current kernel in the upper righthand corner of the notebook
(screenshot below). This will bring up a "Select Kernel" dropdown menu where you
can select which kernel you would like to use for the notebook.

.. image:: images/nb_conda_kernels.png


.. _ipywidgets-extension:

Ipywidgets extension
--------------------

`ipywidgets <https://ipywidgets.readthedocs.io/en/latest/index.html>`_ enables
interactive HTML widgets for Jupyter notebooks and JupyterLab. This provides a
rich, responsive user experience when working in Jupyter. The ``coiled.Cluster``
cluster manager utilizes ipywidgets to display an interactive widget in
JupyterLab (screenshot below) which allows you to manually scale up, scale down,
or `adaptively scale <https://docs.dask.org/en/latest/setup/adaptive.html>`_ the
number of workers in your Coiled cluster.

.. image:: images/cluster-repr.png

The ipywidgets JupyterLab extension can be installed with:

.. code-block:: bash

    conda install -c conda-forge ipywidgets nodejs
    jupyter labextension install @jupyter-widgets/jupyterlab-manager

After installing the extension, the cluster widget will now appear any time your
cluster is the output of a JupyterLab notebook cell.
