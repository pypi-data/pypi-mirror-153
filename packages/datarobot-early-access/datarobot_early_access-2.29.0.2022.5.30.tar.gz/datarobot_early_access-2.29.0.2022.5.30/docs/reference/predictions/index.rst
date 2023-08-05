.. DataRobot Python Package documentation master file, created by
   sphinx-quickstart on Mon Mar 16 10:50:19 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Predictions
===========

The following sections describe the components to making predictions in DataRobot:

* **Generate predictions**: Initiate a prediction job with the ``Model.request_predictions`` object. This method can use either a training dataset or predictions dataset for scoring.
* **Batch predictions**: Score large sets of data with batch predictions. You can define jobs and their schedule.
* **Prediction API**: Use `DataRobot's Prediction API <https://docs.datarobot.com/en/docs/predictions/api/dr-predapi.html>`_. to make predictions on both a dedicated and/or a standalone prediction server.
* **Scoring Code**: Qualifying models allow you to `export Scoring Code <https://docs.datarobot.com/en/docs/predictions/scoring-code/index.html>`_ and use DataRobot-generated models outside of the platform


.. toctree::
   :maxdepth: 2

   predict_job.rst
   batch_predictions.rst
