.. _time_series:

####################
Time Series Projects
####################

Time series projects, like OTV projects, use :ref:`datetime partitioning<set_up_datetime>`, and all
the workflow changes that apply to other datetime partitioned projects also apply to them.
Unlike other projects, time series projects produce different types of models which forecast
multiple future predictions instead of an individual prediction for each row.

DataRobot uses a general time series framework to configure how time series features are created
and what future values the models will output. This framework consists of a Forecast Point
(defining a time a prediction is being made), a Feature Derivation Window (a rolling window used
to create features), and a Forecast Window (a rolling window of future values to predict). These
components are described in more detail below.

Time series projects will automatically transform the dataset provided in order to apply this
framework. During the transformation, DataRobot uses the Feature Derivation Window to derive
time series features (such as lags and rolling statistics), and uses the Forecast Window to provide
examples of forecasting different distances in the future (such as time shifts).
After project creation, a new dataset and a new feature list are generated and used to train
the models. This process is reapplied automatically at prediction time as well in order to
generate future predictions based on the original data features.

The ``time_unit`` and ``time_step`` used to define the Feature Derivation and Forecast Windows are
taken from the datetime partition column, and can be retrieved for a given column in the input data
by looking at the corresponding attributes on the :py:class:`datarobot.models.Feature` object.
If ``windows_basis_unit`` is set to ``ROW``, then Feature Derivation and Forecast Windows will be
defined using number of the rows.

Setting Up A Time Series Project
================================

To set up a time series project, follow the standard :ref:`datetime partitioning<set_up_datetime>`
workflow and use the six new time series specific parameters on the
:py:class:`datarobot.DatetimePartitioningSpecification` object:

use_time_series
    bool, set this to True to enable time series for the project.
default_to_known_in_advance
    bool, set this to True to default to treating all features as known in advance, or a priori, features. Otherwise,
    they will not be handled as known in advance features. Individual features can be set to a value
    different than the default by using the featureSettings parameter. See
    :ref:`the prediction documentation<time_series_predict>` for more information.
default_to_do_not_derive
    bool, set this to True to default to excluding all features from feature derivation.  Otherwise,
    they will not be excluded and will be included in the feature derivation process.
    Individual features can be set to a value different than the default by using the
    featureSettings parameter.
feature_derivation_window_start
    int, specifies how many units of the ``windows_basis_unit`` from the forecast point into the past is the start of
    the feature derivation window
feature_derivation_window_end
    int, specifies how many units of the ``windows_basis_unit`` from the forecast point into the past is the end of the
    feature derivation window
forecast_window_start
    int, specifies how many units of the ``windows_basis_unit`` from the forecast point into the future is the start of
    the forecast window
forecast_window_end
    int, specifies how many units of the ``windows_basis_unit`` from the forecast point into the future is the end of
    the forecast window
windows_basis_unit
    string, set this to ``ROW`` to define feature derivation and forecast windows in terms of the
    rows, rather than time units. If omitted, will default to the detected time unit (one of the
    ``datarobot.enums.TIME_UNITS``).
feature_settings
    list of FeatureSettings specifying per feature settings, can be left unspecified

Feature Derivation Window
*************************

The Feature Derivation window represents the rolling window that is used to derive
time series features and lags, relative to the Forecast Point. It is defined in terms of
``feature_derivation_window_start`` and ``feature_derivation_window_end`` which are integer values
representing datetime offsets in terms of the ``time_unit`` (e.g. hours or days).

The Feature Derivation Window start and end must be less than or equal to zero, indicating they are
positioned before the forecast point. Additionally, the window must be specified as an integer
multiple of the ``time_step`` which defines the expected difference in time units between rows in
the data.

The window is closed, meaning the edges are considered to be inside the window.

Forecast Window
***************

The Forecast Window represents the rolling window of future values to predict, relative to the
Forecast Point. It is defined in terms of the ``forecast_window_start`` and ``forecast_window_end``,
which are positive integer values indicating datetime offsets in terms of the ``time_unit`` (e.g.
hours or days).

