####
Jobs
####

The :ref:`Job <jobs_api>` class is a generic representation of jobs running
through a project's queue.  Many tasks involved in modeling, such as creating a new model or
computing feature impact for a model, will use a job to track the worker usage and progress of
the associated task.

Checking the Contents of the Queue
**********************************
To see what jobs running or waiting in the queue for a project, use the ``Project.get_all_jobs``
method.

.. code-block:: python

    from datarobot.enums import QUEUE_STATUS

    jobs_list = project.get_all_jobs()  # gives all jobs queued or inprogress
    jobs_by_type = {}
    for job in jobs_list:
        if job.job_type not in jobs_by_type:
            jobs_by_type[job.job_type] = [0, 0]
        if job.status == QUEUE_STATUS.QUEUE:
            jobs_by_type[job.job_type][0] += 1
        else:
            jobs_by_type[job.job_type][1] += 1
    for type in jobs_by_type:
        (num_queued, num_inprogress) = jobs_by_type[type]
        print('{} jobs: {} queued, {} inprogress'.format(type, num_queued, num_inprogress))

Cancelling a Job
****************
If a job is taking too long to run or no longer necessary, it can be cancelled easily from the
``Job`` object.

.. code-block:: python

    from datarobot.enums import QUEUE_STATUS

    project.pause_autopilot()
    bad_jobs = project.get_all_jobs(status=QUEUE_STATUS.QUEUE)
    for job in bad_jobs:
        job.cancel()
    project.unpause_autopilot()

Retrieving Results From a Job
*****************************
Once you've found a particular job of interest, you can retrieve the results once it is complete.
Note that the type of the returned object will vary depending on the ``job_type``.  All return types
are documented in ``Job.get_result``.

.. code-block:: python

    from datarobot.enums import JOB_TYPE

    time_to_wait = 60 * 60  # how long to wait for the job to finish (in seconds) - i.e. an hour
    assert my_job.job_type == JOB_TYPE.MODEL
    my_model = my_job.get_result_when_complete(max_wait=time_to_wait)

Model Jobs
##########

Model creation is an asynchronous process. This means that when explicitly invoking
new model creation (with ``project.train`` or ``model.train`` for example) all you get
is the id of the process, responsible for model creation. With this id you can
get info about the model that is being created or the model itself, when
the creation process is finished. For this you should use
the ``ModelJob`` class.

Get an existing ModelJob
************************

To retrieve existing ModelJob use ``ModelJob.get`` method.
For this you need the id of Project that is used for model
creation and the id of ModelJob. Having ModelJob might be useful if you want to
know parameters of model creation, automatically chosen by the API backend,
before actual model was created.

If model is already created, ``ModelJob.get`` will raise ``PendingJobFinished``
exception

.. code-block:: python

    import time

    import datarobot as dr

    blueprint_id = '5506fcd38bd88f5953219da0'
    model_job_id = project.train(blueprint_id)
    model_job = dr.ModelJob.get(project_id=project.id,
                                model_job_id=model_job_id)
    model_job.sample_pct
    >>> 64.0

    # wait for model to be created (in a very inefficient way)
    time.sleep(10 * 60)
    model_job = dr.ModelJob.get(project_id=project.id,
                                model_job_id=model_job_id)
    >>> datarobot.errors.PendingJobFinished

    # get the job attached to the model
    model_job.model
    >>> Model('5d518cd3962d741512605e2b')

Get a created model
*******************

After model is created, you can use ModelJob.get_model to get newly
created model.

.. code-block:: python

    import datarobot as dr

    model = dr.ModelJob.get_model(project_id=project.id,
                                  model_job_id=model_job_id)

.. _wait_for_async_model_creation-label:

wait_for_async_model_creation function
**************************************
If you just want to get the created model after getting the ModelJob id, you
can use the :ref:`wait_for_async_model_creation<wait_for_async_model_creation-api-label>` function.
It will poll for the status of the model creation process until it's finished, and
then will return the newly created model. Note the differences below between datetime partitioned projects and
non-datetime-partitioned projects.

.. code-block:: python

    from datarobot.models.modeljob import wait_for_async_model_creation

    # used during training based on blueprint
    model_job_id = project.train(blueprint, sample_pct=33)
    new_model = wait_for_async_model_creation(
        project_id=project.id,
        model_job_id=model_job_id,
    )

    # used during training based on existing model
    model_job_id = existing_model.train(sample_pct=33)
    new_model = wait_for_async_model_creation(
        project_id=existing_model.project_id,
        model_job_id=model_job_id,
    )

    # For datetime-partitioned projects, use project.train_datetime. Note that train_datetime returns a ModelJob instead
    # of just an id.
    model_job = project.train_datetime(blueprint)
    new_model = wait_for_async_model_creation(
        project_id=project.id,
        model_job_id=model_job.id
    )
