.. _credentials_api_doc:

#################
Credentials
#################

Credentials for user with Database and Data Storage Connectivity can be stored by the system.

To interact with Credentials API, you should use the :ref:`Credential <credential_api>` class.

***********************
List credentials
***********************

In order to retrieve the list of all credentials accessible for current user you can use
:meth:`Credential.list<datarobot.models.Credential.list>`.

.. code-block:: python

    import datarobot as dr

    credentials = dr.Credential.list()


Each Credential object contains the `credential_id` string field which
can be used e.g. in :ref:`Batch Predictions <batch_predictions_s3_creds_usage>`.


.. _basic_creds_usage:

***********************
Basic credentials
***********************

You can store generic user/password credentials:

.. code-block:: python

    >>> import datarobot as dr
    >>> cred = dr.Credential.create_basic(
    ...     name='my_db_cred',
    ...     user='<user>',
    ...     password='<password>',
    ... )
    >>> cred
    Credential('5e429d6ecf8a5f36c5693e0f', 'my_db_cred', 'basic'),

    # store cred.credential_id

    >>> cred = dr.Credential.get(credential_id)
    >>> cred.credential_id
    '5e429d6ecf8a5f36c5693e0f'

Stored credential can be used e.g. in :ref:`Batch Bredictions for JDBC intake or output <batch_predictions_jdbc_creds_usage>`.

.. _s3_creds_usage:

***********************
S3 credentials
***********************

You can store AWS credentials using the three parameters:

* ``aws_access_key_id``
* ``aws_secret_access_key``
* ``aws_session_token``

.. code-block:: python

    >>> import datarobot as dr
    >>> cred = dr.Credential.create_s3(
    ...     name='my_s3_cred',
    ...     aws_access_key_id='<aws access key id>',
    ...     aws_secret_access_key='<aws secret access key>',
    ...     aws_session_token='<aws session token>',
    ... )
    >>> cred
    Credential('5e429d6ecf8a5f36c5693e03', 'my_s3_cred', 's3'),

    # store cred.credential_id

    >>> cred = dr.Credential.get(credential_id)
    >>> cred.credential_id
    '5e429d6ecf8a5f36c5693e03'

Stored credential can be used e.g. in :ref:`Batch Bredictions for S3 intake or output <batch_predictions_s3_creds_usage>`.


***********************
OAUTH credentials
***********************

You can store oauth credentials in the store:

.. code-block:: python

    >>> import datarobot as dr
    >>> cred = dr.Credential.create_oauth(
    ...     name='my_oauth_cred',
    ...     token='<token>',
    ...     refresh_token='<refresh_token>',
    ... )
    >>> cred
    Credential('5e429d6ecf8a5f36c5693e0f', 'my_oauth_cred', 'oauth'),

    # store cred.credential_id

    >>> cred = dr.Credential.get(credential_id)
    >>> cred.credential_id
    '5e429d6ecf8a5f36c5693e0f'


***********************
Credential Data
***********************

For methods that accept credential data instead of user/password, or credential ID:

.. code-block:: json

    {
        "credentialType": "basic",
        "user": "user123",
        "password": "pass123",
    }

.. code-block:: json

    {
        "credentialType": "s3",
        "awsAccessKeyId": "key123",
        "awsSecretAccessKey": "secret123",
    }

.. code-block:: json

    {
        "credentialType": "oauth",
        "oauthRefreshToken": "token123",
        "oauthClientId": "client123",
        "oauthClientSecret": "secret123",
    }

.. _credential_data:
