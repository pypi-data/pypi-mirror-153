.. _reason_codes:

=======================
Prediction Explanations
=======================

To compute prediction explanations you need to have :ref:`feature impact<feature_impact-label>`
computed for a model, and predictions for an uploaded dataset
computed with a selected model.

Computing prediction explanations is a resource-intensive task, but you can configure it with
maximum explanations per row and prediction value thresholds to speed up the process.

Quick Reference
***************

.. code-block:: python

    import datarobot as dr
    # Get project
    my_projects = dr.Project.list()
    project = my_projects[0]
    # Get model
    models = project.get_models()
    model = models[0]
    # Compute feature impact
    feature_impacts = model.get_or_request_feature_impact()
    # Upload dataset
    dataset = project.upload_dataset('./data_to_predict.csv')
    # Compute predictions
    predict_job = model.request_predictions(dataset.id)
    predict_job.wait_for_completion()
    # Initialize prediction explanations
    pei_job = dr.PredictionExplanationsInitialization.create(project.id, model.id)
    pei_job.wait_for_completion()
    # Compute prediction explanations with default parameters
    pe_job = dr.PredictionExplanations.create(project.id, model.id, dataset.id)
    pe = pe_job.get_result_when_complete()
    # Iterate through predictions with prediction explanations
    for row in pe.get_rows():
        print(row.prediction)
        print(row.prediction_explanations)
    # download to a CSV file
    pe.download_to_csv('prediction_explanations.csv')

List Prediction Explanations
****************************
You can use the ``PredictionExplanations.list()`` method to return a list of prediction
explanations computed for a project's models:

.. code-block:: python

    import datarobot as dr
    prediction_explanations = dr.PredictionExplanations.list('58591727100d2b57196701b3')
    print(prediction_explanations)
    >>> [PredictionExplanations(id=585967e7100d2b6afc93b13b,
                     project_id=58591727100d2b57196701b3,
                     model_id=585932c5100d2b7c298b8acf),
         PredictionExplanations(id=58596bc2100d2b639329eae4,
                     project_id=58591727100d2b57196701b3,
                     model_id=585932c5100d2b7c298b8ac5),
         PredictionExplanations(id=58763db4100d2b66759cc187,
                     project_id=58591727100d2b57196701b3,
                     model_id=585932c5100d2b7c298b8ac5),
         ...]
    pe = prediction_explanations[0]

    pe.project_id
    >>> u'58591727100d2b57196701b3'
    pe.model_id
    >>> u'585932c5100d2b7c298b8acf'

You can pass following parameters to filter the result:

* ``model_id`` -- str, used to filter returned prediction explanations by model_id.
* ``limit`` -- int, limit for number of items returned, default: no limit.
* ``offset`` -- int, number of items to skip, default: 0.

**List Prediction Explanations Example:**

.. code-block:: python

    project_id = '58591727100d2b57196701b3'
    model_id = '585932c5100d2b7c298b8acf'
    dr.PredictionExplanations.list(project_id, model_id=model_id, limit=20, offset=100)


Initialize Prediction Explanations
**********************************
In order to compute prediction explanations you have to initialize it for a particular model.

.. code-block:: python

    dr.PredictionExplanationsInitialization.create(project_id, model_id)

Compute Prediction Explanations
*******************************
If all prerequisites are in place, you can compute prediction explanations in the following way:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    dataset_id = '5506fcd98bd88a8142b725c8'
    pe_job = dr.PredictionExplanations.create(project_id, model_id, dataset_id,
                                   max_explanations=2, threshold_low=0.2, threshold_high=0.8)
    pe = pe_job.get_result_when_complete()

Where:

* ``max_explanations`` are the maximum number of prediction explanations to compute for each row.
* ``threshold_low`` and ``threshold_high`` are thresholds for the value of the prediction of the
  row. Prediction explanations will be computed for a row if the row's prediction value is higher
  than ``threshold_high`` or lower than ``threshold_low``. If no thresholds are specified,
  prediction explanations will be computed for all rows.

Retrieving Prediction Explanations
**********************************
You have three options for retrieving prediction explanations.

.. note:: ``PredictionExplanations.get_all_as_dataframe()`` and
          ``PredictionExplanations.download_to_csv()`` reformat
          prediction explanations to match the schema of CSV file downloaded from UI (RowId,
          Prediction, Explanation 1 Strength, Explanation 1 Feature, Explanation 1 Value, ...,
          Explanation N Strength, Explanation N Feature, Explanation N Value)

Get prediction explanations rows one by one as
:class:`PredictionExplanationsRow <datarobot.models.prediction_explanations.PredictionExplanationsRow>`
objects:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    prediction_explanations_id = '5506fcd98bd88f1641a720a3'
    pe = dr.PredictionExplanations.get(project_id, prediction_explanations_id)
    for row in pe.get_rows():
        print(row.prediction_explanations)

Get all rows as ``pandas.DataFrame``:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    prediction_explanations_id = '5506fcd98bd88f1641a720a3'
    pe = dr.PredictionExplanations.get(project_id, prediction_explanations_id)
    prediction_explanations_df = pe.get_all_as_dataframe()

Download all rows to a file as CSV document:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    prediction_explanations_id = '5506fcd98bd88f1641a720a3'
    pe = dr.PredictionExplanations.get(project_id, prediction_explanations_id)
    pe.download_to_csv('prediction_explanations.csv')

Adjusted Predictions In Prediction Explanations
***********************************************
In some projects such as insurance projects, the prediction adjusted by exposure is more useful
compared with raw prediction. For example, the raw prediction (e.g. claim counts) is divided by
exposure (e.g. time) in the project with exposure column. The adjusted prediction provides insights
with regard to the predicted claim counts per unit of time. To include that information, set
`exclude_adjusted_predictions` to False in correspondent method calls.

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    prediction_explanations_id = '5506fcd98bd88f1641a720a3'
    pe = dr.PredictionExplanations.get(project_id, prediction_explanations_id)
    pe.download_to_csv('prediction_explanations.csv', exclude_adjusted_predictions=False)
    prediction_explanations_df = pe.get_all_as_dataframe(exclude_adjusted_predictions=False)

Multiclass Prediction Explanation Modes
***************************************
When calculating prediction explanations for the multiclass model you need to specify which
classes should be explained in each row. By default we only explain the predicted class but
it can be set with the mode parameter of :meth:`PredictionExplanations.create <datarobot.PredictionExplanations.create>`

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    dataset_id = '5506fcd98bd88a8142b725c8'
    # Explain predicted and second-best class results in each row
    pe_job = dr.PredictionExplanations.create(project_id, model_id, dataset_id,
                                              mode=dr.models.TopPredictionsMode(2))
    pe = pe_job.get_result_when_complete()
    # Explain results for classes "setosa" and "versicolor" in each row
    pe_job = dr.PredictionExplanations.create(project_id, model_id, dataset_id,
                                              mode=dr.models.ClassListMode(["setosa", "versicolor"]))
    pe = pe_job.get_result_when_complete()


.. _shap_matrix:

SHAP based prediction explanations
**********************************
You can request SHAP based prediction explanations using previously uploaded scoring dataset for
models that support SHAP. Unlike for XEMP prediction explanations you do not need to have
:ref:`feature impact<feature_impact-label>` computed for a model, and predictions for an
uploaded dataset.

See :meth:`datarobot.models.ShapMatrix.create` reference for a description of the types of
parameters that can be passed in.

.. code-block:: python

    import datarobot as dr
    project_id = '5ea6d3354cfad121cf33a5e1'
    model_id = '5ea6d38b4cfad121cf33a60d'
    project = dr.Project.get(project_id)
    model = dr.Model.get(project=project_id, model_id=model_id)
    # check if model supports SHAP
    model_capabilities = model.get_supported_capabilities()
    print(model_capabilities.get('supportsShap'))
    >>> True
    # upload dataset to generate prediction explanations
    dataset_from_path = project.upload_dataset('./data_to_predict.csv')

    shap_matrix_job = ShapMatrix.create(project_id=project_id, model_id=model_id, dataset_id=dataset_from_path.id)
    shap_matrix_job
    >>> Job(shapMatrix, status=inprogress)
    # wait for job to finish
    shap_matrix = shap_matrix_job.get_result_when_complete()
    shap_matrix
    >>> ShapMatrix(id='5ea84b624cfad1361c53f65d', project_id='5ea6d3354cfad121cf33a5e1', model_id='5ea6d38b4cfad121cf33a60d', dataset_id='5ea84b464cfad1361c53f655')

    # retrieve SHAP matrix as pandas.DataFrame
    df = shap_matrix.get_as_dataframe()

    # list as available SHAP matrices for a project
    shap_matrices = dr.ShapMatrix.list(project_id)
    shap_matrices
    >>> [ShapMatrix(id='5ea84b624cfad1361c53f65d', project_id='5ea6d3354cfad121cf33a5e1', model_id='5ea6d38b4cfad121cf33a60d', dataset_id='5ea84b464cfad1361c53f655')]

    shap_matrix = shap_matrices[0]
    # retrieve SHAP matrix as pandas.DataFrame
    df = shap_matrix.get_as_dataframe()
