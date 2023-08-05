.. _models:

======
Models
======

When a blueprint has been trained on a specific dataset at a specified sample
size, the result is a model. Models can be inspected to analyze their accuracy.

Start Training a Model
**********************

To start training a model, use the :meth:`Project.train<datarobot.models.Project.train>` method with
a blueprint object:

.. code-block:: python

	import datarobot as dr
	project = dr.Project.get('5506fcd38bd88f5953219da0')
	blueprints = project.get_blueprints()
	model_job_id = project.train(blueprints[0])

For a Datetime Partitioned Project (see Specialized Workflows section), use
:meth:`Project.train_datetime<datarobot.models.Project.train_datetime>`:

.. code-block:: python

	import datarobot as dr
	project = dr.Project.get('5506fcd38bd88f5953219da0')
	blueprints = project.get_blueprints()
	model_job_id = project.train_datetime(blueprints[0])

List Finished Models
********************
You can use the :meth:`Project.get_models<datarobot.models.Project.get_models>` method to
return a list of the project models
that have finished training:

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get('5506fcd38bd88f5953219da0')
    models = project.get_models()
    print(models[:5])
    >>> [Model(Decision Tree Classifier (Gini)),
         Model(Auto-tuned K-Nearest Neighbors Classifier (Minkowski Distance)),
         Model(Gradient Boosted Trees Classifier (R)),
         Model(Gradient Boosted Trees Classifier),
         Model(Logistic Regression)]
    model = models[0]

    project.id
    >>> u'5506fcd38bd88f5953219da0'
    model.id
    >>> u'5506fcd98bd88f1641a720a3'

You can pass following parameters to change result:

* ``search_params`` -- dict, used to filter returned projects. Currently you can query models by

    * ``name``
    * ``sample_pct``
    * ``is_starred``

* ``order_by`` -- str or list, if passed returned models are ordered by this attribute(s). Allowed attributes to sort by are:

    * ``metric``
    * ``sample_pct``

  If the sort attribute is preceded by a hyphen, models will be sorted in descending
  order, otherwise in ascending order. Multiple sort attributes can be included as a comma-delimited string or in a list
  e.g. ``order_by='sample_pct,-metric'`` or ``order_by=['sample_pct', '-metric']``. Using `metric` to sort by will result
  in models being sorted according to their validation score by how well they did according to the project metric.

* ``with_metric`` -- str, If not `None`, the returned models will only have scores for this metric. Otherwise all the metrics are returned.

**List Models Example:**

.. code-block:: python

    import datarobot as dr

    dr.Project('5506fcd38bd88f5953219da0').get_models(order_by=['sample_pct', '-metric'])

    # Getting models that contain "Ridge" in name
    # and with sample_pct more than 64
    dr.Project('5506fcd38bd88f5953219da0').get_models(
        search_params={
            'sample_pct__gt': 64,
            'name': "Ridge"
        })

    # Getting models marked as starred
    dr.Project('5506fcd38bd88f5953219da0').get_models(
        search_params={
            'is_starred': True
        })

Retrieve a Known Model
**********************
If you know the ``model_id`` and ``project_id`` values of a model, you can
retrieve it directly:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)

You can also use an instance of ``Project`` as the parameter for
:meth:`Model.get<datarobot.models.Model.get>`

.. code-block:: python

    model = dr.Model.get(project=project,
                         model_id=model_id)


Train a Model on a Different Sample Size
****************************************
One of the key insights into a model and the data behind it is how its
performance varies with more training data.
In Autopilot mode, DataRobot will run at several sample sizes by default,
but you can also create a job that will run at a specific sample size.
You can also specify a featurelist that should be used for training the new model.
The :meth:`Model.train<datarobot.models.Model.train>` method of a ``Model`` instance will
put a new modeling job into the queue and return the id of the created
:doc:`ModelJob <job>`.
You can pass the ModelJob id to the :ref:`wait_for_async_model_creation<wait_for_async_model_creation-label>` function,
which polls the async model creation status and returns the newly created model when it's finished.

.. code-block:: python

    import datarobot as dr

    model_job_id = model.train(sample_pct=33)

    # Retrain a model on a custom featurelist using cross validation.
    # Note that you can specify a custom value for `sample_pct`.
    model_job_id = model.train(
        sample_pct=55,
        featurelist_id=custom_featurelist.id,
        scoring_type=dr.SCORING_TYPE.cross_validation,
    )

Cross-Validating a Model
************************
By default, models are evaluated on the first validation partition. To start
cross-validation, use the :meth:`Model.cross_validate<datarobot.models.Model.cross_validate>` method:

.. code-block:: python

    import datarobot as dr

    model_job_id = model.cross_validate()

For a :doc:Datetime Partitioned Project , backtesting is
the only cross-validation method supported. To run backtesting for a datetime model, use the
:meth:`DatetimeModel.score_backtests<datarobot.models.DatetimeModel.score_backtests>` method:

.. code-block:: python

    import datarobot as dr

    # `model` here must be an instance of `dr.DatetimeModel`.
    model_job_id = model.score_backtests()

Find the Features Used
**********************
Because each project can have many associated featurelists, it is
important to know which features a model requires in order to run. This helps ensure that the necessary features are provided when generating predictions.

.. code-block:: python

    feature_names = model.get_features_used()
    print(feature_names)
    >>> ['MonthlyIncome',
         'VisitsLast8Weeks',
         'Age']

.. _feature_impact-label:

Feature Impact
**************
Feature Impact measures how much worse a model's error score would be if DataRobot made predictions
after randomly shuffling a particular column (a technique sometimes called
`Permutation Importance`).

The following example code snippet shows how a featurelist with just the features with the highest
feature impact could be created.

.. code-block:: python

    import datarobot as dr

    max_num_features = 10
    time_to_wait_for_impact = 4 * 60  # seconds

    feature_impacts = model.get_or_request_feature_impact(time_to_wait_for_impact)

    feature_impacts.sort(key=lambda x: x['impactNormalized'], reverse=True)
    final_names = [f['featureName'] for f in feature_impacts[:max_num_features]]

    project.create_featurelist('highest_impact', final_names)

Feature Effects
*****************************
Feature Effects helps to understand how changing a single feature affects the target while holding all other
features constant. Feature Effects provides partial dependence plot and prediction vs accuracy plot data.

.. code-block:: python

    import datarobot as dr

    feature_effects = model.get_or_request_feature_effect(source='validation')

For multiclass models use ``request_feature_effect_multiclass`` and ``get_feature_effects_multiclass`` or
``get_or_request_feature_effect_multiclass`` methods.

.. code-block:: python

    import datarobot as dr

    feature_effects = model.get_feature_effect(source='validation')

Predict new data
****************
After creating models, you can use them to generate predictions on new data.
See the Predictions documentation for further information on how to request predictions
from a model.

Model IDs vs. Blueprint IDs
***************************
Each model has both a ``model_id`` and a ``blueprint_id``.

A model is the result of training a blueprint on a dataset at a specified
sample percentage. The ``blueprint_id`` is used to keep track of which
blueprint was used to train the model, while the ``model_id`` is used to
locate the trained model in the system.

Model parameters
****************
Some models can have parameters that provide data needed to reproduce their predictions.

For additional usage information see DataRobot documentation, section "Coefficients tab and
pre-processing details"

.. code-block:: python

    import datarobot as dr

    model = dr.Model.get(project=project, model_id=model_id)
    mp = model.get_parameters()
    print(mp.derived_features)
    >>> [{
             'coefficient': -0.015,
             'originalFeature': u'A1Cresult',
             'derivedFeature': u'A1Cresult->7',
             'type': u'CAT',
             'transformations': [{'name': u'One-hot', 'value': u"'>7'"}]
        }]

Create a Blender
****************
You can blend multiple models; in many cases, the resulting blender model is more accurate
than the parent models. To do so you need to select parent models and a blender method from
``datarobot.enums.BLENDER_METHOD``. If this is a time series project, only methods in
``datarobot.enums.TS_BLENDER_METHOD`` are allowed.

Be aware that the tradeoff for better prediction accuracy is bigger resource consumption
and slower predictions.

.. code-block:: python

    import datarobot as dr

    pr = dr.Project.get(pid)
    models = pr.get_models()
    parent_models = [model.id for model in models[:2]]
    pr.blend(parent_models, dr.enums.BLENDER_METHOD.AVERAGE)

Lift chart retrieval
********************
You can use the ``Model`` methods ``get_lift_chart`` and ``get_all_lift_charts`` to retrieve
lift chart data. The first will get it from specific source (validation data, cross validation or
unlocked holdout) and the second will list all available data. Please refer to the
:doc:`Advanced model information </examples/advanced_model_insights/Advanced_Model_Insights>` notebook for additional
information about lift charts and how they can be visualised.

For multiclass models, you can get a list of per-class lift charts using the ``Model`` method ``get_multiclass_lift_chart``.

ROC curve retrieval
*******************
Same as with the lift chart, you can use ``Model`` methods ``get_roc_curve`` and
``get_all_roc_curves`` to retrieve ROC curve data. Please refer to
:doc:`Advanced model information </examples/advanced_model_insights/Advanced_Model_Insights>` notebook for additional
information about ROC curves and how they can be visualised. More information about working with ROC
curves can be found in DataRobot web application documentation section "ROC Curve tab details".

.. _residuals_chart:

Residuals chart retrieval
*************************
Just as with the lift and ROC charts, you can use ``Model`` methods ``get_residuals_chart`` and
``get_all_residuals_charts`` to retrieve residuals chart data. The first will get it from a
specific source (validation data, cross-validation data, or unlocked holdout). The second
will retrieve all available data. Please refer to the
:doc:`Advanced model information </examples/advanced_model_insights_regression/Advanced_Model_Insights_Regression>`
notebook for more information about residuals charts and how they can be visualised.

Word Cloud
**********
If your dataset contains text columns, DataRobot can create text processing models that will
contain word cloud insight data. An example of such a model is any "Auto-Tuned Word N-Gram Text
Modeler" model. You can use the ``Model.get_word_cloud`` method to retrieve those insights - it will
provide up to the 200 most important ngrams in the model and coefficients corresponding to their influence.
The :doc:`Advanced model information </examples/advanced_model_insights/Advanced_Model_Insights>` notebook contains
examples of how you can use that data and build a visualization in a way similar to how the
DataRobot webapp does.

Scoring Code
************
Subset of models in DataRobot supports code generation. For each of those models you can download
a JAR file with scoring code to make predictions locally using the method
``Model.download_scoring_code``. For details on how to do that see "Code Generation" section in
DataRobot web application documentation. Optionally you can download source code in Java to see
what calculations those models do internally.

Be aware that the source code JAR isn't compiled so it cannot be used for making predictions.

.. _model_blueprint_chart:

Get a model blueprint chart
***************************
For any model, you can retrieve its blueprint chart. You can also get its representation in graphviz DOT format to render it into the format you need.

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)
    bp_chart = model.get_model_blueprint_chart()
    print(bp_chart.to_graphviz())

.. _missing_values_report:

Get a model missing values report
*********************************
For the majority of models, you can retrieve their missing values reports on training data
per each numeric and categorical feature. Model needs to have at least one of the supported tasks
in the blueprint in order to have a missing values report (blenders are not supported).
Report is gathered for Numerical Imputation tasks and Categorical converters like Ordinal Encoding,
One-Hot Encoding, etc.
Missing values report is available to users with access to full blueprint docs.

A report is collected for those features which are considered eligible by a given blueprint task.
For instance, a categorical feature with a lot of unique values may not be considered as eligible in
the One-Hot encoding task.

Please refer to :ref:`Missing report attributes description <missing_values_report_api>`
for report interpretation.

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id, model_id=model_id)
    missing_reports_per_feature = model.get_missing_report_info()
    for report_per_feature in missing_reports_per_feature:
        print(report_per_feature)

Consider the following example. Given Decision Tree Classifier (Gini) blueprint chart representation:

.. code-block:: python

    print(blueprint_chart.to_graphviz())
    >>> digraph "Blueprint Chart" {
            graph [rankdir=LR]
            0 [label="Data"]
            -2 [label="Numeric Variables"]
            2 [label="Missing Values Imputed"]
            3 [label="Decision Tree Classifier (Gini)"]
            4 [label="Prediction"]
            -1 [label="Categorical Variables"]
            1 [label="Ordinal encoding of categorical variables"]
            0 -> -2
            -2 -> 2
            2 -> 3
            3 -> 4
            0 -> -1
            -1 -> 1
            1 -> 3
        }

and missing report:

.. code-block:: python

    print(report_per_feature1)
    >>> {'feature': 'Veh Year',
         'type': 'Numeric',
         'missing_count': 150,
         'missing_percentage': 50.00,
         'tasks': [
                    {'id': u'2',
                    'name': u'Missing Values Imputed',
                    'descriptions': [u'Imputed value: 2006']
                    }
            ]
          }
    print(report_per_feature2)
    >>> {'feature': 'Model',
         'type': 'Categorical',
         'missing_count': 100,
         'missing_percentage': 33.33,
         'tasks': [
                    {'id': u'1',
                    'name': u'Ordinal encoding of categorical variables',
                    'descriptions': [u'Imputed value: -2']
                    }
              ]
            }

results can be interpreted in the following way:

Numeric feature "Veh Year" has 150 missing values and respectively 50% in training data.
It was transformed by "Missing Values Imputed" task with imputed value 2006. Task has id 2, and its
output goes into Decision Tree Classifier (Gini) - it can be inferred from the chart.

Categorical feature "Model" was transformed by "Ordinal encoding of categorical variables" task with
imputed value -2.

.. _model_blueprint_doc:

Get a blueprint's documentation
*******************************
You can retrieve documentation on tasks used to build a model. It will contain information about the task, its parameters and (when available) links and references to additional sources.
All documents are instances of ``BlueprintTaskDocument`` class.

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)
    docs = model.get_model_blueprint_documents()
    print(docs[0].task)
    >>> Average Blend
    print(docs[0].links[0]['url'])
    >>> https://en.wikipedia.org/wiki/Ensemble_learning

.. _model_training_predictions:

Request training predictions
****************************
You can request a model's predictions for a particular subset of its training data.
See :py:meth:`datarobot.models.Model.request_training_predictions` reference for all the valid subsets.

See :ref:`training predictions reference<training_predictions>` for more details.

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)
    training_predictions_job = model.request_training_predictions(dr.enums.DATA_SUBSET.HOLDOUT)
    training_predictions = training_predictions_job.get_result_when_complete()
    for row in training_predictions.iterate_rows():
        print(row.row_id, row.prediction)

.. _advanced_tuning:

Advanced Tuning
***************
You can perform advanced tuning on a model -- generate a new model by taking an existing
model and rerunning it with modified tuning parameters.

The AdvancedTuningSession class exists to track the creation of an Advanced Tuning model on the
client.  It enables browsing and setting advanced-tuning parameters one at a time, and
using human-readable parameter names rather than requiring opaque parameter IDs in all cases.
No information is sent to the server until the `run()` method is called on the
AdvancedTuningSession.

See :py:meth:`datarobot.models.Model.get_advanced_tuning_parameters` reference for a description
of the types of parameters that can be passed in.

As of v2.17, all models other than blenders, open source, and user-created models support
Advanced Tuning. The use of Advanced Tuning via API for non-Eureqa models is in beta, but is enabled
by default for all users.


.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)
    tune = model.start_advanced_tuning_session()

    # Get available task names,
    # and available parameter names for a task name that exists on this model
    tune.get_task_names()
    tune.get_parameter_names('Eureqa Generalized Additive Model Classifier (3000 Generations)')

    tune.set_parameter(
        task_name='Eureqa Generalized Additive Model Classifier (3000 Generations)',
        parameter_name='EUREQA_building_block__sine',
        value=1)

    job = tune.run()

.. _shap_impact:

SHAP Impact
***********
You can retrieve SHAP impact scores for features in a model.
SHAP impact is computed by calculating the shap values on a sample of training data and then taking
the mean absolute value for each column. The larger value of impact indicates a more important feature.

See :py:meth:`datarobot.models.ShapImpact.create` reference for a description of the types of parameters
that can be passed in.


.. code-block:: python

    import datarobot as dr

    project_id = '5ec3d6884cfad17cd8c0ed62'
    model_id = '5ec3d6f44cfad17cd8c0ed78'
    shap_impact_job = dr.ShapImpact.create(project_id=project_id, model_id=model_id)
    shap_impact = shap_impact_job.get_result_when_complete()
    print(shap_impact)
    >>> [ShapImpact(count=36)]
    print(shap_impact.shap_impacts[:1])
    >>> [{'feature_name': 'number_inpatient', 'impact_normalized': 1.0, 'impact_unnormalized': 0.07670175497683789}]

    shap_impact = dr.ShapImpact.get(project_id=project_id, model_id=model_id)
    print(shap_impact.shap_impacts[:1])
    >>> [{'feature_name': 'number_inpatient', 'impact_normalized': 1.0, 'impact_unnormalized': 0.07670175497683789}]

Number of Iterations Trained
*****************************
Early-stopping models will train a subset of max estimators/iterations that are defined in advanced tuning.
This method allows the user to retrieve the actual number of estimators that were trained by an early-stopping
tree-based model (currently the only model type supported). The method returns the projectId, modelId, and
a list of dictionaries containing the number of iterations trained for each model stage. In the case of single-stage models,
this dictionary will contain only one entry.


.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)
    num_iterations = model.get_num_iterations_trained()
    print(num_iterations)
    >>> {"projectId": "5506fcd38bd88f5953219da0", "modelId": "5506fcd98bd88f1641a720a3", "data" [{"stage": "FREQ", "numIterations":250}, {"stage":"SEV", "numIterations":50}]}
