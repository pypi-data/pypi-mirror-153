.. _predictions:

###########
Predictions
###########

Predictions generation is an asynchronous process. This means that when starting
predictions with ``Model.request_predictions`` you will receive back a PredictJob for tracking
the process responsible for fulfilling your request.

With this object you can get info about the predictions generation process before it
has finished and be rerouted to the predictions themselves when the
process is finished. For this you should use the :ref:`PredictJob <predict_job_api>` class.

Starting predictions generation
*******************************
Before actually requesting predictions, you should upload the dataset you wish to predict via
``Project.upload_dataset``.  Previously uploaded datasets can be seen under ``Project.get_datasets``.
When uploading the dataset you can provide the path to a local file, a file object, raw file content,
a ``pandas.DataFrame`` object, or the url to a publicly available dataset.


To start predicting on new data using a finished model use ``Model.request_predictions``.
It will create a new predictions generation process and return a PredictJob object tracking this process.
With it, you can monitor an existing PredictJob and retrieve generated predictions when the corresponding
PredictJob is finished.

.. code-block:: python

    import datarobot as dr

    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    project = dr.Project.get(project_id)
    model = dr.Model.get(project=project_id,
                         model_id=model_id)

    # Using path to local file to generate predictions
    dataset_from_path = project.upload_dataset('./data_to_predict.csv')

    # Using file object to generate predictions
    with open('./data_to_predict.csv') as data_to_predict:
        dataset_from_file = project.upload_dataset(data_to_predict)

    predict_job_1 = model.request_predictions(dataset_from_path.id)
    predict_job_2 = model.request_predictions(dataset_from_file.id)


Listing Predictions
*******************
You can use the ``Predictions.list()`` method to return a list of predictions generated on a project.

.. code-block:: python

    import datarobot as dr
    predictions = dr.Predictions.list('58591727100d2b57196701b3')

    print(predictions)
    >>>[Predictions(prediction_id='5b6b163eca36c0108fc5d411',
                    project_id='5b61bd68ca36c04aed8aab7f',
                    model_id='5b61bd7aca36c05744846630',
                    dataset_id='5b6b1632ca36c03b5875e6a0'),
        Predictions(prediction_id='5b6b2315ca36c0108fc5d41b',
                    project_id='5b61bd68ca36c04aed8aab7f',
                    model_id='5b61bd7aca36c0574484662e',
                    dataset_id='5b6b1632ca36c03b5875e6a0'),
        Predictions(prediction_id='5b6b23b7ca36c0108fc5d422',
                    project_id='5b61bd68ca36c04aed8aab7f',
                    model_id='5b61bd7aca36c0574484662e',
                    dataset_id='55b6b1632ca36c03b5875e6a0')
        ]


You can pass following parameters to filter the result:

* ``model_id`` -- str, used to filter returned predictions by model_id.
* ``dataset_id`` -- str, used to filter returned predictions by dataset_id.


Get an existing PredictJob
**************************

To retrieve an existing PredictJob use the ``PredictJob.get`` method. This will give you
a PredictJob matching the latest status of the job if it has not completed.

If predictions have finished building, ``PredictJob.get`` will raise a ``PendingJobFinished``
exception.


.. code-block:: python

    import time

    import datarobot as dr

    predict_job = dr.PredictJob.get(project_id=project_id,
                                    predict_job_id=predict_job_id)
    predict_job.status
    >>> 'queue'

    # wait for generation of predictions (in a very inefficient way)
    time.sleep(10 * 60)
    predict_job = dr.PredictJob.get(project_id=project_id,
                                    predict_job_id=predict_job_id)
    >>> dr.errors.PendingJobFinished

    # now the predictions are finished
    predictions = dr.PredictJob.get_predictions(project_id=project.id,
                                                predict_job_id=predict_job_id)

Get generated predictions
*************************

After predictions are generated, you can use ``PredictJob.get_predictions``
to get newly generated predictions.

If predictions have not yet been finished, it will raise a ``JobNotFinished`` exception.

.. code-block:: python

    import datarobot as dr

    predictions = dr.PredictJob.get_predictions(project_id=project.id,
                                                predict_job_id=predict_job_id)

Wait for and Retrieve results
*****************************
If you just want to get generated predictions from a PredictJob, you
can use the ``PredictJob.get_result_when_complete`` function.
It will poll the status of the predictions generation process until it has finished, and
then will return predictions.

.. code-block:: python

    dataset = project.get_datasets()[0]
    predict_job = model.request_predictions(dataset.id)
    predictions = predict_job.get_result_when_complete()


Get previously generated predictions
************************************
If you don't have a ``Model.predict_job`` on hand, there are two more ways to retrieve predictions from the
``Predictions`` interface:

1. Get all prediction rows as a ``pandas.DataFrame`` object:

.. code-block:: python

    import datarobot as dr

    preds = dr.Predictions.get("5b61bd68ca36c04aed8aab7f", prediction_id="5b6b163eca36c0108fc5d411")
    df = preds.get_all_as_dataframe()
    df_with_serializer = preds.get_all_as_dataframe(serializer='csv')

2. Download all prediction rows to a file as a CSV document:

.. code-block:: python

    import datarobot as dr

    preds = dr.Predictions.get("5b61bd68ca36c04aed8aab7f", prediction_id="5b6b163eca36c0108fc5d411")
    preds.download_to_csv('predictions.csv')

    preds.download_to_csv('predictions_with_serializer.csv', serializer='csv')

.. _training_predictions:

Training predictions
####################
The training predictions interface allows computing and retrieving out-of-sample predictions for a model
using the original project dataset. The predictions can be computed for all the rows, or restricted to validation
or holdout data. As the predictions generated will be out-of-sample, they can be expected to have different
results than if the project dataset were reuploaded as a prediction dataset.

Quick reference
***************
Training predictions generation is an asynchronous process. This means that when starting
predictions with :py:meth:`datarobot.models.Model.request_training_predictions` you will receive back a
:py:class:`datarobot.models.TrainingPredictionsJob` for tracking the process responsible for fulfilling your request.
Actual predictions may be obtained with the help of a
:py:class:`datarobot.models.training_predictions.TrainingPredictions` object returned as the result of
the training predictions job.
There are three ways to retrieve them:

1. Iterate prediction rows one by one as named tuples:

.. code-block:: python

    import datarobot as dr

    # Calculate new training predictions on all dataset
    training_predictions_job = model.request_training_predictions(dr.enums.DATA_SUBSET.ALL)
    training_predictions = training_predictions_job.get_result_when_complete()

    # Fetch rows from API and print them
    for prediction in training_predictions.iterate_rows(batch_size=250):
        print(prediction.row_id, prediction.prediction)

2. Get all prediction rows as a ``pandas.DataFrame`` object:

.. code-block:: python

    import datarobot from dr

    # Calculate new training predictions on holdout partition of dataset
    training_predictions_job = model.request_training_predictions(dr.enums.DATA_SUBSET.HOLDOUT)
    training_predictions = training_predictions_job.get_result_when_complete()

    # Fetch training predictions as data frame
    dataframe = training_predictions.get_all_as_dataframe()

3. Download all prediction rows to a file as a CSV document:

.. code-block:: python

    import datarobot from dr

    # Calculate new training predictions on all dataset
    training_predictions_job = model.request_training_predictions(dr.enums.DATA_SUBSET.ALL)
    training_predictions = training_predictions_job.get_result_when_complete()

    # Fetch training predictions and save them to file
    training_predictions.download_to_csv('my-training-predictions.csv')
