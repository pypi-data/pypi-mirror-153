###############
DataRobot Prime
###############

DataRobot Prime allows the download of executable code approximating models. For more information about this feature, see the documentation within the
DataRobot webapp. Contact your Account Executive or CFDS for information on enabling DataRobot Prime, if needed.

Approximate a Model
*******************
Given a Model you wish to approximate, ``Model.request_approximation`` will start a job creating
several ``Ruleset`` objects approximating the parent model.  Each of those rulesets will identify
how many rules were used to approximate the model, as well as the validation score
the approximation achieved.

.. code-block:: python

    rulesets_job = model.request_approximation()
    rulesets = rulesets_job.get_result_when_complete()
    for ruleset in rulesets:
        info = (ruleset.id, ruleset.rule_count, ruleset.score)
        print('id: {}, rule_count: {}, score: {}'.format(*info))

Prime Models vs. Models
***********************
Given a ruleset, you can create a model based on that ruleset.  We consider such models to be Prime
models.  The ``PrimeModel`` class inherits from the ``Model`` class, so anything a Model can do,
as PrimeModel can do as well.

The ``PrimeModel`` objects available within a ``Project`` can be listed by
``project.get_prime_models``, or a particular one can be retrieve via ``PrimeModel.get``.  If a
ruleset has not yet had a model built for it, ``ruleset.request_model`` can be used to start
a job to make a PrimeModel using a particular ruleset.

.. code-block:: python

    rulesets = parent_model.get_rulesets()
    selected_ruleset = sorted(rulesets, key=lambda x: x.score)[-1]
    if selected_ruleset.model_id:
        prime_model = PrimeModel.get(selected_ruleset.project_id, selected_ruleset.model_id)
    else:
        prime_job = selected_ruleset.request_model()
        prime_model = prime_job.get_result_when_complete()

The ``PrimeModel`` class has two additional attributes and one additional method.  The attributes
are ``ruleset``, which is the Ruleset used in the PrimeModel, and ``parent_model_id`` which is
the id of the model it approximates.

Finally, the new method defined is ``request_download_validation`` which is used to prepare code
download for the model and is discussed later on in this document.

Retrieving Code from a PrimeModel
*********************************
Given a PrimeModel, you can download the code used to approximate the parent model, and view
and execute it locally.

The first step is to validate the PrimeModel, which runs some basic validation of the generated
code, as well as preparing it for download.  We use the ``PrimeFile`` object to represent code
that is ready to download.  ``PrimeFiles`` can be prepared by the ``request_download_validation``
method on ``PrimeModel`` objects, and listed from a project with the ``get_prime_files`` method.

Once you have a ``PrimeFile`` you can check the ``is_valid`` attribute to verify the code passed
basic validation, and then download it to a local file with ``download``.

.. code-block:: python

    validation_job = prime_model.request_download_validation(enums.PRIME_LANGUAGE.PYTHON)
    prime_file = validation_job.get_result_when_complete()
    if not prime_file.is_valid:
        raise ValueError('File was not valid')
    prime_file.download('/home/myuser/drCode/primeModelCode.py')
