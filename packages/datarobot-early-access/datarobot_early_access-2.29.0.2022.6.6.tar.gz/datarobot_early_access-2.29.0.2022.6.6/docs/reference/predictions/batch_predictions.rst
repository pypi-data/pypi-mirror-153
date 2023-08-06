.. _batch_predictions:

.. testsetup:: score_to_file, s3, azure, gcp, manual_wire, s3_csv_intake, jdbc_intake, bigquery_intake,
                ai_catalog_intake, ai_catalog_intake_with_version_id, local_file_output, s3_csv_output,
                jdbc_output, bigquery_output, score_from_existing, score_pandas,
                score_pandas_with_remapping

    import datarobot as dr

    import os
    import mock
    import responses

    # Some odd race condition is causing this to fail after tests have already passed
    dr.models.batch_prediction_job.threading = mock.MagicMock()

    responses.start()

    endpoint = 'http://localhost/api/v2'

    responses.add(
        responses.GET, os.path.join(endpoint, 'version/'), status=200, json={
            'major': 2,
            'minor': 26,
            'versionString': '2.26.0'
        }
    )

    dr.Client(endpoint=endpoint, token='mocked')

    # General 'fixture' that we use all over
    batch_prediction_job_response = {
        'id': 'random_id',
        'status':'COMPLETED',
        'elapsed_time_sec':60,
        'status_details':'something',
        'percentage_completed':60,
        'job_spec':{
          'deployment_id':'whatever',
          'num_concurrent':1
        },
        'links':{
          'self':'whatever',
          'csvUpload':'batchPredictions/random_id/csvUpload/',
          'download':'batchPredictions/random_id/download/'
        }
    }

#################
Batch Predictions
#################

The Batch Prediction API provides a way to score large datasets using flexible options
for intake and output on the Prediction Servers you have already deployed.

The main features are:

* Flexible options for intake and output.
* Stream local files and start scoring while still uploading - while simultaneously downloading the results.
* Score large datasets from and to S3.
* Connect to your database using JDBC with bidirectional streaming of scoring data and results.
* Intake and output options can be mixed and doesn’t need to match. So scoring from a JDBC source to an S3 target is also an option.
* Protection against overloading your prediction servers with the option to control the concurrency level for scoring.
* Prediction Explanations can be included (with option to add thresholds).
* Passthrough Columns are supported to correlate scored data with source data.
* Prediction Warnings can be included in the output.

To interact with Batch Predictions, you should use the :ref:`BatchPredictionJob <batch_prediction_api>` class.

***********************
Scoring local CSV files
***********************

We provide a small utility function for scoring from/to local CSV files: :meth:`BatchPredictionJob.score_to_file <datarobot.models.BatchPredictionJob.score_to_file>`.
The first parameter can be either:

* Path to a CSV dataset
* File-like object
* Pandas DataFrame

For larger datasets, you should avoid using a DataFrame, as that will load
the entire dataset into memory. The other options don't.

.. testsetup:: score_to_file

    dr.models.batch_prediction_job.recognize_sourcedata = mock.MagicMock()

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200, json={'links':{'csvUpload':'batchPredictions/random_id/'}}, adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json=batch_prediction_job_response,
    )

    responses.add(
        responses.PUT, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json={},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/download/'), status=200, json={},
    )

.. testcode:: score_to_file

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    dr.BatchPredictionJob.score_to_file(
        deployment_id,
        './data_to_predict.csv',
        './predicted.csv',
    )

The input file will be streamed to our API and scoring will start immediately.
As soon as results start coming in, we will initiate the download concurrently.
The entire call will block until the file has been scored.

**********************
Scoring from and to S3
**********************

We provide a small utility function for scoring from/to CSV files hosted on S3 :meth:`BatchPredictionJob.score_s3 <datarobot.models.BatchPredictionJob.score_s3>`.
This requires that the intake and output buckets share the same credentials (see :ref:`Credentials <credentials_api_doc>`
and :meth:`Credential.create_s3 <datarobot.models.Credential.create_s3>`) or that their access policy is set to public:

.. testsetup:: s3

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200,
        json={'links': {'csvUpload': 'batchPredictions/random_id/'}},
        adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json=batch_prediction_job_response,
    )

.. testcode:: s3

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    cred = dr.Credential.get('5a8ac9ab07a57a0001be501f')

    job = dr.BatchPredictionJob.score_s3(
        deployment=deployment_id,
        source_url='s3://mybucket/data_to_predict.csv',
        destination_url='s3://mybucket/predicted.csv',
        credential=cred,
    )

.. note:: The S3 output functionality has a limit of 100 GB.

***************************************
Scoring from and to Azure Cloud Storage
***************************************

Like with S3, we provide the same support for Azure through the utility function :meth:`BatchPredictionJob.score_azure <datarobot.models.BatchPredictionJob.score_azure>`.
This required that an Azure connection string has been added to the DataRobot credentials store.
(see :ref:`Credentials <credentials_api_doc>` and :meth:`Credential.create_azure <datarobot.models.Credential.create_azure>`)

.. testsetup:: azure

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200,
        json={'links': {'csvUpload': 'batchPredictions/random_id/'}},
        adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json=batch_prediction_job_response,
    )

.. testcode:: azure

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    cred = dr.Credential.get('5a8ac9ab07a57a0001be501f')

    job = dr.BatchPredictionJob.score_azure(
        deployment=deployment_id,
        source_url='https://mybucket.blob.core.windows.net/bucket/data_to_predict.csv',
        destination_url='https://mybucket.blob.core.windows.net/results/predicted.csv',
        credential=cred,
    )

*****************************************
Scoring from and to Google Cloud Platform
*****************************************

Like with Azure, we provide the same support for GCP through the utility function :meth:`BatchPredictionJob.score_gcp <datarobot.models.BatchPredictionJob.score_gcp>`.
This required that an Azure connection string has been added to the DataRobot credentials store. (see :ref:`Credentials <credentials_api_doc>` and
:meth:`Credential.create_gcp <datarobot.models.Credential.create_gcp>`)

.. testsetup:: gcp

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200, json={'links':{'csvUpload':'batchPredictions/random_id/'}}, adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json=batch_prediction_job_response,
    )

.. testcode:: gcp

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    cred = dr.Credential.get('5a8ac9ab07a57a0001be501f')

    job = dr.BatchPredictionJob.score_gcp(
        deployment=deployment_id,
        source_url='gs:/bucket/data_to_predict.csv',
        destination_url='gs://results/predicted.csv',
        credential=cred,
    )

**************************************
Wiring a Batch Prediction Job manually
**************************************

If you can't use any of the utilities above, you are also free to configure
your job manually. This requires configuring an intake and output option:

.. testsetup:: manual_wire

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200, json={'links':{'csvUpload':'batchPredictions/random_id/'}}, adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json=batch_prediction_job_response,
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/download/'), status=200, json={},
    )

.. testcode:: manual_wire

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    dr.BatchPredictionJob.score(
        deployment_id,
        intake_settings={
            'type': 's3',
            'url': 's3://public-bucket/data_to_predict.csv',
            'credential_id': '5a8ac9ab07a57a0001be501f',
        },
        output_settings={
            'type': 'localFile',
            'path': './predicted.csv',
        },
    )

Credentials may be created with :ref:`Credentials API <credentials_api_doc>`.

Supported intake types
----------------------

These are the supported intake types and descriptions of their configuration parameters:

Local file intake
^^^^^^^^^^^^^^^^^

This requires you to pass either a path to a CSV dataset, file-like object or a Pandas
DataFrame as the ``file`` parameter:

.. testcode::

    intake_settings={
        'type': 'localFile',
        'file': './data_to_predict.csv',
    }

S3 CSV intake
^^^^^^^^^^^^^

This requires you to pass an S3 URL to the CSV file your scoring in the ``url`` parameter:

.. testcode::

    intake_settings={
        'type': 's3',
        'url': 's3://public-bucket/data_to_predict.csv',
    }

.. _batch_predictions_s3_creds_usage:

If the bucket is not publicly accessible, you can supply AWS credentials using the three
parameters:

* ``aws_access_key_id``
* ``aws_secret_access_key``
* ``aws_session_token``

And save it to the :ref:`Credential API <s3_creds_usage>`. Here is an example:

.. testsetup:: s3_csv_intake

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

.. testcode:: s3_csv_intake

    import datarobot as dr

    # get to make sure it exists
    credential_id = '5a8ac9ab07a57a0001be501f'
    cred = dr.Credential.get(credential_id)

    intake_settings={
        'type': 's3',
        'url': 's3://private-bucket/data_to_predict.csv',
        'credential_id': cred.credential_id,
    }

JDBC intake
^^^^^^^^^^^

This requires you to create a :ref:`DataStore <database_connectivity_overview>` and
:ref:`Credential <basic_creds_usage>` for your database:

.. testsetup:: jdbc_intake

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'externalDataStores/5a8ac9ab07a57a0001be5010/'), status=200, json={
            'canonicalName': 'Azure Synapse',
            'creator': '60d06e781d7fdbf4ddd19761',
            'params': {
                'driverId': '60e45344c0e21db5df626fe3',
            },
            'type': 'jdbc',
            'updated': '2021-07-06T12:58:10.419000',
            'role': 'OWNER',
            'id': '60e45362c0e21db5df626fe4'
        }
    )

.. testcode:: jdbc_intake

    # get to make sure it exists
    datastore_id = '5a8ac9ab07a57a0001be5010'
    data_store = dr.DataStore.get(datastore_id)

    credential_id = '5a8ac9ab07a57a0001be501f'
    cred = dr.Credential.get(credential_id)

    intake_settings = {
        'type': 'jdbc',
        'table': 'table_name',
        'schema': 'public', # optional, if supported by database
        'catalog': 'master', # optional, if supported by database
        'data_store_id': data_store.id,
        'credential_id': cred.credential_id,
    }

BigQuery intake
^^^^^^^^^^^^^^^

This requires you to create a GCS :ref:`Credential <basic_creds_usage>` for your database:

.. testsetup:: bigquery_intake

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'gcp_creds',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'gcp'
        }
    )

.. testcode:: bigquery_intake

    # get to make sure it exists
    credential_id = '5a8ac9ab07a57a0001be501f'
    cred = dr.Credential.get(credential_id)

    intake_settings = {
        'type': 'bigquery',
        'dataset': 'dataset_name',
        'table': 'table_or_view_name',
        'bucket': 'bucket_in_gcs',
        'credential_id': cred.credential_id,
    }


.. _batch_predictions-intake-types-dataset:

AI Catalog intake
^^^^^^^^^^^^^^^^^

This requires you to create a :ref:`Dataset <datasets>` and identify the `dataset_id` of that to use as input.

.. testsetup:: ai_catalog_intake

    responses.add(
        responses.GET, os.path.join(endpoint, 'datasets/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'datasetId': '60d31d53e200aba43b76f0d4',
            'name': 'pred_6020_2003.csv',
            'isLatestVersion': True,
            'versionId': '60d31d53e200aba43b76f0d5',
            'categories': [
                'TRAINING',
                'PREDICTION',
                'BATCH_PREDICTIONS'
            ],
            'creationDate': '2021-06-23T11:38:59.231000Z',
            'createdBy': 'admin@datarobot.com',
            'isSnapshot': True,
            'isDataEngineEligible': True,
            'processingState': 'COMPLETED',
        }
    )

.. testcode:: ai_catalog_intake

    # get to make sure it exists
    dataset_id = '5a8ac9ab07a57a0001be501f'
    dataset = dr.Dataset.get(dataset_id)

    intake_settings={
        'type': 'dataset',
        'dataset': dataset
    }

Or, in case you want another `version_id` than the latest, supply your own.

.. testsetup:: ai_catalog_intake_with_version_id

    responses.add(
        responses.GET, os.path.join(endpoint, 'datasets/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'datasetId': '60d31d53e200aba43b76f0d4',
            'name': 'pred_6020_2003.csv',
            'isLatestVersion': True,
            'versionId': '60d31d53e200aba43b76f0d5',
            'categories': [
                'TRAINING',
                'PREDICTION',
                'BATCH_PREDICTIONS'
            ],
            'creationDate': '2021-06-23T11:38:59.231000Z',
            'createdBy': 'admin@datarobot.com',
            'isSnapshot': True,
            'isDataEngineEligible': True,
            'processingState': 'COMPLETED',
        }
    )

.. testcode:: ai_catalog_intake_with_version_id

    # get to make sure it exists
    dataset_id = '5a8ac9ab07a57a0001be501f'
    dataset = dr.Dataset.get(dataset_id)

    intake_settings={
        'type': 'dataset',
        'dataset': dataset,
        'dataset_version_id': 'another_version_id'
    }


Supported output types
----------------------

These are the supported output types and descriptions of their configuration parameters:

Local file output
^^^^^^^^^^^^^^^^^

For local file output you have two options. You can either pass a ``path`` parameter and
have the client block and download the scored data concurrently. This is the fastest way
to get predictions as it will upload, score and download concurrently:

.. code-block:: python

    output_settings={
        'type': 'localFile',
        'path': './predicted.csv',
    }

Another option is to leave out the parameter and subsequently call :meth:`BatchPredictionJob.download <datarobot.models.BatchPredictionJob.download>`
at your own convenience. The :meth:`BatchPredictionJob.score <datarobot.models.BatchPredictionJob.score>` call will then return as soon as the upload is complete.

If the job is not finished scoring, the call to :meth:`BatchPredictionJob.download <datarobot.models.BatchPredictionJob.download>` will start
streaming the data that has been scored so far and block until more data is available.

You can poll for job completion using :meth:`BatchPredictionJob.get_status <datarobot.models.BatchPredictionJob.get_status>` or use
:meth:`BatchPredictionJob.wait_for_completion <datarobot.models.PredictJob.wait_for_completion>` to wait.


.. testsetup:: local_file_output

    dr.models.batch_prediction_job.recognize_sourcedata = mock.MagicMock()

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200, json={'links':{'csvUpload':'batchPredictions/random_id/'}}, adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.PUT, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json={},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200,
        json=batch_prediction_job_response,
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/download/'), status=200, json={},
    )


.. testcode:: local_file_output

    import datarobot as dr

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    job = dr.BatchPredictionJob.score(
        deployment_id,
        intake_settings={
            'type': 'localFile',
            'file': './data_to_predict.csv',
        },
        output_settings={
            'type': 'localFile',
        },
    )

    job.wait_for_completion()

    with open('./predicted.csv', 'wb') as f:
        job.download(f)

S3 CSV output
^^^^^^^^^^^^^

This requires you to pass an S3 URL to the CSV file where the scored data should be saved
to in the ``url`` parameter:

.. code-block:: python

    output_settings={
        'type': 's3',
        'url': 's3://public-bucket/predicted.csv',
    }

Most likely, the bucket is not publically accessible for writes, but you can supply AWS
credentials using the three parameters:

* ``aws_access_key_id``
* ``aws_secret_access_key``
* ``aws_session_token``

And save it to the :ref:`Credential API <s3_creds_usage>`. Here is an example:

.. testsetup:: s3_csv_output

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

.. testcode:: s3_csv_output

    # get to make sure it exists
    credential_id = '5a8ac9ab07a57a0001be501f'
    cred = dr.Credential.get(credential_id)

    output_settings={
        'type': 's3',
        'url': 's3://private-bucket/predicted.csv',
        'credential_id': cred.credential_id,
    }

JDBC output
^^^^^^^^^^^

Same as for the input, this requires you to create a :ref:`DataStore <database_connectivity_overview>` and
:ref:`Credential <basic_creds_usage>` for your database, but for `output_settings` you also need to specify
`statementType`, which should be one of ``datarobot.enums.AVAILABLE_STATEMENT_TYPES``:

.. testsetup:: jdbc_output

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'whatever',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'whatever'
        }
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'externalDataStores/5a8ac9ab07a57a0001be5010/'), status=200, json={
            'canonicalName': 'Azure Synapse',
            'creator': '60d06e781d7fdbf4ddd19761',
            'params': {
                'driverId': '60e45344c0e21db5df626fe3',
            },
            'type': 'jdbc',
            'updated': '2021-07-06T12:58:10.419000',
            'role': 'OWNER',
            'id': '60e45362c0e21db5df626fe4'
        }
    )

.. testcode:: jdbc_output

    # get to make sure it exists
    datastore_id = '5a8ac9ab07a57a0001be5010'
    data_store = dr.DataStore.get(datastore_id)

    credential_id = '5a8ac9ab07a57a0001be501f'
    cred = dr.Credential.get(credential_id)

    output_settings = {
        'type': 'jdbc',
        'table': 'table_name',
        'schema': 'public', # optional, if supported by database
        'catalog': 'master', # optional, if supported by database
        'statementType': 'insert',
        'data_store_id': data_store.id,
        'credential_id': cred.credential_id,
    }

BigQuery output
^^^^^^^^^^^^^^^

Same as for the input, this requires you to create a GCS :ref:`Credential <basic_creds_usage>`
to access BigQuery:

.. testsetup:: bigquery_output

    responses.add(
        responses.GET, os.path.join(endpoint, 'credentials/5a8ac9ab07a57a0001be501f/'), status=200, json={
            'credentialId': 'whatever',
            'name': 'gcp_creds',
            'description': '',
            'creationDate': '2021-06-21T10:53:44.475000Z',
            'credentialType': 'gcp'
        }
    )

.. testcode:: bigquery_output

    # get to make sure it exists
    credential_id = '5a8ac9ab07a57a0001be501f'
    cred = dr.Credential.get(credential_id)

    output_settings = {
        'type': 'bigquery',
        'dataset': 'dataset_name',
        'table': 'table_name',
        'bucket': 'bucket_in_gcs',
        'credential_id': cred.credential_id,
    }


**********************************
Copying a previously submitted job
**********************************

We provide a small utility function for submitting a job using parameters from a job previously submitted:
:meth:`BatchPredictionJob.score_from_existing <datarobot.models.BatchPredictionJob.score_from_existing>`.
The first parameter is the job id of another job.

.. testsetup:: score_from_existing

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/5dc5b1015e6e762a6241f9aa/'), status=200,
        json=batch_prediction_job_response,
    )

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/fromExisting/'), status=200,
        json=batch_prediction_job_response, adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200,
        json=batch_prediction_job_response,
    )

.. testcode:: score_from_existing

    import datarobot as dr

    previously_submitted_job_id = '5dc5b1015e6e762a6241f9aa'

    dr.BatchPredictionJob.score_from_existing(
        previously_submitted_job_id,
    )

*************************************
Scoring an in-memory Pandas DataFrame
*************************************

When working with DataFrames, we provide a method for scoring the data without first writing it to a
CSV file and subsequently reading the data back from a CSV file.

This will also take care of joining the computed predictions into the existing DataFrame.

Use the method :meth:`BatchPredictionJob.score_pandas <datarobot.models.BatchPredictionJob.score_pandas>`.
The first parameter is the deployment ID and then the DataFrame to score.

.. testsetup:: score_pandas

    import pandas as pd

    pd.read_csv = mock.MagicMock(return_value=pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}))

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200,
        json={'links': {'csvUpload': 'batchPredictions/random_id/'}},
        adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.PUT, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json={},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200,
        json=batch_prediction_job_response,
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/download/'), status=200, json={},
    )

.. testcode:: score_pandas

    import datarobot as dr
    import pandas as pd

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    df = pd.read_csv('testdata/titanic_predict.csv')

    job, df = dr.BatchPredictionJob.score_pandas(deployment_id, df)

The method returns a copy of the job status and the updated DataFrame with the predictions added.
So your DataFrame will now contain the following extra columns:

* Survived_1_PREDICTION
* Survived_0_PREDICTION
* Survived_PREDICTION
* THRESHOLD
* POSITIVE_CLASS
* prediction_status

.. code-block:: python

    print(df)
         PassengerId  Pclass                                          Name  ... Survived_PREDICTION  THRESHOLD  POSITIVE_CLASS
    0            892       3                              Kelly, Mr. James  ...                   0        0.5               1
    1            893       3              Wilkes, Mrs. James (Ellen Needs)  ...                   1        0.5               1
    2            894       2                     Myles, Mr. Thomas Francis  ...                   0        0.5               1
    3            895       3                              Wirz, Mr. Albert  ...                   0        0.5               1
    4            896       3  Hirvonen, Mrs. Alexander (Helga E Lindqvist)  ...                   1        0.5               1
    ..           ...     ...                                           ...  ...                 ...        ...             ...
    413         1305       3                            Spector, Mr. Woolf  ...                   0        0.5               1
    414         1306       1                  Oliva y Ocana, Dona. Fermina  ...                   0        0.5               1
    415         1307       3                  Saether, Mr. Simon Sivertsen  ...                   0        0.5               1
    416         1308       3                           Ware, Mr. Frederick  ...                   0        0.5               1
    417         1309       3                      Peter, Master. Michael J  ...                   1        0.5               1

    [418 rows x 16 columns]

If you don't want all of them or if you're not happy with the names of the added columns, they
can be modified using column remapping:

.. testsetup:: score_pandas_with_remapping

    import pandas as pd
    pd.read_csv = mock.MagicMock(return_value=pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}))

    responses.add(
        responses.POST, os.path.join(endpoint, 'batchPredictions/'), status=200,
        json={'links': {'csvUpload': 'batchPredictions/random_id/'}},
        adding_headers={'Location': 'http://localhost/api/v2/batchPredictions/random_id/'},
    )

    responses.add(
        responses.PUT, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200, json={},
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/'), status=200,
        json=batch_prediction_job_response,
    )

    responses.add(
        responses.GET, os.path.join(endpoint, 'batchPredictions/random_id/download/'), status=200, json={},
    )


.. testcode:: score_pandas_with_remapping

    import datarobot as dr
    import pandas as pd

    deployment_id = '5dc5b1015e6e762a6241f9aa'

    df = pd.read_csv('testdata/titanic_predict.csv')

    job, df = dr.BatchPredictionJob.score_pandas(
        deployment_id,
        df,
        column_names_remapping={
            'Survived_1_PREDICTION': None,       # discard column
            'Survived_0_PREDICTION': None,       # discard column
            'Survived_PREDICTION': 'predicted',  # rename column
            'THRESHOLD': None,                   # discard column
            'POSITIVE_CLASS': None,              # discard column
        },
    )

Any column mapped to ``None`` will be discarded. Any column mapped to a string will be renamed.
Any column not mentioned will be kept in the output untouched.
So your DataFrame will now contain the following extra columns:

* predicted
* prediction_status

Refer to the documentation for :meth:`BatchPredictionJob.score <datarobot.models.BatchPredictionJob.score>`
for the full range of available options.

.. _batch_prediction_job_definitions:

********************************
Batch Prediction Job Definitions
********************************

To submit a working Batch Prediction job, you must supply a variety of elements to the :func:`datarobot.models.BatchPredictionJob.score`
request payload depending on what type of prediction is required. Additionally, you must consider the type of intake
and output adapters used for a given job.

Every time a new Batch Prediction is created, the same amount of information must be stored somewhere outside of
DataRobot and re-submitted every time.

For example, a request could look like:

.. code-block:: python

    import datarobot as dr

    deployment_id = "5dc5b1015e6e762a6241f9aa"

    job = dr.BatchPredictionJob.score(
        deployment_id,
        intake_settings={
            "type": "s3",
            "url": "s3://bucket/container/file.csv",
            "credential_id": "5dc5b1015e6e762a6241f9bb"
        },
        output_settings={
            "type": "s3",
            "url": "s3://bucket/container/output.csv",
            "credential_id": "5dc5b1015e6e762a6241f9bb"
        },
    )

    job.wait_for_completion()

    with open("./predicted.csv", "wb") as f:
        job.download(f)

***************
Job Definitions
***************

If your use case requires the same, or close to the same, type of prediction to be done multiple times, you can choose to
create a *Job Definition* of the Batch Prediction job and store this inside DataRobot for future use.

The method for creating job definitions is identical to the existing :func:`datarobot.models.BatchPredictionJob.score` method,
except for the addition of a ``enabled``, ``name`` and ``schedule`` parameter: :func:`datarobot.models.BatchPredictionJobDefinition.create`

.. code-block:: python

    >>> import datarobot as dr
    >>> job_spec = {
    ...    "num_concurrent": 4,
    ...    "deployment_id": "5dc5b1015e6e762a6241f9aa",
    ...    "intake_settings": {
    ...        "url": "s3://foobar/123",
    ...        "type": "s3",
    ...        "format": "csv",
    ...        "credential_id": "5dc5b1015e6e762a6241f9bb"
    ...    },
    ...    "output_settings": {
    ...        "url": "s3://foobar/123",
    ...        "type": "s3",
    ...        "format": "csv",
    ...        "credential_id": "5dc5b1015e6e762a6241f9bb"
    ...    },
    ...}
    >>> definition = BatchPredictionJobDefinition.create(
    ...    enabled=False,
    ...    batch_prediction_job=job_spec,
    ...    name="some_definition_name",
    ...    schedule=None
    ... )
    >>> definition
    BatchPredictionJobDefinition(foobar)

.. note:: The ``name`` parameter must be unique across your organization. If you attempt to create multiple definitions
    with the same name, the request will fail. If you wish to free up a name, you must first :func:`datarobot.models.BatchPredictionJobDefinition.delete`
    the existing definition before creating this one. Alternatively you can just :func:`datarobot.models.BatchPredictionJobDefinition.update`
    the existing definition with a new name.

**************************
Executing a job definition
**************************

Manual job execution
--------------------

To submit a stored job definition for scoring, you can either do so on a scheduled basis, described
below, or manually submit the definition ID using :func:`datarobot.models.BatchPredictionJobDefinition.run_once`,
as such:

.. code-block:: python

    >>> import datarobot as dr
    >>> definition = dr.BatchPredictionJobDefinition.get("5dc5b1015e6e762a6241f9aa")
    >>> job = definition.run_once()
    >>> job.wait_for_completion()

Scheduled job execution
-----------------------

A Scheduled Batch Prediction job works just like a regular Batch Prediction job, except DataRobot handles the execution
of the job.

In order to schedule the execution of a Batch Prediction job, a definition must first be created, using
:func:`datarobot.models.BatchPredictionJobDefinition.create`, or updated, using
:func:`datarobot.models.BatchPredictionJobDefinition.update`, where ``enabled`` is set to ``True`` and a ``schedule``
payload is provided.

Alternatively, you can use a short-hand version with :func:`datarobot.models.BatchPredictionJobDefinition.run_on_schedule`
as such:

.. code-block:: python

    >>> import datarobot as dr
    >>> schedule = {
    ...    "day_of_week": [
    ...        1
    ...    ],
    ...    "month": [
    ...        "*"
    ...    ],
    ...    "hour": [
    ...        16
    ...    ],
    ...    "minute": [
    ...        0
    ...    ],
    ...    "day_of_month": [
    ...        1
    ...    ]
    ...}
    >>> definition = dr.BatchPredictionJob.get("5dc5b1015e6e762a6241f9aa")
    >>> job = definition.run_on_schedule(schedule)

If the created job was not enabled previously, this method will also enable it.

************************
The ``Schedule`` payload
************************

The ``schedule`` payload defines at what intervals the job should run, which can be combined in various ways to construct
complex scheduling terms if needed. In all of the elements in the objects, you can supply either an asterisk ``["*"]``
denoting "every" time denomination or an array of integers (e.g. ``[1, 2, 3]``) to define a specific interval.

..  list-table:: The ``schedule`` payload elements
    :widths: 10, 10, 10, 5
    :header-rows: 1
    :class: tight-table

    * - Key
      - Possible values
      - Example
      - Description
    * - minute
      - ``["*"]`` or ``[0 ... 59]``
      - ``[15, 30, 45]``
      - The job will run at these minute values for every hour of the day.
    * - hour
      - ``["*"]`` or ``[0 ... 23]``
      - ``[12,23]``
      - The hour(s) of the day that the job will run.
    * - month
      - ``["*"]`` or ``[1 ... 12]``
      - ``["jan"]``
      - Strings, either 3-letter abbreviations or the full name of the month, can be used interchangeably (e.g., "jan" or "october").

        Months that are not compatible with ``day_of_month`` are ignored, for example ``{"day_of_month": [31], "month":["feb"]}``.
    * - day_of_week
      - ``["*"]`` or ``[0 ... 6]`` where (Sunday=0)
      - ``["sun"]``
      - The day(s) of the week that the job will run. Strings, either 3-letter abbreviations or the full name of the day, can be used interchangeably (e.g., "sunday", "Sunday", "sun", or "Sun", all map to ``[0]``).

        **NOTE:** This field is additive with ``day_of_month``, meaning the job will run both on the date specified by ``day_of_month`` and the day defined in this field.
    * - day_of_month
      - ``["*"]`` or ``[1 ... 31]``
      - ``[1, 25]``
      - The date(s) of the month that the job will run. Allowed values are either ``[1 ... 31]`` or ``["*"]`` for all days of the month.

        **NOTE:** This field is additive with ``day_of_week``, meaning the job will run both on the date(s) defined in this field and the day specified
        by ``day_of_week`` (for example, dates 1st, 2nd, 3rd, plus every Tuesday). If ``day_of_month`` is set to ``["*"]`` and ``day_of_week`` is defined,
        the scheduler will trigger on every day of  the month that matches ``day_of_week`` (for example, Tuesday the 2nd, 9th, 16th, 23rd, 30th).

        Invalid dates such as February 31st are ignored.

Disabling a scheduled job
-------------------------

Job definitions are only be executed by the scheduler if ``enabled`` is set to ``True``. If you have a job definition
that was previously running as a scheduled job, but should now be stopped, simply
:func:`datarobot.models.BatchPredictionJobDefinition.delete` to remove it completely, or :func:`datarobot.models.BatchPredictionJobDefinition.update`
it with ``enabled=False`` if you want to keep the definition, but stop the scheduled job from executing at intervals.
If a job is currently running, this will finish execution regardless.

.. code-block:: python

    >>> import datarobot as dr
    >>> definition = dr.BatchPredictionJobDefinition.get("5dc5b1015e6e762a6241f9aa")
    >>> definition.delete()
