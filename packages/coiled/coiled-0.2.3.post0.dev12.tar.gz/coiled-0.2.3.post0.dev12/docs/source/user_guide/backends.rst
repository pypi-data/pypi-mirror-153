Backends
========

Coiled manages launching Dask clusters and creating software environments for
you. A crucial part of this process is specifying exactly *where* Coiled should
run (i.e., if Coiled should run on AWS or GCP).

By default, Coiled will run on AWS inside Coiled's own AWS account. This makes
it easy for you to get started quickly, without needing to set up any additional
infrastructure. However, you can run Coiled on different cloud provider backends
depending on your needs.

You can configure which cloud provider (i.e., "backend") that you want Coiled to
use for provisioning Dask clusters by visiting the "Account" page of your Coiled
account at ``https://cloud.coiled.io/<account-name>/account``. More information
about each backend is available below.

AWS
---

By default, Coiled will run on AWS inside Coiled's own AWS account. This makes
it easy for you to get started quickly, without needing to set up any additional
infrastructure.

However, you may prefer to run Coiled-managed computations within your own
infrastructure for security or billing purposes. To facilitate this, you can
also have Coiled run computations inside your own AWS account.

.. link-button:: backends_aws
    :type: ref
    :text: Learn more about the AWS backend
    :classes: btn-full btn-block

GCP
---

If you prefer to use Google Cloud Platform (GCP), you can run Coiled on GCP to
run your computations. Coiled can be configured to run on Coiled's GCP account
or your own GCP account.

.. link-button:: backends_gcp
    :type: ref
    :text: Learn more about the GCP backend
    :classes: btn-full btn-block
