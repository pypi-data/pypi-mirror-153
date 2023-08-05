.. _monotonic_constraints:

#####################
Monotonic Constraints
#####################

Training with monotonic constraints allows users to force models to learn monotonic relationships with respect to some features and the target. This helps users create accurate models that comply with regulations (e.g. insurance, banking). Currently, only certain blueprints (e.g. xgboost) support this feature, and it is only supported for regression and binary classification projects. Typically working with monotonic constraints follows the following two workflows:

Workflow one - Running a project with default monotonic constraints

* set the target and specify default constraint lists for the project
* when running autopilot or manually training models without overriding constraint settings, all blueprints that support monotonic constraints will use the specified default constraint featurelists

Workflow two - Running a model with specific monotonic constraints

* create featurelists for monotonic constraints
* train a blueprint that supports monotonic constraints while specifying monotonic constraint featurelists
* the specified constraints will be used, regardless of the defaults on the blueprint

Creating featurelists
---------------------

When specifying monotonic constraints, users must pass a reference to a featurelist containing only the features to be constrained, one for features that should monotonically increase with the target and another for those that should monotonically decrease with the target.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id)
    features_mono_up = ['feature_0', 'feature_1']  # features that have monotonically increasing relationship with target
    features_mono_down = ['feature_2', 'feature_3']  # features that have monotonically decreasing relationship with target
    flist_mono_up = project.create_featurelist(name='mono_up',
                                               features=features_mono_up)
    flist_mono_down = project.create_featurelist(name='mono_down',
                                                 features=features_mono_down)

Specify default monotonic constraints for a project
---------------------------------------------------

When setting the target, the user can specify default monotonic constraints for the project, to ensure that autopilot models use the desired settings, and optionally to ensure that only blueprints supporting monotonic constraints appear in the project. Regardless of the defaults specified during target selection, the user can override them when manually training a particular model.

.. code-block:: python

    import datarobot as dr
    from datarobot.enums import AUTOPILOT_MODE
    advanced_options = dr.AdvancedOptions(
        monotonic_increasing_featurelist_id=flist_mono_up.id, 
        monotonic_decreasing_featurelist_id=flist_mono_down.id,
        only_include_monotonic_blueprints=True)
    project = dr.Project.get(project_id)
    project.set_target(target='target', mode=AUTOPILOT_MODE.FULL_AUTO, advanced_options=advanced_options)

Retrieve models and blueprints using monotonic constraints
----------------------------------------------------------

When retrieving models, users can inspect to see which supports monotonic constraints, and which actually enforces them. Some models will not support monotonic constraints at all, and some may support constraints but not have any constrained features specified.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id)
    models = project.get_models()
    # retrieve models that support monotonic constraints
    models_support_mono = [model for model in models if model.supports_monotonic_constraints]
    # retrieve models that support and enforce monotonic constraints
    models_enforce_mono = [model for model in models
                           if (model.monotonic_increasing_featurelist_id or
                               model.monotonic_decreasing_featurelist_id)]

When retrieving blueprints, users can check if they support monotonic constraints and see what default contraint lists are associated with them. The monotonic featurelist ids associated with a blueprint will be used everytime it is trained, unless the user specifically overrides them at model submission time.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id)
    blueprints = project.get_blueprints()
    # retrieve blueprints that support monotonic constraints
    blueprints_support_mono = [blueprint for blueprint in blueprints if blueprint.supports_monotonic_constraints]
    # retrieve blueprints that support and enforce monotonic constraints
    blueprints_enforce_mono = [blueprint for blueprint in blueprints
                               if (blueprint.monotonic_increasing_featurelist_id or
                                   blueprint.monotonic_decreasing_featurelist_id)]

Train a model with specific monotonic constraints
-------------------------------------------------

Even after specifiying default settings for the project, users can override them to train a new model with different constraints, if desired.

.. code-block:: python

    import datarobot as dr
    features_mono_up = ['feature_2', 'feature_3']  # features that have monotonically increasing relationship with target
    features_mono_down = ['feature_0', 'feature_1']  # features that have monotonically decreasing relationship with target
    project = dr.Project.get(project_id)
    flist_mono_up = project.create_featurelist(name='mono_up',
                                               features=features_mono_up)
    flist_mono_down = project.create_featurelist(name='mono_down',
                                                 features=features_mono_down)
    model_job_id = project.train(
        blueprint,
        sample_pct=55,
        featurelist_id=featurelist.id,
        monotonic_increasing_featurelist_id=flist_mono_up.id,
        monotonic_decreasing_featurelist_id=flist_mono_down.id
    )