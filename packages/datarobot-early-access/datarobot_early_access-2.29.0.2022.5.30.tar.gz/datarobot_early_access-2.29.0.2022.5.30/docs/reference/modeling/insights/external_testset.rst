.. _external_testset:

#################
External Testset
#################

Testing with external datasets allows better evaluation model performance, you can compute metric
scores and insights on external test dataset to ensure consistent performance prior to deployment.


.. note:: Not available for Time series models.

Requesting External Scores and Insights
=======================================

To compute scores and insights on a dataset

Upload a prediction dataset that contains the target column ``PredictionDataset.contains_target_values == True``.
Dataset should be in the same structure as the original project.

.. code-block:: python

    import datarobot as dr
    # Upload dataset
    project = dr.Project(project_id)
    dataset = project.upload_dataset('./test_set.csv')
    dataset.contains_target_values
    >>>True
    # request external test to compute metric scores and insights on dataset
    # select model using project.get_models()
    external_test_job = model.request_external_test(dataset.id)
    # once job is complete, scores and insights are ready for retrieving
    external_test_job.wait_for_completion()


Retrieving External Metric Scores and Insights
==============================================
After completion of external test job, metric scores and insights for external testsets will be ready.

.. note::
   Please check ``PredictionDataset.data_quality_warnings`` for dataset warnings.
   Insights are not avaiable if dataset is too small (less than 10 rows).
   ROC curve cannot be calculated if dataset has only one class in target column

Retrieving External Metric Scores
=================================

.. code-block:: python

    import datarobot as dr
    # retrieving list of external metric scores on multiple datasets
    metric_scores_list = dr.ExternalScores.list(project_id, model_id)
    # retrieving external metric scores on one dataset
    metric_scores = dr.ExternalScores.get(project_id, model_id, dataset_id)

Retrieving External Lift Chart
==============================

.. code-block:: python

    import datarobot as dr
    # retrieving list of lift charts on multiple datasets
    lift_list = dr.ExternalLiftChart.list(project_id, model_id)
    # retrieving one lift chart for dataset
    lift = dr.ExternalLiftChart.get(project_id, model_id, dataset_id)


Retrieving External Multiclass Lift Chart
==========================================
Lift chart for Multiclass models only

.. code-block:: python

    import datarobot as dr
    # retrieving list of lift charts on multiple datasets
    lift_list = ExternalMulticlassLiftChart.list(project_id, model_id)
    # retrieving one lift chart for dataset and a target class
    lift = ExternalMulticlassLiftChart.get(project_id, model_id, dataset_id, target_class)


Retrieving External ROC Curve
=============================
Avaiable for Binary classification models only

.. code-block:: python

    import datarobot as dr
    # retrieving list of roc curves on multiple datasets
    roc_list = ExternalRocCurve.list(project_id, model_id)
    # retrieving one ROC curve for dataset
    roc = ExternalRocCurve.get(project_id, model_id, dataset_id)

Retrieving Multiclass Confusion Matrix
======================================
Avaiable for Multiclass classification models only

.. code-block:: python

    import datarobot as dr
    # retrieving list of confusion charts on multiple datasets
    confusion_list = ExternalConfusionChart.list(project_id, model_id)
    # retrieving one confusion chart for dataset
    confusion = ExternalConfusionChart.get(project_id, model_id, dataset_id)



Retrieving Residuals Chart
==========================
Aviavble for Regression models only

.. code-block:: python

    import datarobot as dr
    # retrieving list of residuals charts on multiple datasets
    residuals_list = ExternalResidualsChart.list(project_id, model_id)
    # retrieving one residuals chart for dataset
    residuals = ExternalResidualsChart.get(project_id, model_id, dataset_id)


