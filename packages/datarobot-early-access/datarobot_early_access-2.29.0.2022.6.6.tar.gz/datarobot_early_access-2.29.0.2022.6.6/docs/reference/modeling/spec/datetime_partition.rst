.. _datetime_project_documentation:

#############################
Datetime Partitioned Projects
#############################

If your dataset is modeling events taking place over time, datetime partitioning may be appropriate.
Datetime partitioning ensures that when partitioning the dataset for training and validation, rows
are ordered according to the value of the date partition feature.

.. _set_up_datetime:

Setting Up a Datetime Partitioned Project
#########################################

After creating a project and before setting the target, create a
:ref:`DatetimePartitioningSpecification<datetime_part_spec>` to define how the project should
be partitioned.  By passing the specification into ``DatetimePartitioning.generate``, the full
partitioning can be previewed before finalizing the partitioning.  After verifying that the
partitioning is correct for the project dataset, pass the specification into ``Project.set_target``
via the ``partitioning_method`` argument.  Once modeling begins, the project can be used as normal.

The following code block shows the basic workflow for creating datetime partitioned projects.

.. code-block:: python

    import datarobot as dr

    project = dr.Project.create('some_data.csv')
    spec = dr.DatetimePartitioningSpecification('my_date_column')
    # can customize the spec as needed

    partitioning_preview = dr.DatetimePartitioning.generate(project.id, spec)
    # the preview generated is based on the project's data

    print(partitioning_preview.to_dataframe())
    # hmm ... I want more backtests
    spec.number_of_backtests = 5
    partitioning_preview = dr.DatetimePartitioning.generate(project.id, spec)
    print(partitioning_preview.to_dataframe())
    # looks good

    project.set_target('target_column', partitioning_method=spec)

    # I can retrieve the partitioning settings after the target has been set too
    partitioning = dr.DatetimePartitioning.get(project.id)

.. _backtest_configuration:

Configuring Backtests
---------------------

Backtests are configurable using one of two methods:

Method 1:

  * index (int): The index from zero of this backtest.
  * gap_duration (str): A duration string such as those returned by the :meth:`partitioning_methods.construct_duration_string
    <datarobot.helpers.partitioning_methods.construct_duration_string>` helper method. This represents the gap between
    training and validation scoring data for this backtest.
  * validation_start_date (datetime.datetime): Represents the start date of the validation scoring data for this backtest.
  * validation_duration (str): A duration string such as those returned by the :meth:`partitioning_methods.construct_duration_string
    <datarobot.helpers.partitioning_methods.construct_duration_string>` helper method. This represents the desired duration
    of the validation scoring data for this backtest.

.. code-block:: python

    import datarobot as dr
    from datetime import datetime

        partitioning_spec = dr.DatetimePartitioningSpecification(
            backtests=[
                # modify the first backtest using option 1
                dr.BacktestSpecification(
                    index=0,
                    gap_duration=dr.partitioning_methods.construct_duration_string(),
                    validation_start_date=datetime(year=2010, month=1, day=1),
                    validation_duration=dr.partitioning_methods.construct_duration_string(years=1),
                )
            ],
            # other partitioning settings...
        )

Method 2 (New in version v2.20):

  * validation_start_date (datetime.datetime): Represents the start date of the validation scoring data for this backtest.
  * validation_end_date (datetime.datetime): Represents the end date of the validation scoring data for this backtest.
  * primary_training_start_date (datetime.datetime): Represents the desired start date of the training partition for this backtest.
  * primary_training_end_date (datetime.datetime): Represents the desired end date of the training partition for this backtest.

.. code-block:: python

    import datarobot as dr
    from datetime import datetime

        partitioning_spec = dr.DatetimePartitioningSpecification(
            backtests=[
                # modify the first backtest using option 2
                dr.BacktestSpecification(
                    index=0,
                    primary_training_start_date=datetime(year=2005, month=1, day=1),
                    primary_training_end_date=datetime(year=2010, month=1, day=1),
                    validation_start_date=datetime(year=2010, month=1, day=1),
                    validation_end_date=datetime(year=2011, month=1, day=1),
                )
            ],
            # other partitioning settings...
        )

Note that Method 2 allows you to directly configure the start and end dates of each partition, including the training
partition. The gap partition is calculated as the time between ``primary_training_end_date`` and
``validation_start_date``. Using the same date for both ``primary_training_end_date`` and ``validation_start_date`` will
result in no gap being created.

After configuring backtests, you can set ``use_project_settings`` to ``True`` in calls to
:meth:`Model.train_datetime <datarobot.models.DatetimeModel.train_datetime>`. This will create models that are trained
and validated using your custom backtest training partition start and end dates.

.. _datetime_modeling_workflow:

Modeling with a Datetime Partitioned Project
############################################

While ``Model`` objects can still be used to interact with the project,
:ref:`DatetimeModel<datetime_mod>` objects, which are only retrievable from datetime partitioned
projects, provide more information including which date ranges and how many rows are used in
training and scoring the model as well as scores and statuses for individual backtests.

The autopilot workflow is the same as for other projects, but to manually train a model,
``Project.train_datetime`` and ``Model.train_datetime`` should be used in the place of
``Project.train`` and ``Model.train``.  To create frozen models,
``Model.request_frozen_datetime_model`` should be used in place of
``DatetimeModel.request_frozen_datetime_model``.  Unlike other projects, to trigger computation of
scores for all backtests use ``DatetimeModel.score_backtests`` instead of using the `scoring_type`
argument in the ``train`` methods.

.. _accuracy_over_time_plots:

Accuracy Over Time Plots
########################

For datetime partitioned model you can retrieve the Accuracy over Time plot. To do so use
:meth:`DatetimeModel.get_accuracy_over_time_plot<datarobot.models.DatetimeModel.get_accuracy_over_time_plot>`.
You can also retrieve the detailed metadata using :meth:`DatetimeModel.get_accuracy_over_time_plots_metadata<datarobot.models.DatetimeModel.get_accuracy_over_time_plots_metadata>`,
and the preview plot using :meth:`DatetimeModel.get_accuracy_over_time_plot_preview<datarobot.models.DatetimeModel.get_accuracy_over_time_plot_preview>`.

.. _date_dur_spec:

Dates, Datetimes, and Durations
###############################

When specifying a date or datetime for datetime partitioning, the client expects to receive and
will return a ``datetime``.  Timezones may be specified, and will be assumed to be UTC if left
unspecified.  All dates returned from DataRobot are in UTC with a timezone specified.

Datetimes may include a time, or specify only a date; however, they may have a non-zero time
component only if the partition column included a time component in its date format. If the
partition column included only dates like "24/03/2015", then the time component of any datetimes,
if present, must be zero.

When date ranges are specified with a start and an end date, the end date is exclusive, so only
dates earlier than the end date are included, but the start date is inclusive, so dates equal to or
later than the start date are included.  If the start and end date are the same, then no dates are
included in the range.

Durations are specified using a subset of ISO8601.  Durations will be of the form PnYnMnDTnHnMnS
where each "n" may be replaced with an integer value.  Within the duration string,

  * nY represents the number of years
  * the nM following the "P" represents the number of months
  * nD represents the number of days
  * nH represents the number of hours
  * the nM following the "T" represents the number of minutes
  * nS represents the number of seconds

and "P" is used to indicate that the string represents a period and "T" indicates the beginning of
the time component of the string.  Any section with a value of 0 may be excluded.  As with
datetimes, if the partition column did not include a time component in its date format, the time
component of any duration must be either unspecified or consist only of zeros.

Example Durations:

  * "P3Y6M" (three years, six months)
  * "P1Y0M0DT0H0M0S" (one year)
  * "P1Y5DT10H" (one year, 5 days, 10 hours)

:ref:`datarobot.helpers.partitioning_methods.construct_duration_string<dur_string_helper>` is a
helper method that can be used to construct appropriate duration strings.
