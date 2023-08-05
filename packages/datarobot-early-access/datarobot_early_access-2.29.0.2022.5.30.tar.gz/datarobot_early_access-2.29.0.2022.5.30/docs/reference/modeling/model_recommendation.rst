.. _model_recommendation:

####################
Model Recommendation
####################

During the Autopilot modeling process, DataRobot will recommend up to three well-performing models.

.. warning::
	Model recommendations are only generated when you run full Autopilot.

One of them (the most accurate individual, non-blender model) will be prepared for deployment.
In the preparation process, DataRobot:

1. Calculates **feature impact** for the selected model and uses it to generate **a reduced feature list**.
2. Retrains the selected model on **the reduced feature list**. If the new model performs better than the original model, DataRobot uses the new model for the next stage. Otherwise, the original model is used.
3. Retrains the selected model on **a higher sample size**. If the new model performs better than the original model, DataRobot selects it as **Recommended for Deployment**. Otherwise, the original model is selected.

.. note::
	The higher sample size DataRobot uses in Step 3 is either:

	1. **Up to holdout** if the training sample size *does not* exceed the maximum Autopilot size threshold: sample size is the training set plus the validation set (for TVH) or 5-folds (for CV). In this case, DataRobot compares retrained and original models on the holdout score.
	2. **Up to validation** if the training sample size *does* exceed the maximum Autopilot size threshold: sample size is the training set (for TVH) or 4-folds (for CV). In this case, DataRobot compares retrained and original models on the validation score.

The three types of recommendations are the following:

- **Recommended for Deployment**. This is the most accurate individual, non-blender model on the Leaderboard. This model is ready for deployment.
- **Most Accurate**. Based on the validation or cross-validation results, this model is the most accurate model overall on the Leaderboard (in most cases, a blender).
- **Fast & Accurate**. This is the most accurate individual model on the Leaderboard that passes a set prediction speed guidelines. If no models meet the guideline, the badge is not applied.

Retrieve all recommendations
----------------------------

The following code will return all models recommended for the project.

.. code-block:: python

	import datarobot as dr

	recommendations = dr.ModelRecommendation.get_all(project_id)

Retrieve a default recommendation
---------------------------------

If you are unsure about the tradeoffs between the various types of recommendations, DataRobot can make this choice
for you. The following route will return the Recommended for Deployment model to use for predictions for the project.

.. code-block:: python

	import datarobot as dr

	recommendation = dr.ModelRecommendation.get(project_id)

Retrieve a specific recommendation
----------------------------------

If you know which recommendation you want to use, you can select a specific recommendation using the
following code.

.. code-block:: python

	import datarobot as dr

	recommendation_type = dr.enums.RECOMMENDED_MODEL_TYPE.FAST_ACCURATE
	recommendations = dr.ModelRecommendation.get(project_id, recommendation_type)

Get recommended model
---------------------

You can use method `get_model()` of a recommendation object to retrieve a recommended model.

.. code-block:: python

	import datarobot as dr

	recommendation = dr.ModelRecommendation.get(project_id)
	recommended_model = recommendation.get_model()

