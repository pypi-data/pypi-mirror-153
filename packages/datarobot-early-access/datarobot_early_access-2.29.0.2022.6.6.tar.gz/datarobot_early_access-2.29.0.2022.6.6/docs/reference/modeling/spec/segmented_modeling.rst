.. _segmented_modeling:

###########################
Segmented Modeling Projects
###########################

Many :ref:`time series<time_series>` multiseries projects introduce complex forecasting use cases that require using different models for subsets of series (i.e., sales of groceries and clothing can be very different). Within the segmented modeling framework, DataRobot runs multiple time series projects (one per segment / group of series), selects the best models for each segment, and then combines those models to make predictions. 

Segment
*******
A segment is a group of series in a multiseries project. For example, given ``store`` and ``country`` columns in dataset, you can use the former as the series identifier and the latter  as the segment identifier. For the best results, group series with similar patterns into segments (instead of random selection). 

Segmentation Task
*****************
A segmentation task is an entity that defines how input dataset is partitioned. Currently only user-defined segmentation is supported. That is, the dataset must have a separate column that is used to identify segment (and the user must select it). All records within a series must have the same segment identifier.

Combined Model
**************
A combined model in a segmented modeling project can be thought of as a meta-model made of references to the best model within each segment. While being quite different from a standard DataRobot model in its creation, its use is very much the same after the model is complete (for example, deploying or making predictions).

The following examples illustrate how to set up, run, and manage a segmented modeling project using the Python public API client. For details please refer to :ref:`Segmented Modeling API Reference<segmented_modeling_api>`.

Starting a Segmentation Project with a User Defined Segment ID
==============================================================
`Time series` modeling must be enabled for your account to run segmented modeling projects.

Use the standard method to create a DataRobot project:

.. code-block:: python

    from datarobot import DatetimePartitioningSpecification
    from datarobot import enums
    from datarobot import Project
    from datarobot import SegmentationTask

    project_name = "Segmentation Demo with Segmentation ID"
    project_dataset = "multiseries_segmentation.csv"
    project = Project.create(project_dataset, project_name=project_name)

    datetime_partition_column = "timestamp"
    multiseries_id_column = "series_id"
    user_defined_segment_id_column = "物类segment_id"
    target = "target"

Create a simple datetime specification for a time series project:

.. code-block:: python

    spec = DatetimePartitioningSpecification(
        use_time_series=True,
        datetime_partition_column=datetime_partition_column,
        multiseries_id_columns=[multiseries_id_column],
    )

Create a segmentation task for the project:

.. code-block:: python

    segmentation_task_results = SegmentationTask.create(
        project_id=project.id,
        target=target,
        use_time_series=True,
        datetime_partition_column=datetime_partition_column,
        multiseries_id_columns=[multiseries_id_column],
        user_defined_segment_id_columns=[user_defined_segment_id_column],
    )
    segmentation_task = segmentation_task_results["completedJobs"][0]

Start a segmented project by passing the `segmentation_task_id` argument:

.. code-block:: python

    project.set_target(
        target=target,
        partitioning_method=spec,
        mode=enums.AUTOPILOT_MODE.QUICK,
        worker_count=-1,
        segmentation_task_id=segmentation_task.id,
    )
    
Working with Combined Models
============================

Retrieve Combined Models:

.. code-block:: python

    from datarobot import Project, CombinedModel
    project_id = "60ff165dde5f3ceacda0f2d6"

    # Get an existing segmentation project
    project = Project.get(segmented_project_id)

    # Retrieve list of all combined models in the project
    combined_models = project.get_combined_models()

    # Or just an active (current) combined model
    current_combined_model = project.get_active_combined_model()

Get information about segments in the Combined Model:

.. code-block:: python

    segments_info = current_combined_model.get_segments_info()

    # Alternatively this information can be retrieved as a Pandas DataFrame
    segments_df = current_combined_model.get_segments_as_dataframe()

    # Or even in CSV format
    current_combined_model.get_segments_as_csv("combined_model_segments.csv")

Ensure Autopilot has completed for all segments:

.. code-block:: python

    segments_info = current_combined_model.get_segments_info()
    assert all(segment.autopilot_done for segment in segments_info)

Optionally, view a list of all models associated with individual segments:

.. code-block:: python

    segments_and_child_models = project.get_segments_models(current_combined_model.id)

Set a new champion for a segment in the Combined Model, specifying the `project_id` of the segmented  project and the `model_id` from that project:

.. code-block:: python

    segment_project_id = "60ff165dde5f3ceacdaabcde"
    new_champion_id = "60ff165dde5f3ceacdaa12f7"
    
    CombinedModel.set_segment_champion(project_id=segment_project_id, model_id=new_champion_id)

If active Combined Model has already been deployed - changing champions is not allowed. In this case, create a copy of Combined Model, make it active, and set champion for it (deployed model remains unchanged):

.. code-block:: python

    new_combined_model = CombinedModel.set_segment_champion(project_id=segment_project_id, model_id=new_champion_id, clone=True)

Run predictions on the Combined Model:

.. code-block:: python

    prediction_dataset = "multiseries_predictions.csv"

    # Upload dataset
    dataset = project.upload_dataset(
        source=prediction_dataset,
    )

    # Request predictions
    predictions_job = current_combined_model.request_predictions(
        dataset_id=dataset.id,
    )
    predictions_job.wait_for_completion()
    predictions = predictions.get_result()
