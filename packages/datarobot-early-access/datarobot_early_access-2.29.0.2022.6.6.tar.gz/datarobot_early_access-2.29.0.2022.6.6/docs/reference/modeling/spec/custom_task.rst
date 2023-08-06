.. _custom-tasks:


#############
Composable ML
#############

Composable ML consists of two major components: `the DataRobot Blueprint Workshop <https://blueprint-workshop.datarobot.com/>`_ and custom tasks, detailed below.

Custom tasks provide users the ability to train models with arbitrary code in an environment defined by the user.

For details on using environments, see: :ref:`custom-models-execution-environments`.

Manage Custom Tasks
*******************

Before you can upload code for a custom task, you need to create the entity that holds all the
metadata.

.. code-block:: python

    import datarobot as dr
    from datarobot.enums import CUSTOM_TASK_TARGET_TYPE

    transform = dr.CustomTask.create(
        name="a convenient display name",  # required
        target_type=CUSTOM_TASK_TARGET_TYPE.TRANSFORM,  # required
        language="python",
        description="a longer description of the task"
    )

    binary = dr.CustomTask.create(
        name="this or that",
        target_type=CUSTOM_TASK_TARGET_TYPE.BINARY,
    )

A task, by itself is an empty metadata container. Before using your tasks, you need create a
:ref:`CustomTaskVersion <custom-task-versions>` associated with it. A task that is ready for use
will have a `latest_version` field populated with this task.

.. code-block:: python

    binary.latest_version
    >>> None

    execution_environment = dr.ExecutionEnvironment.create(
        name="Python3 PyTorch Environment",
        description="This environment contains Python3 pytorch library.",
    )
    custom_task_folder = "datarobot-user-tasks/task_templates/python3_pytorch"
    task_version = dr.CustomTaskVersion.create_clean(
        custom_task_id=binary.id,
        base_environment_id=execution_environment.id,
        folder_path=custom_task_folder,
    )

    binary.refresh()  # In order to see the change, you need to GET it from DataRobot
    binary.latest_version
    >>> CustomTaskVersion('v1.0')

If you create a new version, that will be returned as the `latest_version`. You can
download the latest version as a zip file.

.. code-block:: python

    binary.latest_version
    >>> CustomTaskVersion('v1.0')

    custom_task_folder = "/home/my-user-name/tasks/my-updated-task/"
    task_version = dr.CustomTaskVersion.create_clean(
        custom_task_id=binary.id,
        base_environment_id=execution_environment.id,
        folder_path=custom_task_folder,
    )

    binary.refresh()
    binary.latest_version
    >>> CustomTaskVersion('v2.0')

    binary.download_latest_version("/home/my-user-name/downloads/my-task-files.zip")

You can `get`, `list`, `copy`, exactly as you would expect. `copy` makes a *complete* copy of the
task: new copies of the metadata, new copies of the versions, new copies of uploaded files for the
new versions.

.. code-block:: python

    all_tasks = CustomTask.list()
    assert {el.id for el in all_tasks} == {binary.id, transform.id}

    new_binary = CustomTask.copy(binary.id)
    assert new_binary.latest_version.id != binary.latest_version.id

    original_binary = CustomTask.get(binary.id)

    assert len(CustomTask.list()) == 3

You can `update` the metadata of a task. When you do this, the object is also updated to the latest
data.

.. code-block:: python

    assert binary.description == new_binary.description
    binary.update(description="totally new description")

    assert binary.description != new_binary.description
    assert original_binary.description != binary.description  # hasn't refreshed from the server yet

    original_binary.refresh()
    assert original_binary.description == binary.description

And finally, you can `delete` **only if** the task is not in use by any of the following:

- Trained models
- Deployments
- Blueprints in the AI catalog

Once you have deleted the objects that use the task, you will be able to delete the task itself.


.. _custom-task-versions:

Manage Custom Task Versions
******************************

Code for Custom Tasks can be uploaded by creating a Custom Task Version.
When creating a Custom Task Version, the version must be associated with a base execution
environment.  If the base environment supports additional task dependencies
(R or Python environments) and the Custom Task Version
contains a valid requirements.txt file, the task version will run in an environment based on
the base environment with the additional dependencies installed.

Create Custom Task Version
===========================

Upload actual custom task content by creating a clean Custom Task Version:

.. code-block:: python

    import os

    custom_task_id = binary.id
    custom_task_folder = "datarobot-user-tasks/task_templates/python3_pytorch"

    # add files from the folder to the custom task
    task_version = dr.CustomTaskVersion.create_clean(
        custom_task_id=custom_task_id,
        base_environment_id=execution_environment.id,
        folder_path=custom_task_folder,
    )


To create a new Custom Task Version from a previous one, with just some files added or removed, do the following:

.. code-block:: python

    import os
    import datarobot as dr

    new_files_folder = "datarobot-user-tasks/task_templates/my_files_to_add_to_pytorch_task"

    file_to_delete = task_version.items[0].id

    task_version_2 = dr.CustomTaskVersion.create_from_previous(
        custom_task_id=custom_task_id,
        base_environment_id=execution_environment.id,
        folder_path=new_files_folder,
    )

Please refer to :class:`~datarobot.models.custom_task_version.CustomTaskFileItem` for description of custom task file properties.


List Custom Task Versions
==========================

Use the following command to list Custom Task Versions available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomTaskVersion.list(custom_task_id)

    >>> [CustomTaskVersion('v2.0'), CustomTaskVersion('v1.0')]

Retrieve Custom Task Version
=============================

To retrieve a specific Custom Task Version, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomTaskVersion.get(custom_task_id, custom_task_version_id='5ebe96b84024035cc6a6560b')

    >>> CustomTaskVersion('v2.0')

Update Custom Task Version
===========================

To update Custom Task Version description execute the following:

.. code-block:: python

    import datarobot as dr

    custom_task_version = dr.CustomTaskVersion.get(
        custom_task_id,
        custom_task_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_task_version.update(description='new description')

    custom_task_version.description
    >>> 'new description'

Download Custom Task Version
=============================

Download content of the Custom Task Version as a ZIP archive:

.. code-block:: python

    import datarobot as dr

    path_to_download = '/home/user/Documents/myTask.zip'

    custom_task_version = dr.CustomTaskVersion.get(
        custom_task_id,
        custom_task_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_task_version.download(path_to_download)


Preparing a Custom Task Version for Use
****************************************

If your custom task version has dependencies, a dependency build must be completed before the task
can be used.  The dependency build installs your task's dependencies into the base environment
associated with the task version.

see: :ref:`custom-models-dependencies`
