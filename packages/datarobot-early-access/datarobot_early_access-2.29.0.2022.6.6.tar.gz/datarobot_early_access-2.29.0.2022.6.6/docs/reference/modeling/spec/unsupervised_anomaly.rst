.. _unsupervised_anomaly:

#########################################
Unsupervised Projects (Anomaly Detection)
#########################################

When the data is not labelled and the problem can be interpreted either as anomaly detection or time
series anomaly detection, projects in unsupervised mode become useful.

Creating Unsupervised Projects
==============================

In order to create an unsupervised project set ``unsupervised_mode`` to ``True`` when setting the target.

.. code-block:: python

    >>> import datarobot as dr
    >>> project = Project.create('dataset.csv', project_name='unsupervised')
    >>> project.set_target(unsupervised_mode=True)

Creating Time Series Unsupervised Projects
==========================================

To create a time series unsupervised project pass  ``unsupervised_mode=True`` to
datetime partitioning creation and to project aim. The forecast window will be automatically set to nowcasting,
i.e. forecast distance zero (FW = 0, 0).

.. code-block:: python

    >>> import datarobot as dr
    >>> project = Project.create('dataset.csv', project_name='unsupervised')
    >>> spec = DatetimePartitioningSpecification('date',
    ...    use_time_series=True, unsupervised_mode=True,
    ...    feature_derivation_window_start=-4, feature_derivation_window_end=0)

    # this step is optional - preview the default partitioning which will be applied
    >>> partitioning_preview = DatetimePartitioning.generate(project.id, spec)
    >>> full_spec = partitioning_preview.to_specification()
    >>> project.set_target(unsupervised_mode=True, partitioning_method=full_spec)

Unsupervised Project Metrics
============================

In unsupervised projects, metrics are not used for the model optimization. Instead, they are used for the
purpose of model ranking. There are two available unsupervised metrics -- Synthetic AUC and
synthetic LogLoss -- both of which are calculated on artificially-labelled validation samples.


.. _anomaly_over_time_plots:

Estimating Accuracy of Unsupervised Anomaly Detection Datetime Partitioned Models
=================================================================================

For datatime partitioned unsupervised model you can retrieve the Anomaly over Time plot. To do so use
:meth:`DatetimeModel.get_anomaly_over_time_plot<datarobot.models.DatetimeModel.get_anomaly_over_time_plot>`.
You can also retrieve the detailed metadata using :meth:`DatetimeModel.get_anomaly_over_time_plots_metadata<datarobot.models.DatetimeModel.get_anomaly_over_time_plots_metadata>`,
and the preview plot using :meth:`DatetimeModel.get_anomaly_over_time_plot_preview<datarobot.models.DatetimeModel.get_anomaly_over_time_plot_preview>`.

.. _anomaly_assessment:


Explaining Unsupervised Time Series Anomaly Detection Models Predictions
========================================================================

Within a timeseries unsupervised project for models supporting calculation of Shapley values,
Anomaly Assessment insight can be computed to explain anomalies.

Example 1: computation, retrieval and deletion of the anomaly assessment insight.

.. code-block:: python

    >>> import datarobot as dr
    # Initialize Anomaly Assessment for the backtest 0, training subset and series "series1"
    >>> model = dr.DatetimeModel.get(project_id, model_id)
    >>> anomaly_assessment_record = model.initialize_anomaly_assessment(0, "training", "series1")
    # Get available Anomaly Assessment for the project and model
    >>> all_records = model.get_anomaly_assessment_records()
    # Get most recent anomaly assessment explanations
    >>> all_records[0].get_latest_explanations()
    # Get anomaly assessment explanations in the range
    >>> all_records[0].get_explanations(start_date="2020-01-01", points_count=500)
     # Get anomaly assessment predictions preview
    >>> all_records[0].get_predictions_preview()
    # Delete record
    >>> all_records[0].delete()

Example 2: Find explanations for the anomalous regions (regions with maximum anomaly score >=0.6)
for the multiseries project. Leave only explanations for the rows with anomaly score >= 0.5.

.. code-block:: python

    >>> def collect_explanations(model, backtest, source, series_ids):
    ... for series in series_ids:
    ...     try:
    ...         model.initialize_anomaly_assessment(backtest, source, series)
    ...      except ClientError:
    ...         # when insight was already computed
    ...         pass
    ... records_for_series = model.get_anomaly_assessment_records(source=source, backtest=backtest, with_data_only=True, limit=0)
    ... result = {}
    ... for record in records_for_series:
    ...     preview = record.get_predictions_preview()
    ...     anomalous_regions = preview.find_anomalous_regions(max_prediction_threshold=0.6)
    ...     if anomalous_regions:
    ...         result[record.series_id] = record.get_explanations_data_in_regions(anomalous_regions, prediction_threshold=0.5)
    ... return result
    >>> import datarobot as dr
    >>> model = dr.DatetimeModel.get(project_id, model_id)
    >>> collect_explanations(model, 0, "validation", series_ids)


.. _unsupervised_external_dataset:

Assessing Unsupervised Anomaly Detection Models on External Test Set
====================================================================

In unsupervised projects, if there is some labelled data, it may be used to assess anomaly detection
models by checking computed classification metrics such as AUC and LogLoss, etc. and insights such as ROC and Lift.
Such data is uploaded as a prediction dataset with a specified actual value column name, and, if it
is a time series project, a prediction date range. The actual value column can contain only zeros and ones or True/False,
and it should not have been seen during training time.

Requesting External Scores and Insights (Time Series)
=====================================================

There are two ways to specify an actual value column and compute scores and insights:

1. Upload a prediction dataset, specifying ``predictions_start_date``, ``predictions_end_date``,
and ``actual_value_column``, and request predictions on that dataset using a specific model.

.. code-block:: python

    >>> import datarobot as dr
    # Upload dataset
    >>> project = dr.Project(project_id)
    >>> dataset = project.upload_dataset(
    ...    './data_to_predict.csv',
    ...    predictions_start_date=datetime(2000, 1, 1),
    ...    predictions_end_date=datetime(2015, 1, 1),
    ...    actual_value_column='actuals'
    ...    )
    # run prediction job which also will calculate requested scores and insights.
    >>> predict_job = model.request_predictions(dataset.id)
    # prediction output will have column with actuals
    >>> result = pred_job.get_result_when_complete()



2. Upload a prediction dataset without specifying any options, and request predictions for a specific model with
``predictions_start_date``, ``predictions_end_date``, and ``actual_value_column`` specified.
Note, these settings cannot be changed for the dataset after making predictions.


.. code-block:: python

    >>> import datarobot as dr
    # Upload dataset
    >>> project = dr.Project(project_id)
    >>> dataset = project.upload_dataset('./data_to_predict.csv')
    # Check which columns are candidates for actual value columns
    >>> dataset.detected_actual_value_columns
    [{'missing_count': 25, 'name': 'label_column'}]

    # run prediction job which also will calculate requested scores and insights.
    >>> predict_job = model.request_predictions(
    ...    dataset.id,
    ...    predictions_start_date=datetime(2000, 1, 1),
    ...    predictions_end_date=datetime(2015, 1, 1),
    ...    actual_value_column='label_column'
    ...  )
    >>> result = pred_job.get_result_when_complete()


Requesting External Scores and Insights for AutoML models
=========================================================

To compute scores and insights on an external dataset for unsupervised AutoML models (Non Time series)

Upload a prediction dataset that contains label column(s), request compute external test on one
of ``PredictionDataset.detected_actual_value_columns``

.. code-block:: python

    import datarobot as dr
    # Upload dataset
    project = dr.Project(project_id)
    dataset = project.upload_dataset('./test_set.csv')
    dataset.detected_actual_value_columns
    >>>['label_column_1', 'label_column_2']
    # request external test to compute metric scores and insights on dataset
    external_test_job = model.request_external_test(dataset.id, actual_value_column='label_column_1')
    # once job is complete, scores and insights are ready for retrieving
    external_test_job.wait_for_completion()

Retrieving External Scores and Insights
=======================================

Upon completion of prediction, external scores and insights can be retrieved to assess model
performance. For unsupervised projects Lift Chart and ROC Curve are computed.
If the dataset is too small insights will not be computed. If the actual value column contained
only one class, the ROC Curve will not be computed. Information about the dataset can be retrieved
using ``PredictionDataset.get``.

.. code-block:: python

     >>> import datarobot as dr
    # Check which columns are candidates for actual value columns
     >>> scores_list = ExternalScores.list(project_id)
     >>> scores = ExternalScores.get(project_id, dataset_id=dataset_id, model_id=model_id)
     >>> lift_list = ExternalLiftChart.list(project_id, model_id)
     >>> roc = ExternalRocCurve.get(project_id, model, dataset_id)
    # check dataset warnings, need to be called after predictions are computed.
     >>> dataset = PredictionDataset.get(project_id, dataset_id)
     >>> dataset.data_quality_warnings
    {'single_class_actual_value_column': True,
    'insufficient_rows_for_evaluating_models': False,
    'has_kia_missing_values_in_forecast_window': False}
