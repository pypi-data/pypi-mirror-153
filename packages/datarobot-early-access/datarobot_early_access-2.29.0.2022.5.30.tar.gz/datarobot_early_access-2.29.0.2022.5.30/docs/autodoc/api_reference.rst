API Reference
#############

.. _advanced_options_api:

Advanced Options
================

.. autoclass:: datarobot.helpers.AdvancedOptions
   :members:

.. _anomaly_assessment_api:

Anomaly Assessment
==================

.. autoclass::  datarobot.models.anomaly_assessment.AnomalyAssessmentRecord
   :members:

.. autoclass::  datarobot.models.anomaly_assessment.AnomalyAssessmentExplanations
   :members:

.. autoclass::  datarobot.models.anomaly_assessment.AnomalyAssessmentPredictionsPreview
   :members:

.. _batch_prediction_api:

Batch Predictions
=================

.. autoclass:: datarobot.models.BatchPredictionJob
   :members:

.. autoclass:: datarobot.models.BatchPredictionJobDefinition
   :members:

Blueprint
=========

.. autoclass:: datarobot.models.Blueprint
   :members:

.. autoclass:: datarobot.models.BlueprintTaskDocument
   :members:

.. autoclass:: datarobot.models.BlueprintChart
   :members:

.. autoclass:: datarobot.models.ModelBlueprintChart
   :members: get, to_graphviz

Calendar File
=============

.. autoclass:: datarobot.CalendarFile
   :members:

.. _automated_documentation_api:

Automated Documentation
========================

.. autoclass:: datarobot.models.automated_documentation.AutomatedDocument
   :members:

Class Mapping Aggregation Settings
==================================

For multiclass projects with a lot of unique values in target column you can
specify the parameters for aggregation of rare values to improve the modeling
performance and decrease the runtime and resource usage of resulting models.

.. autoclass:: datarobot.helpers.ClassMappingAggregationSettings
   :members:

Clustering
==========

.. autoclass:: datarobot.models.ClusteringModel
   :members:

.. autoclass:: datarobot.models.cluster.Cluster
   :members:

.. autoclass:: datarobot.models.cluster_insight.ClusterInsight
   :members:


Compliance Documentation Templates
==================================

.. autoclass:: datarobot.models.compliance_doc_template.ComplianceDocTemplate
   :members:

Compliance Documentation
========================

.. autoclass:: datarobot.models.compliance_documentation.ComplianceDocumentation
   :members:

Confusion Chart
===============

.. autoclass:: datarobot.models.confusion_chart.ConfusionChart
   :members:

.. _credential_api:

Credentials
=================

.. autoclass:: datarobot.models.Credential
   :members:

Custom Models
=============

.. autoclass:: datarobot.models.custom_model_version.CustomModelFileItem
   :members:

.. autoclass:: datarobot.CustomInferenceImage
   :members:

.. autoclass:: datarobot.CustomInferenceModel
   :members:

.. autoclass:: datarobot.CustomModelTest
   :members:

.. autoclass:: datarobot.CustomModelVersion
   :members:

.. autoclass:: datarobot.models.execution_environment.RequiredMetadataKey
   :members:

.. autoclass:: datarobot.CustomModelVersionDependencyBuild
   :members:

.. autoclass:: datarobot.ExecutionEnvironment
   :members:

.. autoclass:: datarobot.ExecutionEnvironmentVersion
   :members:

Custom Tasks
============

.. autoclass:: datarobot.CustomTask
   :members:

.. autoclass:: datarobot.models.custom_task_version.CustomTaskFileItem
   :members:

.. autoclass:: datarobot.CustomTaskVersion
   :members:

Database Connectivity
=====================

.. autoclass:: datarobot.DataDriver
   :members:

.. autoclass:: datarobot.Connector
   :members:

.. autoclass:: datarobot.DataStore
   :members:

.. autoclass:: datarobot.DataSource
   :members:

.. autoclass:: datarobot.DataSourceParameters

Datasets
========

.. autoclass:: datarobot.Dataset
   :members:

.. autoclass:: datarobot.DatasetDetails
   :members:

Data Engine Query Generator
===========================

.. autoclass:: datarobot.DataEngineQueryGenerator
   :members:

Datetime Trend Plots
====================

.. autoclass:: datarobot.models.datetime_trend_plots.AccuracyOverTimePlotsMetadata
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.AccuracyOverTimePlot
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.AccuracyOverTimePlotPreview
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.ForecastVsActualPlotsMetadata
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.ForecastVsActualPlot
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.ForecastVsActualPlotPreview
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.AnomalyOverTimePlotsMetadata
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.AnomalyOverTimePlot
   :members:

.. autoclass:: datarobot.models.datetime_trend_plots.AnomalyOverTimePlotPreview
   :members:
   
Deployment
==========

.. autoclass:: datarobot.Deployment
   :members:

.. autoclass:: datarobot.models.deployment.DeploymentListFilters
   :members:

.. autoclass:: datarobot.models.ServiceStats
   :members:

.. autoclass:: datarobot.models.ServiceStatsOverTime
   :members:

.. autoclass:: datarobot.models.TargetDrift
   :members:

.. autoclass:: datarobot.models.FeatureDrift
   :members:

.. autoclass:: datarobot.models.Accuracy
   :members:

.. autoclass:: datarobot.models.AccuracyOverTime
   :members:

External Scores and Insights
============================

.. autoclass:: datarobot.ExternalScores
   :members:

.. autoclass:: datarobot.ExternalLiftChart
   :members:

.. autoclass:: datarobot.ExternalRocCurve
   :members:

Feature
=======

.. autoclass:: datarobot.models.Feature
   :members:

.. autoclass:: datarobot.models.ModelingFeature
   :members:

.. autoclass:: datarobot.models.DatasetFeature
   :members:

.. autoclass:: datarobot.models.DatasetFeatureHistogram
   :members:

.. autoclass:: datarobot.models.FeatureHistogram
   :members:

.. autoclass:: datarobot.models.InteractionFeature
   :members:

.. autoclass:: datarobot.models.MulticategoricalHistogram
   :members:

.. autoclass:: datarobot.models.PairwiseCorrelations
   :members:

.. autoclass:: datarobot.models.PairwiseJointProbabilities
   :members:

.. autoclass:: datarobot.models.PairwiseConditionalProbabilities
   :members:

Feature Association
===================

.. autoclass:: datarobot.models.FeatureAssociationMatrix
   :members:

Feature Association Matrix Details
==================================

.. autoclass:: datarobot.models.FeatureAssociationMatrixDetails
   :members:

Feature Association Featurelists
================================

.. autoclass:: datarobot.models.FeatureAssociationFeaturelists
   :members:

Feature Discovery
=================

.. _relationship_config:

Relationships Configuration
***************************
.. autoclass:: datarobot.models.RelationshipsConfiguration
   :members: create, get, delete, replace


.. _dataset_definition:

Dataset Definition
******************
.. autoclass:: datarobot.helpers.feature_discovery.DatasetDefinition
   :members:

.. _relationship:

Relationship
************
.. autoclass:: datarobot.helpers.feature_discovery.Relationship
   :members:

Feature Lineage
***************
.. autoclass:: datarobot.models.FeatureLineage
   :members: get

.. _secondary_dataset_config:

Secondary Dataset Configurations
********************************

.. autoclass:: datarobot.models.SecondaryDatasetConfigurations
   :members: create, get, delete, list

.. _secondary_dataset:

Secondary Dataset
*****************
.. autoclass:: datarobot.helpers.feature_discovery.SecondaryDataset
   :members:

Feature Effects
===============

.. autoclass:: datarobot.models.FeatureEffects
   :members:

.. autoclass:: datarobot.models.FeatureEffectMetadata
   :members:

.. autoclass:: datarobot.models.FeatureEffectMetadataDatetime
   :members:

.. autoclass:: datarobot.models.FeatureEffectMetadataDatetimePerBacktest
   :members:

Feature Fit
===========

.. autoclass:: datarobot.models.FeatureFit
   :members:

.. autoclass:: datarobot.models.FeatureFitMetadata
   :members:

.. autoclass:: datarobot.models.FeatureFitMetadataDatetime
   :members:

.. autoclass:: datarobot.models.FeatureFitMetadataDatetimePerBacktest
   :members:

Feature List
============

.. autoclass:: datarobot.DatasetFeaturelist
   :members: get, update, delete

.. autoclass:: datarobot.models.Featurelist
   :members: get, update, delete

