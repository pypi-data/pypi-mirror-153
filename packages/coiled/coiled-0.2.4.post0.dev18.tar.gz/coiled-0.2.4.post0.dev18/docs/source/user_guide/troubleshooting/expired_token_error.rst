.. _expired-token-error:

===================
Expired Token error
===================

Under some circumstances, AWS users have encountered errors blamed on expired 
tokens. Often, this occurs when attempting to read/write to an S3 bucket. 

.. code-block::

    ClientError: An error occurred (ExpiredToken) when calling the PutObject 
    operation: The provided token has expired. 
     ...
    PermissionError: The provided token has expired.

It turns out that the best way to deal with this error is to simply wait.  It 
is an AWS issue, and experience shows that you simply need to wait for AWS to
update the token. Alternatively, if you're working from a notebook, consider 
restarting it and spinning up a new cluster for the same workflow, reading/writing
from S3.
