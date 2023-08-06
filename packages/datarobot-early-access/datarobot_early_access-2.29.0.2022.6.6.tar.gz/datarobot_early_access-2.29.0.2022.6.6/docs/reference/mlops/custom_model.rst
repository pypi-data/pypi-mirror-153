.. _custom_models:

#############
Custom Models
#############

Custom models provide users the ability to run arbitrary modeling code in an environment defined by the user.

.. _custom-models-execution-environments:

Manage Execution Environments
*****************************

Execution Environment defines the runtime environment for custom models.
Execution Environment Version is a revision of Execution Environment with an actual runtime definition.
Please refer to DataRobot User Models (https://github.com/datarobot/datarobot-user-models) for sample
environments.

Create Execution Environment
===============================

To create an Execution Environment run:

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.create(
        name="Python3 PyTorch Environment",
        description="This environment contains Python3 pytorch library.",
    )

    execution_environment.id
    >>> '5b6b2315ca36c0108fc5d41b'

There are 2 ways to create an Execution Environment Version: synchronous and asynchronous.

Synchronous way means that program execution will be blocked until an Execution Environment Version
creation process is finished with either success or failure:

.. code-block:: python

    import datarobot as dr

    # use execution_environment created earlier

    environment_version = dr.ExecutionEnvironmentVersion.create(
        execution_environment.id,
        docker_context_path="datarobot-user-models/public_dropin_environments/python3_pytorch",
        max_wait=3600,  # 1 hour timeout
    )

    environment_version.id
    >>> '5eb538959bc057003b487b2d'
    environment_version.build_status
    >>> 'success'

Asynchronous way means that program execution will be not blocked, but an Execution Environment Version
created will not be ready to be used for some time, until its creation process is finished.
In such case, it will be required to manually call :meth:`~datarobot.ExecutionEnvironmentVersion.refresh`
for the Execution Environment Version and check if its `build_status` is "success".
To create an Execution Environment Version without blocking a program, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    # use execution_environment created earlier

    environment_version = dr.ExecutionEnvironmentVersion.create(
        execution_environment.id,
        docker_context_path="datarobot-user-models/public_dropin_environments/python3_pytorch",
        max_wait=None,  # set None to not block execution on this method
    )

    environment_version.id
    >>> '5eb538959bc057003b487b2d'
    environment_version.build_status
    >>> 'processing'

    # after some time
    environment_version.refresh()
    environment_version.build_status
    >>> 'success'

If your environment requires additional metadata to be supplied for models using it, you can create an
environment with additional metadata keys. Custom model versions that use this environment must specify
values for these keys before they can be used to run tests or make deployments.  The values will be baked in
as environment variables with field_name as the environment variable name.

.. code-block:: python

    import datarobot as dr
    from datarobot.models.execution_environment import RequiredMetadataKey

    execution_environment = dr.ExecutionEnvironment.create(
        name="Python3 PyTorch Environment",
        description="This environment contains Python3 pytorch library.",
        required_metadata_keys=[
            RequiredMetadataKey(field_name="MY_VAR", display_name="A value needed by hte environment")
        ],
    )

    model_version = dr.CustomModelVersion.create_clean(
        custom_model_id=custom_model.id,
        base_environment_id=execution_environment.id,
        folder_path=custom_model_folder,
        required_metadata={"MY_VAR": "a value"}
    )

List Execution Environments
===========================

Use the following command to list execution environments available to the user.

.. code-block:: python

    import datarobot as dr

    execution_environments = dr.ExecutionEnvironment.list()
    execution_environments
    >>> [ExecutionEnvironment('[DataRobot] Python 3 PyTorch Drop-In'), ExecutionEnvironment('[DataRobot] Java Drop-In')]

    environment_versions = dr.ExecutionEnvironmentVersion.list(execution_environment.id)
    environment_versions
    >>> [ExecutionEnvironmentVersion('v1')]

Refer to :class:`~datarobot.ExecutionEnvironment` for properties of the execution environment object and
:class:`~datarobot.ExecutionEnvironmentVersion` for properties of the execution environment object version.

You can also filter the execution environments that are returned by passing a string as `search_for` parameter -
only the execution environments that contain the passed string in name or description will be returned.

.. code-block:: python

    import datarobot as dr

    execution_environments = dr.ExecutionEnvironment.list(search_for='java')
    execution_environments
    >>> [ExecutionEnvironment('[DataRobot] Java Drop-In')]

Execution environment versions can be filtered by build status.

.. code-block:: python

    import datarobot as dr

    environment_versions = dr.ExecutionEnvironmentVersion.list(
        execution_environment.id, dr.EXECUTION_ENVIRONMENT_VERSION_BUILD_STATUS.PROCESSING
    )
    environment_versions
    >>> [ExecutionEnvironmentVersion('v1')]

Retrieve Execution Environment
=================================

To retrieve an execution environment and an execution environment version by identifier,
rather than list all available ones, do the following:

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.get(execution_environment_id='5506fcd38bd88f5953219da0')
    execution_environment
    >>> ExecutionEnvironment('[DataRobot] Python 3 PyTorch Drop-In')

    environment_version = dr.ExecutionEnvironmentVersion.get(
        execution_environment_id=execution_environment.id, version_id='5eb538959bc057003b487b2d')
    environment_version
    >>> ExecutionEnvironmentVersion('v1')

Update Execution Environment
===============================

To update name and/or description of the execution environment run:

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.get(execution_environment_id='5506fcd38bd88f5953219da0')
    execution_environment.update(name='new name', description='new description')

Delete Execution Environment
===============================

To delete the execution environment and execution environment version, use the following commands.

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.get(execution_environment_id='5506fcd38bd88f5953219da0')
    execution_environment.delete()

Get Execution Environment build log
======================================

To get execution environment version build log run:

.. code-block:: python

    import datarobot as dr

    environment_version = dr.ExecutionEnvironmentVersion.get(
        execution_environment_id='5506fcd38bd88f5953219da0', version_id='5eb538959bc057003b487b2d')
    log, error = environment_version.get_build_log()

Manage Custom Models
********************

Custom Inference Model is user-defined modeling code that supports making predictions against it.
Custom Inference Model supports regression and binary classification target types.

To upload actual modeling code Custom Model Version must be created for a custom model.
Please see :ref:`Custom Model Version documentation <custom_model_versions>`.

Create Custom Inference Model
=============================

To create a regression Custom Inference Model run:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.REGRESSION,
        target_name='MEDV',
        description='This is a Python3-based custom model. It has a simple PyTorch model built on boston housing',
        language='python'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

When creating a binary classification Custom Inference Model,
`positive_class_label` and `negative_class_label` must be set:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.BINARY,
        target_name='readmitted',
        positive_class_label='False',
        negative_class_label='True',
        description='This is a Python3-based custom model. It has a simple PyTorch model built on 10k_diabetes dataset',
        language='Python 3'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

When creating a multiclass classification Custom Inference Model,
`class_labels` must be provided:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.MULTICLASS,
        target_name='readmitted',
        class_labels=['hot dog', 'burrito', 'hoagie', 'reuben'],
        description='This is a Python3-based custom model. It has a simple PyTorch model built on sandwich dataset',
        language='Python 3'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

For convenience when there are many class labels, multiclass labels can also be provided as a file.
The file should have all the class labels separated by newline:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.MULTICLASS,
        target_name='readmitted',
        class_labels_file='/path/to/classlabels.txt',
        description='This is a Python3-based custom model. It has a simple PyTorch model built on sandwich dataset',
        language='Python 3'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

For unstructured model `target_name` parameter is optional and is ignored if provided.
To create an unstructured Custom Inference Model run:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 Unstructured Custom Model',
        target_type=dr.TARGET_TYPE.UNSTRUCTURED,
        description='This is a Python3-based unstructured model',
        language='python'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

For anomaly detection models, the `target_name` parameter is also optional and is ignored if provided.
To create an anomaly Custom Inference Model run:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 Unstructured Custom Model',
        target_type=dr.TARGET_TYPE.ANOMALY,
        description='This is a Python3-based anomaly detection model',
        language='python'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

To create a Custom Inference Model with specific k8s resources:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.BINARY,
        target_name='readmitted',
        positive_class_label='False',
        negative_class_label='True',
        description='This is a Python3-based custom model. It has a simple PyTorch model built on 10k_diabetes dataset',
        language='Python 3',
        maximum_memory=512*1024*1024,
    )

Custom Inference Model k8s resources are optional and unless specifically provided, the configured defaults
will be used.

List Custom Inference Models
============================

Use the following command to list Custom Inference Models available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomInferenceModel.list()
    >>> [CustomInferenceModel('my model 2'), CustomInferenceModel('my model 1')]

    # use these parameters to filter results:
    dr.CustomInferenceModel.list(
        is_deployed=True,  # set to return only deployed models
        order_by='-updated',  # set to define order of returned results
        search_for='model 1',  # return only models containing 'model 1' in name or description
    )
    >>> CustomInferenceModel('my model 1')

Please refer to :meth:`~datarobot.CustomInferenceModel.list` for detailed parameter description.

Retrieve Custom Inference Model
===============================

To retrieve a specific Custom Inference Model, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomInferenceModel.get('5ebe95044024035cc6a65602')
    >>> CustomInferenceModel('my model 1')

Update Custom Model
===================

To update Custom Inference Model properties execute the following:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.get('5ebe95044024035cc6a65602')

    custom_model.update(
        name='new name',
        description='new description',
    )

Please, refer to :meth:`~datarobot.CustomInferenceModel.update` for the full list of properties that can be updated.

Download latest revision of Custom Inference Model
==================================================

To download content of the latest Custom Model Version of `CustomInferenceModel` as a ZIP archive:

.. code-block:: python

    import datarobot as dr

    path_to_download = '/home/user/Documents/myModel.zip'

    custom_model = dr.CustomInferenceModel.get('5ebe96b84024035cc6a6560b')

    custom_model.download_latest_version(path_to_download)

.. _custom_inference_model_assign_data:

Assign training data to Custom Inference Model
==============================================

To assign training data to Custom Inference Model, run:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/trainingDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model = dr.CustomInferenceModel.get('5ebe96b84024035cc6a6560b')

    custom_model.assign_training_data(dataset.id)

To assign training data without blocking a program, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/trainingDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model = dr.CustomInferenceModel.get('5ebe96b84024035cc6a6560b')

    custom_model.assign_training_data(
        dataset.id,
        max_wait=None
    )

    custom_model.training_data_assignment_in_progress
    >>> True

    # after some time
    custom_model.refresh()
    custom_model.training_data_assignment_in_progress
    >>> False

Note: training data must be assigned to retrieve feature impact from Custom Model Version.
Please see to :ref:`Custom Model Version documentation <custom_model_version_feature_impact>`.

.. _custom_model_versions:

Manage Custom Model Versions
******************************

Modeling code for Custom Inference Models can be uploaded by creating a Custom Model Version.
When creating a Custom Model Version, the version must be associated with a base execution
environment.  If the base environment supports additional model dependencies
(R or Python environments) and the Custom Model Version
contains a valid requirements.txt file, the model version will run in an environment based on
the base environment with the additional dependencies installed.

Create Custom Model Version
===========================

Upload actual custom model content by creating a clean Custom Model Version:

.. code-block:: python

    import os
    import datarobot as dr

    custom_model_folder = "datarobot-user-models/model_templates/python3_pytorch"

    # add files from the folder to the custom model
    model_version = dr.CustomModelVersion.create_clean(
        custom_model_id=custom_model.id,
        base_environment_id=execution_environment.id,
        folder_path=custom_model_folder,
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

    # or add a list of files to the custom model
    model_version_2 = dr.CustomModelVersion.create_clean(
        custom_model_id=custom_model.id,
        files=[(os.path.join(custom_model_folder, 'custom.py'), 'custom.py')],
    )

    # and/or set k8s resources to the custom model
    model_version_3 = dr.CustomModelVersion.create_clean(
        custom_model_id=custom_model.id,
        files=[(os.path.join(custom_model_folder, 'custom.py'), 'custom.py')],
        network_egress_policy=dr.NETWORK_EGRESS_POLICY.PUBLIC,
        maximum_memory=512*1024*1024,
        replicas=1,
    )

To create a new Custom Model Version from a previous one, with just some files added or removed, do the following:

.. code-block:: python

    import os
    import datarobot as dr

    custom_model_folder = "datarobot-user-models/model_templates/python3_pytorch"

    file_to_delete = model_version_2.items[0].id

    model_version_3 = dr.CustomModelVersion.create_from_previous(
        custom_model_id=custom_model.id,
        base_environment_id=execution_environment.id,
        files=[(os.path.join(custom_model_folder, 'custom.py'), 'custom.py')],
        files_to_delete=[file_to_delete],
    )

Please refer to :class:`~datarobot.models.custom_model_version.CustomModelFileItem` for description of custom model file properties.

To create a new Custom Model Version from a previous one, with just new k8s resources values, do the following:

.. code-block:: python

    import os
    import datarobot as dr

    custom_model_folder = "datarobot-user-models/model_templates/python3_pytorch"

    file_to_delete = model_version_2.items[0].id

    model_version_3 = dr.CustomModelVersion.create_from_previous(
        custom_model_id=custom_model.id,
        base_environment_id=execution_environment.id,
        maximum_memory=1024*1024*1024,
    )


List Custom Model Versions
==========================

Use the following command to list Custom Model Versions available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelVersion.list(custom_model.id)

    >>> [CustomModelVersion('v2.0'), CustomModelVersion('v1.0')]

Retrieve Custom Model Version
=============================

To retrieve a specific Custom Model Version, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelVersion.get(custom_model.id, custom_model_version_id='5ebe96b84024035cc6a6560b')

    >>> CustomModelVersion('v2.0')

Update Custom Model Version
===========================

To update Custom Model Version description execute the following:

.. code-block:: python

    import datarobot as dr

    custom_model_version = dr.CustomModelVersion.get(
        custom_model.id,
        custom_model_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_model_version.update(description='new description')

    custom_model_version.description
    >>> 'new description'

Download Custom Model Version
=============================

Download content of the Custom Model Version as a ZIP archive:

.. code-block:: python

    import datarobot as dr

    path_to_download = '/home/user/Documents/myModel.zip'

    custom_model_version = dr.CustomModelVersion.get(
        custom_model.id,
        custom_model_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_model_version.download(path_to_download)


.. _custom_model_version_calculate_feature_impact:

Calculate Custom ModelVersion feature impact
===============================================

To trigger calculation of Custom Model Version feature impact, training data must be assigned to a Custom Inference Model.
Please refer to :ref:`Custom Inference Model documentation <custom_inference_model_assign_data>`.
If training data is assigned, run the following to trigger the calculation of the feature impact:

.. code-block:: python

    import datarobot as dr

    version = dr.CustomModelVersion.get(custom_model.id, custom_model_version_id='5ebe96b84024035cc6a6560b')

    version.calculate_feature_impact()

To trigger calculating feature impact without blocking a program, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    version = dr.CustomModelVersion.get(custom_model.id, custom_model_version_id='5ebe96b84024035cc6a6560b')

    version.calculate_feature_impact(max_wait=None)


.. _custom_model_version_feature_impact:

Retrieve Custom Inference Image feature impact
==============================================

To retrieve Custom Model Version feature impact, it must be calculated beforehand.
Please refer to :ref:`Custom Inference Image feature impact documentation <custom_model_version_calculate_feature_impact>`.
Run the following to get feature impact:

.. code-block:: python

    import datarobot as dr

    version = dr.CustomModelVersion.get(custom_model.id, custom_model_version_id='5ebe96b84024035cc6a6560b')

    version.get_feature_impact()
    >>> [{'featureName': 'B', 'impactNormalized': 1.0, 'impactUnnormalized': 1.1085356209402688, 'redundantWith': 'B'}...]


.. _custom-models-dependencies:

Preparing a Custom Model Version for Use
****************************************

If your custom model version has dependencies, a dependency build must be completed before the model
can be used.  The dependency build installs your model's dependencies into the base environment
associated with the model version.

Starting the Dependency Build
=============================

To start the Custom Model Version Dependency Build, run:

.. code-block:: python

    import datarobot as dr

    build_info = dr.CustomModelVersionDependencyBuild.start_build(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        max_wait=3600,  # 1 hour timeout
    )

    build_info.build_status
    >>> 'success'

To start Custom Model Version Dependency Build without blocking a program until the test finishes,
set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    build_info = dr.CustomModelVersionDependencyBuild.start_build(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        max_wait=None,
    )

    build_info.build_status
    >>> 'submitted'

    # after some time
    build_info.refresh()
    build_info.build_status
    >>> 'success'

In case the build fails, or you are just curious, do the following to retrieve the build log once complete:

.. code-block:: python

    print(build_info.get_log())

To cancel a Custom Model Version Dependency Build, simply run:

.. code-block:: python

    build_info.cancel()


Manage Custom Model Tests
*************************

A Custom Model Test represents testing performed on custom models.

Create Custom Model Test
========================

To create Custom Model Test, run:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/testDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        dataset_id=dataset.id,
        max_wait=3600,  # 1 hour timeout
    )

    custom_model_test.overall_status
    >>> 'succeeded'

or, with k8s resources:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/testDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        dataset_id=dataset.id,
        max_wait=3600,  # 1 hour timeout
        maximum_memory=1024*1024*1024,
    )

    custom_model_test.overall_status
    >>> 'succeeded'

To start Custom Model Test without blocking a program until the test finishes, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/testDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        environment_id=execution_environment.id,
        environment_version_id=environment_version.id,
        dataset_id=dataset.id,
        max_wait=None,
    )

    custom_model_test.overall_status
    >>> 'in_progress'

    # after some time
    custom_model_test.refresh()
    custom_model_test.overall_status
    >>> 'succeeded'

