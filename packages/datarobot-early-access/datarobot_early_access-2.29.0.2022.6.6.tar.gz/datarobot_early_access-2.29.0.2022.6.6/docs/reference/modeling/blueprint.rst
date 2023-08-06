##########
Blueprints
##########

The set of computation paths that a dataset passes through before producing
predictions from data is called a blueprint. A blueprint can be trained on
a dataset to generate a model.

To modify blueprints using python, please refer to the `documentation
for the Blueprint Workshop <https://blueprint-workshop.datarobot.com/>`_.

Quick Reference
***************
The following code block summarizes the interactions available for blueprints.

.. code-block:: python

    # Get the set of blueprints recommended by datarobot
    import datarobot as dr
    my_projects = dr.Project.list()
    project = my_projects[0]
    menu = project.get_blueprints()

    first_blueprint = menu[0]
    project.train(first_blueprint)

List Blueprints
***************
When a file is uploaded to a project and the target is set, DataRobot
recommends a set of blueprints that are appropriate for the task at hand.
You can use the ``get_blueprints`` method to get the list of blueprints recommended for a project:

.. code-block:: python

    project = dr.Project.get('5506fcd38bd88f5953219da0')
    menu = project.get_blueprints()
    blueprint = menu[0]

Get a blueprint
***************
If you already have a ``blueprint_id`` from a model you can retrieve the blueprint directly.

.. code-block:: python

    project_id = '5506fcd38bd88f5953219da0'
    project = dr.Project.get(project_id)
    models = project.get_models()
    model = models[0]
    blueprint = Blueprint.get(project_id, model.blueprint_id)

Get a blueprint chart
*********************
For all blueprints - either from blueprint menu or already used in model - you can retrieve its
chart. You can also get its representation in graphviz DOT format to render it into the format you need.

.. code-block:: python

    project_id = '5506fcd38bd88f5953219da0'
    blueprint_id = '4321fcd38bd88f595321554223'
    bp_chart = BlueprintChart.get(project_id, blueprint_id)
    print(bp_chart.to_graphviz())

Get a blueprint's documentation
*******************************
You can retrieve documentation on tasks used in the blueprint. It will contain information about
task, its parameters and (when available) links and references to additional sources.
All documents are instances of ``BlueprintTaskDocument`` class.

.. code-block:: python

    project_id = '5506fcd38bd88f5953219da0'
    blueprint_id = '4321fcd38bd88f595321554223'
    bp = Blueprint.get(project_id, blueprint_id)
    docs = bp.get_documents()
    print(docs[0].task)
    >>> Average Blend
    print(docs[0].links[0]['url'])
    >>> https://en.wikipedia.org/wiki/Ensemble_learning

Blueprint Attributes
********************
The ``Blueprint`` class holds the data required to use the blueprint
for modeling. This includes the ``blueprint_id`` and ``project_id``.
There are also two attributes that help distinguish blueprints: ``model_type``
and ``processes``.

.. code-block:: python

    print(blueprint.id)
    >>> u'8956e1aeecffa0fa6db2b84640fb3848'
    print(blueprint.project_id)
    >>> u5506fcd38bd88f5953219da0'
    print(blueprint.model_type)
    >>> Logistic Regression
    print(blueprint.processes)
    >>> [u'One-Hot Encoding',
         u'Missing Values Imputed',
         u'Standardize',
         u'Logistic Regression']

Create a Model from a Blueprint
*******************************
You can use a blueprint instance to train a model. The default dataset for the project is used.
Note that :meth:`Project.train <datarobot.models.Project.train>` is used for non-datetime-partitioned projects.
:meth:`Project.train_datetime <datarobot.models.Project.train_datetime>` should be used for datetime partitioned
projects.

.. code-block:: python

    model_job_id = project.train(blueprint)

    # For datetime partitioned projects
    model_job = project.train_datetime(blueprint.id)

Both :meth:`Project.train <datarobot.models.Project.train>` and :meth:`Project.train_datetime <datarobot.models.Project.train_datetime>`
will put a new modeling job into the queue. However, note that ``Project.train`` returns the id of the created
:doc:`ModelJob <job>`, while ``Project.train_datetime`` returns the ``ModelJob`` object itself.
You can pass a ModelJob id to :ref:`wait_for_async_model_creation <wait_for_async_model_creation-label>` function,
which polls the async model creation status and returns the newly created model when it's finished.