The Forecast Window start and end must be positive integers, indicating they are
positioned after the forecast point. Additionally, the window must be specified as an integer
multiple of the ``time_step`` which defines the expected difference in time units between rows in
the data.

The window is closed, meaning the edges are considered to be inside the window.

.. _multiseries:

Multiseries Projects
********************

Certain time series problems represent multiple separate series of data, e.g. "I have five different
stores that all have different customer bases.  I want to predict how many units of a particular
item will sell, and account for the different behavior of each store".  When setting up the project,
a column specifying series ids must be identified, so that each row from the same series has the
same value in the multiseries id column.

Using a multiseries id column changes which partition columns are eligible for time series, as
each series is required to be unique and regular, instead of the entire partition column being
required to have those properties.  In order to use a multiseries id column for partitioning,
a detection job must first be run to analyze the relationship between the partition and multiseries
id columns.  If needed, it will be automatically triggered by calling
:py:meth:`datarobot.models.Feature.get_multiseries_properties` on the desired partition column. The
previously computed multiseries properties for a particular partition column can then be accessed
via that method.  The computation will also be automatically triggered when calling
:py:meth:`datarobot.DatetimePartitioning.generate` or :py:meth:`datarobot.models.Project.set_target`
with a multiseries id column specified.

Note that currently only one multiseries id column is supported, but all interfaces accept lists
of id columns to ensure multiple id columns will be able to be supported in the future.

In order to create a multiseries project:

   1. Set up a datetime partitioning specification with the desired partition column and multiseries
      id columns.
   #. (Optionally) Use :py:meth:`datarobot.models.Feature.get_multiseries_properties` to confirm the
      inferred time step and time unit of the partition column when used with the specified
      multiseries id column.
   #. (Optionally) Specify the multiseries id column in order to preview the full datetime
      partitioning settings using :py:meth:`datarobot.DatetimePartitioning.generate`.
   #. Specify the multiseries id column when sending the target and partitioning settings via
      :py:meth:`datarobot.models.Project.set_target`.

.. code-block:: python

   project = dr.Project.create('path/to/multiseries.csv', project_name='my multiseries project')
   partitioning_spec = dr.DatetimePartitioningSpecification(
       'timestamp', use_time_series=True, multiseries_id_columns=['multiseries_id']
   )

   # manually confirm time step and time unit are as expected
   datetime_feature = dr.Feature.get(project.id, 'timestamp')
   multiseries_props = datetime_feature.get_multiseries_properties(['multiseries_id'])
   print(multiseries_props)

   # manually check out the partitioning settings like feature derivation window and backtests
   # to make sure they make sense before moving on
   full_part = dr.DatetimePartitioning.generate(project.id, partitioning_spec)
   print(full_part.feature_derivation_window_start, full_part.feature_derivation_window_end)
   print(full_part.to_dataframe())

   # finalize the project and start the autopilot
   project.set_target('target', partitioning_method=partitioning_spec)


.. _optimized_partitioning:

You can also access optimized partitioning in the API where the target over time is inspected to
ensure that the default backtests cover regions of interest and adjust backtests avoid common
problems with missing target values or partitions with single values (e.g. zero-inflated datasets).
In this case you need to pass the target column when generating the partitioning specification and
then pass the full partitioning specification when starting autopilot.

.. code-block:: python

   project = dr.Project.create('path/to/multiseries.csv', project_name='my multiseries project')
   partitioning_spec = dr.DatetimePartitioningSpecification(
       'timestamp', use_time_series=True, multiseries_id_columns=['multiseries_id']
   )

   # Pass the target column to generate optimized partitions
   full_part = dr.DatetimePartitioning.generate(project.id, partitioning_spec, 'target')

   # finalize the project and start the autopilot, passing in the full partitioning spec
   project.set_target('target', partitioning_method=full_part.to_specification())


.. _input_vs_modeling:

Feature Settings
****************

:py:class:`datarobot.FeatureSettings` constructor receives `feature_name` and settings. For now
settings `known_in_advance` and `do_not_derive` are supported.

.. code-block:: python

    # I have 10 features, 8 of them are known in advance and two are not
    # Also, I do not want to derive new features from previous_day_sales
    not_known_in_advance_features = ['previous_day_sales', 'amount_in_stock']
    do_not_derive_features = ['previous_day_sales']
    feature_settings = [dr.FeatureSettings(feat_name, known_in_advance=False) for feat_name in not_known_in_advance_features]
    feature_settings += [dr.FeatureSettings(feat_name, do_not_derive=True) for feat_name in do_not_derive_features]
    spec = dr.DatetimePartitioningSpecification(
        # ...
        default_to_known_in_advance=True,
        feature_settings=feature_settings
    )

Modeling Data and Time Series Features
======================================

In time series projects, a new set of modeling features is created after setting the
partitioning options.  If a featurelist is specified with the partitioning options, it will be used
to select which features should be used to derived modeling features; if a featurelist is not
specified, the default featurelist will be used.

These features are automatically derived from those in the project's
dataset and are the features used for modeling - note that the Project methods
``get_featurelists`` and ``get_modeling_featurelists`` will return different data in time series
projects.  Modeling featurelists are the ones that can be used for modeling and will be accepted by
the backend, while regular featurelists will continue to exist but cannot be used.  Modeling
features are only accessible once the target and partitioning options have been
set.  In projects that don't use time series modeling, once the target has been set,
modeling and regular features and featurelists will behave the same.

Restoring Discarded Features
****************************

:py:class:`datarobot.models.restore_discarded_features.DiscardedFeaturesInfo` can be used to get and
restore features that have been removed by the time series feature generation and reduction functionality.

.. code-block:: python

    project = Project(project_id)
    discarded_feature_info = project.get_discarded_features()
    restored_features_info = project.restore_discarded_features(discarded_features_info.features)

.. _time_series_predict:

Making Predictions
==================

Prediction datasets are uploaded :ref:`as normal <predictions>`. However, when uploading a
prediction dataset, a new parameter ``forecast_point`` can be specified. The forecast point of a
prediction dataset identifies the point in time relative which predictions should be generated, and
if one is not specified when uploading a dataset, the server will choose the most recent possible
forecast point. The forecast window specified when setting the partitioning options for the project
determines how far into the future from the forecast point predictions should be calculated.

.. _new_pred_ux:

To simplify the predictions process, starting in version v2.20 a forecast point or prediction start and end dates can
be specified when requesting predictions, instead of being specified at dataset upload. Upon uploading a dataset,
DataRobot will calculate the range of dates available for use as a forecast point or for batch predictions. To that end,
:class:`Predictions<datarobot.models.Predictions>` objects now also contain the following new fields:

    - ``forecast_point``: The default point relative to which predictions will be generated
    - ``predictions_start_date``: The start date for bulk historical predictions.
    - ``predictions_end_date``: The end date for bulk historical predictions.

Similar settings are provided as part of the :ref:`batch prediction API <batch_prediction_api>`
and the `real-time prediction API <https://docs.datarobot.com/en/docs/predictions/api/dr-predapi.html#making-predictions-with-time-series>`_
to make predictions using deployed time series models.

datarobot.models.BatchPredictionJob.score

When setting up a time series project, input features could be identified as known-in-advance features.
These features are not used to generate lags, and are expected to be known for the rows in the
forecast window at predict time (e.g. "how much money will have been spent on marketing", "is this
a holiday").

Enough rows of historical data must be provided to cover the span of the effective Feature
Derivation Window (which may be longer than the project's Feature Derivation Window depending
on the differencing settings chosen).  The effective Feature Derivation Window of any model
can be checked via the ``effective_feature_derivation_window_start`` and
``effective_feature_derivation_window_end`` attributes of a
:py:class:`DatetimeModel <datarobot.models.DatetimeModel>`.

When uploading datasets to a time series project, the dataset might look something like the
following, where "Time" is the datetime partition column, "Target" is the target column, and "Temp."
is an input feature.  If the dataset was uploaded with a forecast point of "2017-01-08" and the
effective feature derivation window start and end for the model are -5 and -3 and the forecast
window start and end were set to 1 and 3, then rows 1 through 3 are historical data, row 6 is the
forecast point, and rows 7 though 9 are forecast rows that will have predictions when predictions
are computed.

.. code-block:: text

   Row, Time, Target, Temp.
   1, 2017-01-03, 16443, 72
   2, 2017-01-04, 3013, 72
   3, 2017-01-05, 1643, 68
   4, 2017-01-06, ,
   5, 2017-01-07, ,
   6, 2017-01-08, ,
   7, 2017-01-09, ,
   8, 2017-01-10, ,
   9, 2017-01-11, ,

On the other hand, if the project instead used "Holiday" as an a priori input feature, the uploaded
dataset might look like the following:

.. code-block:: text

   Row, Time, Target, Holiday
   1, 2017-01-03, 16443, TRUE
   2, 2017-01-04, 3013, FALSE
   3, 2017-01-05, 1643, FALSE
   4, 2017-01-06, , FALSE
   5, 2017-01-07, , FALSE
   6, 2017-01-08, , FALSE
   7, 2017-01-09, , TRUE
   8, 2017-01-10, , FALSE
   9, 2017-01-11, , FALSE


.. _calendar_files:

Calendars
=========

You can upload a :py:class:`calendar file <datarobot.CalendarFile>` containing a list of events relevant to your
dataset. When provided, DataRobot automatically derives and creates time series features based on the calendar
events (e.g., time until the next event, labeling the most recent event).

The calendar file:

* Should span the entire training data date range, as well as all future dates in which model will be forecasting.
* Must be in csv or xlsx format with a header row.
* Must have one date column which has values in the date-only format YYY-MM-DD (i.e., no hour, month, or second).
* Can optionally include a second column that provides the event name or type.
* Can optionally include a series ID column which specifies which series an event is applicable to. This column name
  must match the name of the column set as the series ID.

    * Multiseries ID columns are used to add an ability to specify different sets of events for different series, e.g.
      holidays for different regions.
    * Values of the series ID may be absent for specific events. This means that the event is valid for all series in
      project dataset (e.g. New Year's Day is a holiday in all series in the example below).
    * If a multiseries ID column is not provided, all listed events will be applicable to all series in the project
      dataset.

* Cannot be updated in an active project. You must specify all future calendar events at project start. To update the
  calendar file, you will have to train a new project.

An example of a valid calendar file:

.. code-block:: text

    Date,        Name
    2019-01-01,  New Year's Day
    2019-02-14,  Valentine's Day
    2019-04-01,  April Fools
    2019-05-05,  Cinco de Mayo
    2019-07-04,  July 4th

An example of a valid multiseries calendar file:

.. code-block:: text

     Date,        Name,                   Country
     2019-01-01,  New Year's Day,
     2019-05-27,  Memorial Day,           USA
     2019-07-04,  July 4th,               USA
     2019-11-28,  Thanksgiving,           USA
     2019-02-04,  Constitution Day,       Mexico
     2019-03-18,  Benito Juárez's birth,  Mexico
     2019-12-25,  Christmas Day,

Once created, a calendar can be used with a time series project by specifying the ``calendar_id`` field in the :py:class:`datarobot.DatetimePartitioningSpecification` object for the project:

.. code-block:: python

    import datarobot as dr

    # create the project
    project = dr.Project.create('input_data.csv')
    # create the calendar
    calendar = dr.CalendarFile.create('calendar_file.csv')

    # specify the calendar_id in the partitioning specification
    datetime_spec = dr.DatetimePartitioningSpecification(
        use_time_series=True,
        datetime_partition_column='date'
        calendar_id=calendar.id
    )

    # start the project, specifying the partitioning method
    project.set_target(
        target='project target',
        partitioning_method=datetime_spec
    )

.. _preloaded_calendar_files:

As of version v2.23 it is possible to ask DataRobot to generate a calendar file for you using
:py:meth:`CalendarFile.create_calendar_from_country_code<datarobot.CalendarFile.create_calendar_from_country_code>`.
This method allows you to provide a country code specifying which country's holidays to use in generating the calendar,
along with a start and end date indicating the bounds of the calendar. Allowed country codes can be retrieved using
:py:meth:`CalendarFile.get_allowed_country_codes<datarobot.CalendarFile.get_allowed_country_codes>`. See the following code block for example usage:

.. code-block:: python

    import datarobot as dr
    from datetime import datetime

    # create the project
    project = dr.Project.create('input_data.csv')
    # retrieve the allowed country codes and use the first one
    country_code = dr.CalendarFile.get_allowed_country_codes()[0]['code']
    calendar = dr.CalendarFile.create_calendar_from_country_code(
        country_code, datetime(2018, 1, 1), datetime(2018, 7, 4)
    )
    # specify the calendar_id in the partitioning specification
    datetime_spec = dr.DatetimePartitioningSpecification(
        use_time_series=True,
        datetime_partition_column='date'
        calendar_id=calendar.id
    )
    # start the project, specifying the partitioning method
    project.set_target(
        target='project target',
        partitioning_method=datetime_spec
    )

.. _datetime_trend_plots:

Datetime Trend Plots
====================

As a version v2.25, it is possible to retrieve Datetime Trend Plots for time series models
to estimate the accuracy of the model. This includes Accuracy over Time and Forecast vs Actual for supervised projects,
and Anomaly over Time for unsupervised projects. You can retrieve respective plots using following methods:

* :meth:`DatetimeModel.get_accuracy_over_time_plot<datarobot.models.DatetimeModel.get_accuracy_over_time_plot>`
* :meth:`DatetimeModel.get_forecast_vs_actual_plot<datarobot.models.DatetimeModel.get_forecast_vs_actual_plot>`
* :meth:`DatetimeModel.get_anomaly_over_time_plot<datarobot.models.DatetimeModel.get_anomaly_over_time_plot>`

By default, the plots would be automatically computed when accessed via retrieval methods. You can compute Datetime Trend Plots separately
using a common method :meth:`DatetimeModel.compute_datetime_trend_plots<datarobot.models.DatetimeModel.compute_datetime_trend_plots>`.

In addition, you can retrieve the respective detailed metadata for each plot type:

* :meth:`DatetimeModel.get_accuracy_over_time_plots_metadata<datarobot.models.DatetimeModel.get_accuracy_over_time_plots_metadata>`
* :meth:`DatetimeModel.get_forecast_vs_actual_plots_metadata<datarobot.models.DatetimeModel.get_forecast_vs_actual_plots_metadata>`
* :meth:`DatetimeModel.get_anomaly_over_time_plots_metadata<datarobot.models.DatetimeModel.get_anomaly_over_time_plots_metadata>`

And the preview plots:

* :meth:`DatetimeModel.get_accuracy_over_time_plot_preview<datarobot.models.DatetimeModel.get_accuracy_over_time_plot_preview>`
* :meth:`DatetimeModel.get_forecast_vs_actual_plot_preview<datarobot.models.DatetimeModel.get_forecast_vs_actual_plot_preview>`
* :meth:`DatetimeModel.get_anomaly_over_time_plot_preview<datarobot.models.DatetimeModel.get_anomaly_over_time_plot_preview>`

.. _prediction_intervals:

Prediction Intervals
====================

For each model, prediction intervals estimate the range of values DataRobot expects actual values of the target to fall within.
They are similar to a confidence interval of a prediction, but are based on the residual errors measured during the
backtesting for the selected model.

Note that because calculation depends on the backtesting values, prediction intervals are not available for predictions
on models that have not had all backtests completed. To that end, note that creating a prediction with prediction intervals through the API will
automatically complete all backtests if they were not already completed. For start-end retrained models, the parent model will be used for backtesting.
Additionally, prediction intervals are not available when the number of points per forecast distance is less than 10, due to insufficient data.

In a prediction request, users can specify a prediction interval's size, which specifies the desired probability of actual values
falling within the interval range. Larger values are less precise, but more conservative. For example, specifying a size
of 80 will result in a lower bound of 10% and an upper bound of 90%. More generally, for a specific `prediction_intervals_size`,
the upper and lower bounds will be calculated as follows:

* prediction_interval_upper_bound = 50% + (`prediction_intervals_size` / 2)
* prediction_interval_lower_bound = 50% - (`prediction_intervals_size` / 2)

Prediction intervals can be calculated for a :py:class:`DatetimeModel <datarobot.models.DatetimeModel>` using the
:py:meth:`DatetimeModel.calculate_prediction_intervals<datarobot.models.DatetimeModel.calculate_prediction_intervals>` method.
Users can also retrieve which intervals have already been calculated for the model using the
:py:meth:`DatetimeModel.get_calculated_prediction_intervals<datarobot.models.DatetimeModel.get_calculated_prediction_intervals>` method.

To view prediction intervals data for a prediction, the prediction needs to have been created using the
:py:meth:`DatetimeModel.request_predictions<datarobot.models.DatetimeModel.request_predictions>` method and specifying
``include_prediction_intervals = True``. The size for the prediction interval can be specified with the ``prediction_intervals_size``
parameter for the same function, and will default to 80 if left unspecified. Specifying either of these fields will
result in prediction interval bounds being included in the retrieved prediction data for that request (see the
:py:class:`Predictions <datarobot.models.Predictions>` class for retrieval methods). Note that if the specified interval
size has not already been calculated, this request will automatically calculate the specified size.

Prediction intervals are also supported for time series model deployments, and should be specified in deployment settings
if desired. Use :py:meth:`Deployment.get_prediction_intervals_settings <datarobot.Deployment.get_prediction_intervals_settings>`
to retrieve current prediction intervals settings for a deployment, and :py:meth:`Deployment.update_prediction_intervals_settings <datarobot.Deployment.update_prediction_intervals_settings>`
to update prediction intervals settings for a deployment.

Prediction intervals are also supported for time series model export. See the optional ``prediction_intervals_size`` parameter
in :py:meth:`Model.request_transferable_export <datarobot.models.Model.request_transferable_export>` for usage.


.. _partial_history_predictions:

Partial History Predictions
===========================


As of version v2.24 it is possible to ask DataRobot to allow to make predictions with incomplete historical data
multiseries regression projects. To make predictions in regular project user has to provide enough data for the
feature derivation. By setting the datetime partitioning attribute ``allow_partial_history_time_series_predictions``
to true (:py:class:`datarobot.DatetimePartitioningSpecification` object),
the project would be created that allow to make such predictions. The number of models are significantly
smaller compared to regular multiseries model, but they are designed to make predictions on unseen series with
reasonable accuracy.


.. _external_baseline_predictions:

External Baseline Predictions
=============================

As of version v2.26  it is possible to ask DataRobot to scale accuracy metric by external predictions. Users can
upload data into a Dataset (see :ref:`Dataset documentation <datasets>`) and compare the external time series
predictions with DataRobot models' accuracy performance. To use the external predictions dataset in the autopilot,
the dataset must be validated first (see
:py:meth:`Project.validate_external_time_series_baseline <datarobot.models.Project.validate_external_time_series_baseline>`).
Once the dataset is validated, it can be used with a time series project by specifying ``external_time_series_baseline_dataset_id``
field in :py:class:`AdvancedOptions <datarobot.helpers.AdvancedOptions>` and passes the advanced options to the project.
See the following code block for example usage:

.. code-block:: python

    import datarobot as dr
    from datarobot.helpers import AdvancedOptions
    from datarobot.models import Dataset

    # create the project
    project = dr.Project.create('input_data.csv')

    # prepare datatime partitioning for external baseline validation
    datetime_spec = dr.DatetimePartitioningSpecification(
        use_time_series=True,
        datetime_partition_column='date',
        multiseries_id_columns=['series_id'],
    )
    datetime_partitioning = dr.DatetimePartitioning.generate(
        project_id=project.id,
        spec=datetime_spec,
        target='target',
    )

    # create external baseline prediction dataset from local file
    external_baseline_dataset = Dataset.create_from_file(file_path='external_predictions.csv')

    # validate the external baseline prediction dataset
    validation_info = project.validate_external_time_series_baseline(
        catalog_version_id=external_baseline_dataset.version_id,
        target='target',
        datetime_partitioning=datetime_partitioning,
    )
    print(
        'External baseline predictions passes validation check:',
        validation_info.is_external_baseline_dataset_valid
    )

    # start the project and add the validated dataset version id into advanced options
    project.set_target(
        target='target',
        partitioning_method=datetime_partitioning.to_specification(),
        advanced_options=AdvancedOptions(
            external_time_series_baseline_dataset_id=external_baseline_dataset.version_id,
        )
    )

.. _external_ts_baseline_example:


.. _time_series_data_prep:

Time Series Data Prep
=============================

As of version v2.27 it is possible to prepare a dataset for time series modeling in the AI catalog
using the API client. Users can upload unprepped modeling data into a Dataset
(see :ref:`Dataset documentation <datasets>`) and the prep the data set for time series modeling by
aggregating data to a regular time step and filling gaps via a generated Spark SQL query in the AI
catalog. Once the dataset is uploaded, the time series data prep query generator can be created
using :py:meth:`DataEngineQueryGenerator.create <datarobot.DataEngineQueryGenerator.create>`
See the following code block for example usage:

.. code-block:: python

    import datarobot as dr
    from datarobot.models.data_engine_query_generator import (
        QueryGeneratorDataset,
        QueryGeneratorSettings,
    )

    # upload the dataset to the AI Catalog
    dataset = dr.Dataset.create_from_file('input_data.csv')

    # create a time series data prep query generator
    query_generator_dataset = QueryGeneratorDataset(
        alias='input_data_csv',
        dataset_id=dataset.id,
        dataset_version_id=dataset.version_id,
    )
    query_generator_settings = QueryGeneratorSettings(
        datetime_partition_column="date",
        time_unit="DAY",
        time_step=1,
        default_numeric_aggregation_method="sum",
        default_categorical_aggregation_method="mostFrequent",
        target="y",
        multiseries_id_columns=["id"],
        default_text_aggregation_method="concat",
        start_from_series_min_datetime=True,
        end_to_series_max_datetime=True,
    )
    query_generator = dr.DataEngineQueryGenerator.create(
        generator_type='TimeSeries',
        datasets = [query_generator_dataset],
        generator_settings=query_generator_settings,
    )

    # prep the training dataset
    training_dataset = query_generator.create_dataset()

    # create a project
    project = dr.Project.create_from_dataset(training_dataset.id, project_name='prepped_dataset')

    # set up datetime partitioning, target, and train model(s)
    # ...

    # upload the unprepped prediction dataset to the AI Catalog
    unprepped_prediction_dataset = dr.Dataset.create_from_file('prediction_data.csv')

    # query generator can be retrieved from the project if necessary
    # query_generator = dr.DataEngineQueryGenerator.get(project.query_generator_id)

    # prep the prediction dataset
    prediction_dataset = query_generator.create_dataset(unprepped_prediction_dataset.id)

    # make predictions
    # ...

    # query generator can be retrieved from a deployed model via project if necessary
    # deployment = dr.Deployment.get(deployment_id)
    # project = dr.Project.get(deployment.model['project_id'])
    # query_generator = dr.DataEngineQueryGenerator.get(project.query_generator_id)

.. _time_series_data_prep_example:
