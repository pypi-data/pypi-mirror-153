.. _rating_table:

============
Rating Table
============
A rating table is an exportable csv representation of a Generalized Additive Model. They contain
information about the features and coefficients used to make predictions. Users can influence
predictions by downloading and editing values in a rating table, then reuploading the table and
using it to create a new model.

See the page about interpreting Generalized Additive Models' output in the Datarobot user guide for
more details on how to interpret and edit rating tables.

Download A Rating Table
***********************
You can retrieve a rating table from the list of rating tables in a project:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    project = dr.Project.get(project_id)
    rating_tables = project.get_rating_tables()
    rating_table = rating_tables[0]

Or you can retrieve a rating table from a specific model. The model must already exist:

.. code-block:: python

    import datarobot as dr
    from datarobot.models import RatingTableModel, RatingTable
    project_id = '5506fcd38bd88f5953219da0'
    project = dr.Project.get(project_id)

    # Get model from list of models with a rating table
    rating_table_models = project.get_rating_table_models()
    rating_table_model = rating_table_models[0]

    # Or retrieve model by id. The model must have a rating table.
    model_id = '5506fcd98bd88f1641a720a3'
    rating_table_model = dr.RatingTableModel.get(project=project_id, model_id=model_id)

    # Then retrieve the rating table from the model
    rating_table_id = rating_table_model.rating_table_id
    rating_table = dr.RatingTable.get(projcet_id, rating_table_id)

Then you can download the contents of the rating table:

.. code-block:: python

    rating_table.download('./my_rating_table.csv')

Uploading A Rating Table
************************
After you've retrieved the rating table CSV and made the necessary edits, you
can re-upload the CSV so you can create a new model from it:

.. code-block:: python

    job = dr.RatingTable.create(project_id, model_id, './my_rating_table.csv')
    new_rating_table = job.get_result_when_complete()
    job = new_rating_table.create_model()
    model = job.get_result_when_complete()
