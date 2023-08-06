Performance Reports
===================

Overview
--------

Dask and Coiled help you understand computational performance and profile your
distributed workload in terms of cluster utilization, workload profiling,
network communication, task execution, and more. Dask provides an interactive
dashboard that shows various plots and tables that update with live information
as computations are running.

In addition to the interactive dashboard, Dask has the ability to generate
static
`performance reports <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
and save the results to a standalone HTML file. These performance reports are
useful for later inspection since they can be viewed after your computation is
finished and your Coiled cluster is no longer running.

.. figure:: images/performance-report-profile.png
   :width: 100%

Coiled also provides functionality to generate performance reports using the
same functionality in Dask, but with the added step of uploading the performance
report to Coiled Cloud. This makes it easier to share performance reports with
other members of your team or with Dask experts at Coiled without having to
email or send around an HTML file.


Generating performance reports
------------------------------

To generate a performance report and upload it to Coiled Cloud, simply wrap the
Dask code that you want to profile with the :meth:`coiled.performance_report`
context manager:

.. code-block:: python

    from coiled import performance_report

    with performance_report(filename="dask-report.html"):
        df.groupby(...).value.mean().compute()  ## Your dask computation(s)

After the computation finishes, the Coiled client will output a message that
includes a link to your hosted performance report:

.. code-block::

    Performance Report Available at: https://cloud.coiled.io/your-username/reports/74

That's it! Your performance report is now available on Coiled Cloud and is ready
to be viewed or shared with others. You can open the link in your browser to
view and explore it within the Coiled Cloud interface:

.. figure:: images/performance-report-tasks.png
   :width: 100%

The video below walks you through generating a performance report using Coiled.

.. raw:: html

   <div style="display: flex; justify-content: center;">
       <iframe width="560" height="315" src="https://www.youtube.com/embed/hJMINENeEQA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>


Viewing performance reports
---------------------------

You can view a list of the performance reports that you've uploaded to Coiled
Cloud by calling :meth:`coiled.list_performance_reports`, which will return a
list of all performance reports and a URL where they can be viewed:

.. code-block:: python

    coiled.list_performance_reports()

.. code-block:: python

    [
        {
            "private": False,
            "filename": "performance_report.html",
            "url": "https://cloud.coiled.io/your-username/reports/1",
        },
        {
            "private": False,
            "filename": "performance_report.html",
            "url": "https://cloud.coiled.io/your-username/reports/2",
        },
        {
            "private": False,
            "filename": "performance_report.html",
            "url": "https://cloud.coiled.io/your-username/reports/3",
        },
    ]


Performance reports in a Team account
-------------------------------------

If you want to generate and upload a performance report to a Team account on
Coiled, you can use the ``account=`` option, as in:

.. code-block:: python

    from coiled import performance_report

    with performance_report(filename="dask-report.html", account="my-team-account"):
        df.groupby(...).value.mean().compute()  ## Your dask computation(s)


Visibility
----------

By default, performance reports can be viewed by anyone with the link (no Coiled account
required). If you want your performance report to be visible only to you or members of your
team account, then you can use the ``private=True`` option, as in:

.. code-block:: python

    from coiled import performance_report

    with performance_report(filename="dask-report.html", private=True):
        df.groupby(...).value.mean().compute()  ## Your dask computation(s)