Running a Custom Model Test uses the Custom Model Version's base image with its dependencies installed as an execution
environment. To start Custom Model Test using an execution environment "as-is", without the model's
dependencies installed, supply an environment ID and (optionally) and environment version ID:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/testDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        environment_id=execution_environment.id,
        environment_version_id=environment_version.id,
        dataset_id=dataset.id,
        max_wait=3600,  # 1 hour timeout
    )

    custom_model_test.overall_status
    >>> 'succeeded'

In case a test fails, do the following to examine details of the failure:

.. code-block:: python

    for name, test in custom_model_test.detailed_status.items():
        print('Test: {}'.format(name))
        print('Status: {}'.format(test['status']))
        print('Message: {}'.format(test['message']))

    print(custom_model_test.get_log())


To cancel a Custom Model Test, simply run:

.. code-block:: python

    custom_model_test.cancel()


To start Custom Model Test for an unstructured custom model, dataset details should not be provided:

.. code-block:: python

    import datarobot as dr

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
    )


List Custom Model Tests
=======================

Use the following command to list Custom Model Tests available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelTest.list(custom_model_id=custom_model.id)
    >>> [CustomModelTest('5ec262604024031bed5aaa16')]

Retrieve Custom Model Test
===========================

To retrieve a specific Custom Model Test, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelTest.get(custom_model_test_id='5ec262604024031bed5aaa16')
    >>> CustomModelTest('5ec262604024031bed5aaa16')