.. autoclass:: datarobot.models.ModelingFeaturelist
   :members: get, update, delete


Restoring Discarded Features
============================

.. autoclass:: datarobot.models.restore_discarded_features.DiscardedFeaturesInfo
   :members:

Job
===

.. _jobs_api:

.. autoclass:: datarobot.models.Job
   :members:
   :inherited-members:

.. autoclass:: datarobot.models.TrainingPredictionsJob
   :members:
   :inherited-members:

.. autoclass:: datarobot.models.ShapMatrixJob
   :members:
   :inherited-members:

.. autoclass:: datarobot.models.FeatureImpactJob
   :members:
   :inherited-members:

Lift Chart
==========

.. autoclass:: datarobot.models.lift_chart.LiftChart
   :members:

.. _missing_values_report_api:

Missing Values Report
=====================

.. autoclass:: datarobot.models.missing_report.MissingValuesReport
   :members:
   :exclude-members: from_server_data

Models
======

Model
*****

.. autoclass:: datarobot.models.Model
   :members:
   :exclude-members: from_server_data

PrimeModel
**********

.. autoclass:: datarobot.models.PrimeModel
   :inherited-members:
   :members:
   :exclude-members: from_server_data, request_frozen_model, request_frozen_datetime_model, train, train_datetime, request_approximation

BlenderModel
************

.. autoclass:: datarobot.models.BlenderModel
   :members:
   :inherited-members:
   :exclude-members: from_server_data

.. _datetime_mod:

DatetimeModel
*************

.. autoclass:: datarobot.models.DatetimeModel
   :inherited-members:
   :members:
   :exclude-members: from_server_data, train, request_frozen_model

Frozen Model
************

.. autoclass:: datarobot.models.FrozenModel
   :members:

Imported Model
**************

.. note::
   Imported Models are used in Stand Alone Scoring Engines.  If you are not an administrator of such
   an engine, they are not relevant to you.

.. autoclass:: datarobot.models.ImportedModel
   :members:

RatingTableModel
****************

.. autoclass:: datarobot.models.RatingTableModel
   :inherited-members:
   :members:
   :exclude-members: from_server_data

Combined Model
**************

See API reference for Combined Model in :ref:`Segmented Modeling API Reference<segmented_modeling_api>`

Advanced Tuning
***************

.. autoclass:: datarobot.models.advanced_tuning.AdvancedTuningSession
   :members:

ModelJob
========

.. _wait_for_async_model_creation-api-label:
.. autofunction:: datarobot.models.modeljob.wait_for_async_model_creation

.. _modeljob_api:
.. autoclass:: datarobot.models.ModelJob
   :members:
   :inherited-members:

Pareto Front
============

.. autoclass:: datarobot.models.pareto_front.ParetoFront
   :members:

.. autoclass:: datarobot.models.pareto_front.Solution
   :members:

.. _partitions_api:

Partitioning
============

.. autoclass:: datarobot.RandomCV
   :members:

.. autoclass:: datarobot.StratifiedCV
   :members:

.. autoclass:: datarobot.GroupCV
   :members:

.. autoclass:: datarobot.UserCV
   :members:

.. autoclass:: datarobot.RandomTVH
   :members:

.. autoclass:: datarobot.UserTVH
   :members:

.. autoclass:: datarobot.StratifiedTVH
   :members:

.. autoclass:: datarobot.GroupTVH
   :members:

.. _datetime_part_spec:
.. autoclass:: datarobot.DatetimePartitioningSpecification
   :members:

.. autoclass:: datarobot.BacktestSpecification
   :members:

.. autoclass:: datarobot.FeatureSettings
   :members:

.. autoclass:: datarobot.Periodicity
   :members:

.. _datetime_part:
.. autoclass:: datarobot.DatetimePartitioning
   :members:

.. autoclass:: datarobot.helpers.partitioning_methods.Backtest
   :members:

.. _dur_string_helper:
.. autofunction:: datarobot.helpers.partitioning_methods.construct_duration_string

PayoffMatrix
============

.. autoclass:: datarobot.models.PayoffMatrix
   :members:
   :inherited-members:

PredictJob
==========

.. _wait_for_async_predictions=api=label:
.. autofunction:: datarobot.models.predict_job.wait_for_async_predictions

