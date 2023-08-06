.. _projects:

########
Projects
########

All of the modeling within DataRobot happens within a project. Each project
has one dataset that is used as the source from which to train models.

Create a Project
****************
You can create a project from previously created :ref:`datasets` or directly from a data source.

.. code-block:: python

    import datarobot as dr
    dataset = Dataset.create_from_file(file_path='/home/user/data/last_week_data.csv')
    project = dr.Project.create_from_dataset(dataset.id, project_name='New Project')

The following command creates a new project directly from a data source. You must specify a path
to data file, file object URL (starting with ``http://``, ``https://``, ``file://``, or ``s3://``),
raw file contents, or a ``pandas.DataFrame`` object when creating a new project.
Path to file can be either a path to a local file or a publicly accessible URL.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.create('/home/user/data/last_week_data.csv',
                                project_name='New Project')


You can use the following commands to view the project ID and name:

.. code-block:: python

    project.id
    >>> u'5506fcd38bd88f5953219da0'
    project.project_name
    >>> u'New Project'

Select Modeling Parameters
**************************
The final information needed to begin modeling includes the target feature, the queue mode, the metric for comparing models, and the optional parameters such as weights, offset, exposure and downsampling.

Target
======
The target must be the name of one of the columns of data uploaded to the
project.

Metric
======
The optimization metric used to compare models is an important factor in building accurate models. If a metric is not specified, the default metric recommended by DataRobot will be used. You can use the following code to view a list of valid metrics for a specified target:

.. code-block:: python

    target_name = 'ItemsPurchased'
    project.get_metrics(target_name)
    >>> {'available_metrics': [
             'Gini Norm',
             'Weighted Gini Norm',
             'Weighted R Squared',
             'Weighted RMSLE',
             'Weighted MAPE',
             'Weighted Gamma Deviance',
             'Gamma Deviance',
             'RMSE',
             'Weighted MAD',
             'Tweedie Deviance',
             'MAD',
             'RMSLE',
             'Weighted Tweedie Deviance',
             'Weighted RMSE',
             'MAPE',
             'Weighted Poisson Deviance',
             'R Squared',
             'Poisson Deviance'],
         'feature_name': 'SalePrice'}


Partitioning Method
===================

DataRobot projects always have a `holdout` set used for final model validation. We use two different approaches for testing prior to the holdout set:

- split the remaining data into `training` and `validation` sets
- cross-validation, in which the remaining data is split into a number of folds (partitions); each fold serves as a validation set, with models trained on the other folds and evaluated on that fold.

There are several other options you can control. To specify a partition method, create an instance of one of the :ref:`Partition Classes <partitions_api>`, and pass it as the ``partitioning_method`` argument in your call to ``project.set_target`` or ``project.start``.  See :ref:`here<set_up_datetime>` for more information on using datetime partitioning.

Several partitioning methods include parameters for ``validation_pct`` and ``holdout_pct``, specifying desired percentages for the validation and holdout sets. Note that there may be constraints that prevent the actual percentages used from exactly (or some cases, even closely) matching the requested percentages.

Queue Mode
==========
You can use the API to set the DataRobot modeling process to run in either automatic or manual mode.

**Autopilot** mode means that the modeling process will proceed completely
automatically, including running recommended models, running at
different sample sizes, and blending.

**Manual** mode means that DataRobot will populate a list of recommended models, but will not insert any of them into the queue. Manual mode lets you select which models to execute before starting the modeling process.

**Quick** mode means that a smaller set of Blueprints is used, so autopilot finishes faster.

Weights
=======
DataRobot also supports using a weight parameter. A full discussion of the use of weights in data science is not within the scope of this document, but weights are often used to help compensate for rare events in data. You can specify a column name in the project dataset to be used as a weight column.

Offsets
=======
Starting with version v2.6 DataRobot also supports using an offset parameter. Offsets are commonly used in insurance modeling to include effects that are outside of the training data due to regulatory compliance or constraints. You can specify the names of several columns in the project dataset to be used as the offset columns.

Exposure
========
Starting with version v2.6 DataRobot also supports using an exposure parameter. Exposure is often used to model insurance premiums where strict proportionality of premiums to duration is required. You can specify the name of the column in the project dataset to be used as an exposure column.

Start Modeling
**************

Once you have selected modeling parameters, you can use the following code structure to specify parameters and start the modeling process.

.. code-block:: python

    import datarobot as dr
    project.set_target(target='ItemsPurchased',
                       metric='Tweedie Deviance',
                       mode=dr.AUTOPILOT_MODE.FULL_AUTO)

You can also pass additional optional parameters to ``project.set_target`` to change parameters of
the modeling process. Some of those parameters include:

* ``worker_count`` -- int, sets number of workers used for modeling.
* ``partitioning_method`` -- ``PartitioningMethod`` object.
* ``positive_class`` -- str, float, or int; Specifies a level of the target column that should be treated as the positive class for binary classification.  May only be specified for binary classification targets.
* ``advanced_options`` -- :ref:`AdvancedOptions <advanced_options_api>` object, used to set advanced options of modeling process.
* ``target_type`` -- str, override the automatically selected target_type. An example usage would be setting the `target_type=TARGET_TYPE.MULTICLASS` when you want to perform a multiclass classification task on a numeric column that has a low cardinality.

For a full reference of available parameters, see :meth:`Project.set_target <datarobot.models.Project.set_target>`.

You can run with different autopilot modes with the ``mode`` parameter. ``AUTOPILOT_MODE.FULL_AUTO``
is the default, which will trigger modeling with no further actions necessary. Other accepted modes
include ``AUTOPILOT_MODE.MANUAL`` for manual mode (choose your own models to run rather than use the
DataRobot autopilot) and ``AUTOPILOT_MODE.QUICK`` for quickrun (run on a more limited set of models
to get insights more quickly).

Clone a Project
===============

Once a project has been successfully created, you may clone it using the following code structure:

.. code-block:: python

    new_project = project.clone_project(new_project_name='This is my new project')
    new_project.project_name
    >> 'This is my new project'
    new_project.id != project.id
    >> True

The ``new_project_name`` attribute is optional. If it is omitted, the default new project name will be 'Copy of <project.name>'.

Interact with a Project
***********************

The following commands can be used to manage DataRobot projects.

List Projects
=============
Returns a list of projects associated with current API user.

.. code-block:: python

    import datarobot as dr
    dr.Project.list()
    >>> [Project(Project One), Project(Two)]

    dr.Project.list(search_params={'project_name': 'One'})
    >>> [Project(One)]

You can pass following parameters to change result:

* ``search_params`` -- dict, used to filter returned projects. Currently you can query projects only by ``project_name``


Get an existing project
=======================
Rather than querying the full list of projects every time you need
to interact with a project, you can retrieve its ``id`` value and use that to reference the project.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id='5506fcd38bd88f5953219da0')
    project.id
    >>> '5506fcd38bd88f5953219da0'
    project.project_name
    >>> 'Churn Projection'


Get feature association statistics for an existing project
==========================================================
Get either feature association or correlation statistics and metadata on informative
features for a given project

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id='5506fcd38bd88f5953219da0')
    association_data = project.get_associations(assoc_type='association', metric='mutualInfo')
    association_data.keys()
    >>> ['strengths', 'features']


Get whether your featurelists have association statistics
=========================================================
Get whether an association matrix job has been run on each of your featurelists

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id='5506fcd38bd88f5953219da0')
    featurelists = project.get_association_featurelists()
    featurelists['featurelists'][0]
    >>> {"featurelistId": "54e510ef8bd88f5aeb02a3ed", "hasFam": True, "title": "Informative Features"}


Get values for a pair of features in an existing project
========================================================
Get a sample of the exact values used in the feature association matrix plotting

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id='5506fcd38bd88f5953219da0')
    feature_values = project.get_association_matrix_details(feature1='foo', feature2='bar')
    feature_values.keys()
    >>> ['features', 'types', 'values']


Update a project
================

You can update various attributes of a project.

To update the name of the project:

.. code-block:: python

    project.rename(new_name)


To update the number of workers used by your project (this will fail if you request more workers than you have
available; the special value `-1` will request your maximum number):

.. code-block:: python

    project.set_worker_count(num_workers)

To unlock the holdout set, allowing holdout scores to be shown and models to be trained on more data:

.. code-block:: python

    project.unlock_holdout()


To add or change the project description:

.. code-block:: python

    project.set_project_description(project_description)


Delete a project
================

Use the following command to delete a project:

.. code-block:: python

    project.delete()

Wait for Autopilot to Finish
============================

Once the modeling autopilot is started, in some cases you will want to wait for autopilot to finish:

.. code-block:: python

    project.wait_for_autopilot()

Play/Pause the autopilot
========================
If your project is running in autopilot mode, it will continually use
available workers, subject to the number of workers allocated to the project
and the total number of simultaneous workers allowed according to the user
permissions.

To pause a project running in autopilot mode:

.. code-block:: python

    project.pause_autopilot()

To resume running a paused project:

.. code-block:: python

    project.unpause_autopilot()

Start autopilot on another Featurelist
======================================
You can start autopilot on an existing featurelist.

.. code-block:: python

    import datarobot as dr

    featurelist = project.create_featurelist('test', ['feature 1', 'feature 2'])
    project.start_autopilot(featurelist.id)
    >>> True

    # Starting autopilot that is already running on the provided featurelist
    project.start_autopilot(featurelist.id)
    >>> dr.errors.AppPlatformError

.. note::

    This method should be used on a project where the target has already been
    set.  An error will be raised if autopilot is currently running on
    or has already finished running on the provided featurelist.

Start preparing a specific model for deployment
===============================================
You can start preparing a specific model for deployment. The model will then go through the various
recommendation stages including retraining on a reduced feature list and retraining the model on
a higher sample size (recent data for datetime partitioned).

.. code-block:: python

    project.start_prepare_model_for_deployment(model_id=model.id)

.. note::

    This method should be used on a project where the target has already been
    set.  An error will be raised if autopilot is currently running on the project or
    another model in the project is being prepared for deployment.

Further reading
***************
The Blueprints and Models sections of this document will describe how to create
new models based on the Blueprints recommended by DataRobot.

Using Credential Data
=====================

For methods that accept credential data instead of user/password or credential ID, please see :ref:`Credential Data <credential_data>`.
