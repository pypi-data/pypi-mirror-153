.. _setup_access_token_error:

========================
Setup Access Token Error
========================

If you are trying to use a software environment that has a dependency located in
a private GitHub repository, you might see the following error message when
creating a cluster.

.. code::

    Traceback (most recent call last):
        # ...
        File "/home/fabiorosado/anaconda3/envs/coiled/lib/python3.8/site-packages/coiled/core.py", line 1225, in _get_software_info
            await handle_api_exception(response)
        File "/home/fabiorosado/anaconda3/envs/coiled/lib/python3.8/site-packages/coiled/utils.py", line 90, in handle_api_exception
            raise exception_cls(", ".join(f"{k}={v}" for (k, v) in error_body.items()))
    Exception: detail=Setup your Access Token to access this object

If you encounter this error, you might need to add your
:doc:`GitHub personal access token <../tutorials/github_tokens>`
to your Coiled profile page. By adding the GitHub token, you will give Coiled
access to private repositories and we should be able to pull the private
dependency from Github.

If you have added your GitHub Access token and you still see this error when
creating clusters, you might need to check with the creator of the software
environment if you have access to the private repository on GitHub.