.. _predict_job_api:
.. autoclass:: datarobot.models.PredictJob
   :members:
   :inherited-members:

Prediction Dataset
==================

.. autoclass:: datarobot.models.PredictionDataset
   :members:


.. _pred_expl_api:

Prediction Explanations
=======================

.. autoclass:: datarobot.PredictionExplanationsInitialization
   :members:

.. autoclass:: datarobot.PredictionExplanations
   :members:

.. autoclass:: datarobot.models.prediction_explanations.PredictionExplanationsRow
   :members:

.. autoclass:: datarobot.models.prediction_explanations.PredictionExplanationsPage
   :members:

.. autoclass:: datarobot.models.ShapMatrix
   :members:

.. autoclass:: datarobot.models.ClassListMode
   :members:

.. autoclass:: datarobot.models.TopPredictionsMode
   :members:


.. _predictions_api:

Predictions
===========

.. autoclass:: datarobot.models.Predictions
    :members:

PredictionServer
================

.. autoclass:: datarobot.PredictionServer
    :members:

PrimeFile
=========

.. autoclass:: datarobot.models.PrimeFile
   :members:

Project
=======

.. autoclass:: datarobot.models.Project
   :members:

.. autoclass:: datarobot.helpers.eligibility_result.EligibilityResult
   :members:

Rating Table
============

.. autoclass:: datarobot.models.RatingTable
   :members:
   :exclude-members: from_server_data

.. _recommended_models:

Recommended Models
==================

.. autoclass:: datarobot.models.ModelRecommendation
   :members:

ROC Curve
=========

.. autoclass:: datarobot.models.roc_curve.RocCurve
   :members:

.. autoclass:: datarobot.models.roc_curve.LabelwiseRocCurve
   :members:

Ruleset
=======

.. autoclass:: datarobot.models.Ruleset
   :members:


.. _segmented_modeling_api:

Segmented Modeling
==================

API Reference for entities used in Segmented Modeling. See dedicated :ref:`User Guide<segmented_modeling>` for examples.

.. autoclass:: datarobot.CombinedModel
    :members:

.. autoclass:: datarobot.SegmentationTask
    :members:

.. autoclass:: datarobot.SegmentInfo
    :members:

SHAP
====

.. autoclass:: datarobot.models.ShapImpact
   :members:

SharingAccess
=============

.. autoclass:: datarobot.SharingAccess

.. _training_predictions_api:

Training Predictions
====================

.. automodule:: datarobot.models.training_predictions
   :members: TrainingPredictions, TrainingPredictionsIterator

.. _user_blueprints_api:

User Blueprints
===============

.. autoclass:: datarobot.UserBlueprint
   :members:

VisualAI
========

.. autoclass:: datarobot.models.visualai.Image
   :members:

.. autoclass:: datarobot.models.visualai.SampleImage
   :members:

.. autoclass:: datarobot.models.visualai.DuplicateImage
   :members:

.. autoclass:: datarobot.models.visualai.ImageEmbedding
   :members:

.. autoclass:: datarobot.models.visualai.ImageActivationMap
   :members:

.. autoclass:: datarobot.models.visualai.ImageAugmentationOptions
   :members:

.. autoclass:: datarobot.models.visualai.ImageAugmentationList
   :members:

.. autoclass:: datarobot.models.visualai.ImageAugmentationSample
   :members:

Word Cloud
==========

.. autoclass:: datarobot.models.word_cloud.WordCloud
   :members:

.. only:: include_experimental_docs

    Experimental API features
    =========================
    These features all require special permissions to be activated on your DataRobot account, and
    will not work otherwise. If you want to test a feature, please ask your DataRobot CFDS or
    account manager about enrolling in our preview program.

    Classes in this list should be considered "experimental", not fully released, and likely to
    change in future releases. **Do not use them for production systems or other mission-critical
    uses.**

    .. autoclass:: datarobot._experimental.models.model.Model
       :members:

    .. autoclass:: datarobot._experimental.models.model.DatetimeModel
       :members:

    .. autoclass:: datarobot._experimental.models.model_package.ModelPackage
       :members:

    .. autoclass:: datarobot._experimental.models.project.Project
       :members:

    .. autoclass:: datarobot._experimental.models.segmentation.SegmentationTask
       :members:
