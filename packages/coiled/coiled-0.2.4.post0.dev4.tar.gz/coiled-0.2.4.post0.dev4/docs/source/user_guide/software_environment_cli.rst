======================
Command line interface
======================

All the software environment management functionality supported in Python (e.g.
:meth:`coiled.create_software_environment`) is also available via the command
line.

The table below lists each software environment Python function along with its
corresponding CLI command:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Python
     - Command line
   * - ``coiled.create_software_environment``
     - ``coiled env create``
   * - ``coiled.delete_software_environment``
     - ``coiled env delete``
   * - ``coiled.list_software_environment``
     - ``coiled env list``
   * - ``coiled.install``
     - ``coiled install``
   * - ``coiled.inspect``
     - ``coiled env inspect``


CLI Reference
-------------

.. click:: coiled.cli.env:create
   :prog: coiled env create
   :show-nested:

.. click:: coiled.cli.env:delete
   :prog: coiled env delete
   :show-nested:

.. click:: coiled.cli.env:list
   :prog: coiled env list
   :show-nested:

.. click:: coiled.cli.env:inspect
   :prog: coiled env inspect
   :show-nested:

.. click:: coiled.cli.install:install
   :prog: coiled install
   :show-nested:
