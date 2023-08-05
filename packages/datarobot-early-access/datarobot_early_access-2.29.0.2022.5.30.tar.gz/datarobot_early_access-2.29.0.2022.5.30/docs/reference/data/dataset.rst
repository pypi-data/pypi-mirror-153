.. _datasets:

########
Datasets
########

Before training any models or creating any projects, you need to upload your data into a Dataset.

Creating A Dataset
******************

There are several ways to create a Dataset.
:meth:`Dataset.create_from_file<datarobot.Dataset.create_from_file>` can take either a path to a
local file or any stream-able file object.

.. code-block:: python

    >>> import datarobot as dr
    >>> dataset = dr.Dataset.create_from_file(file_path='data_dir/my_data.csv')
    >>> with open('data_dir/my_data.csv', 'rb') as f:
    ...     other_dataset = dr.Dataset.create_from_file(filelike=f)


:meth:`Dataset.create_from_in_memory_data<datarobot.Dataset.create_from_in_memory_data>` can take
either a ``pandas.Dataframe`` or a list of dictionaries representing rows of data.  Note that the
dictionaries representing the rows of data must contain the same keys.

.. code-block:: python

    >>> import pandas as pd
    >>> data_frame = pd.read_csv('data_dir/my_data.csv')

    # do things to my data_frame
    >>> pandas_dataset = dr.Dataset.create_from_in_memory_data(data_frame=data_frame)

    >>> in_memory_data = [{'key1': 'value', 'key2': 'other_value', ...},
    ...                   {'key1': 'new_value', 'key2': 'other_new_value', ...}, ...]
    >>> in_memory_dataset = dr.Dataset.create_from_in_memory_data(records=other_data)

:meth:`Dataset.create_from_url<datarobot.Dataset.create_from_url>` takes csv data from a URL. If you
have set ``DISABLE_CREATE_SNAPSHOT_DATASOURCE``, you must set ``do_snapshot=False``.

.. code-block:: python

    >>> url_dataset = dr.Dataset.create_from_url('https://s3.amazonaws.com/my_data/my_dataset.csv',
    ...                                          do_snapshot=False)

:meth:`Dataset.create_from_data_source<datarobot.Dataset.create_from_data_source>` takes data
from a data source.
If you have set ``DISABLE_CREATE_SNAPSHOT_DATASOURCE``, you must set ``do_snapshot=False``.

.. code-block:: python

    >>> data_source_dataset = dr.Dataset.create_from_data_source(data_source.id, do_snapshot=False)

or

.. code-block:: python

    >>> data_source_dataset = data_source.create_dataset(do_snapshot=False)


Using Datasets
==============

Once a Dataset is created, you can create :ref:`projects` from it and then begin training on
the projects. (You can also combine the creation of a project and the uploading of a Dataset in a
single step in :meth:`Project.create<datarobot.models.Project.create>`.
However, this means the data is only accessible to the project which created it.)

.. code-block:: python

    >>> project = dataset.create_project(project_name='New Project')
    >>> project.set_target('some target')
    Project(New Project)

Getting Information From A Dataset
**********************************

The dataset object contains some basic information:

.. code-block:: python

    >>> dataset.id
    u'5e31cdac39782d0f65842518'
    >>> dataset.name
    u'my_data.csv'
    >>> dataset.categories
     ["TRAINING", "PREDICTION"]
    >>> dataset.created_at
    datetime.datetime(2020, 2, 7, 16, 51, 10, 311000, tzinfo=tzutc())

There are several methods to get details from a Dataset.

.. code-block:: python

    # Details
    >>> details = dataset.get_details()
    >>> details.last_modification_date
    datetime.datetime(2020, 2, 7, 16, 51, 10, 311000, tzinfo=tzutc())
    >>> details.feature_count_by_type
    [FeatureTypeCount(count=1, feature_type=u'Text'),
     FeatureTypeCount(count=1, feature_type=u'Boolean'),
     FeatureTypeCount(count=16, feature_type=u'Numeric'),
     FeatureTypeCount(count=3, feature_type=u'Categorical')]
    >>> details.to_dataset().id == details.dataset_id
    True

    # Projects
    >>> dr.Project.create_from_dataset(dataset.id, project_name='Project One')
    Project(Project One)
    >>> dr.Project.create_from_dataset(dataset.id, project_name='Project Two')
    Project(Project Two)
    >>> dataset.get_projects()
    [ProjectLocation(url=u'https://app.datarobot.com/api/v2/projects/5e3c94aff86f2d10692497b5/', id=u'5e3c94aff86f2d10692497b5'),
     ProjectLocation(url=u'https://app.datarobot.com/api/v2/projects/5e3c94eb9525d010a9918ec1/', id=u'5e3c94eb9525d010a9918ec1')]
    >>> first_id = dataset.get_projects()[0].id
    >>> dr.Project.get(first_id).project_name
    'Project One'

    # Features
    >>> all_features = dataset.get_all_features()
    >>> feature = next(dataset.iterate_all_features(offset=2, limit=1))
    >>> feature.name == all_features[2].name
    True
    >>> print(feature.name, feature.feature_type, feature.dataset_id)
    (u'Partition', u'Numeric', u'5e31cdac39782d0f65842518')
    >>> feature.get_histogram().plot
    [{'count': 3522, 'target': None, 'label': u'0.0'},
     {'count': 3521, 'target': None, 'label': u'1.0'}, ... ]

    # The raw data
    >>> with open('myfile.csv', 'wb') as f:
    ...     dataset.get_file(filelike=f)


Retrieving Datasets
*******************

You can retrieve either specific datasets, the list of all datasets or an iterator that can get
all or some of the datasets.

.. code-block:: python

    >>> dataset_id = '5e387c501a438646ed7bf0f2'
    >>> dataset = dr.Dataset.get(dataset_id)
    >>> dataset.id == dataset_id
    True
    # a blocking call that returns all datasets
    >>> dr.Dataset.list()
    [Dataset(name=u'Untitled Dataset', id=u'5e3c51e0f86f2d1087249728'),
     Dataset(name=u'my_data.csv', id=u'5e3c2028162e6a5fe9a0d678'), ...]

    # avoid listing Datasets that failed to properly upload
    >>> dr.Dataset.list(filter_failed=True)
    [Dataset(name=u'my_data.csv', id=u'5e3c2028162e6a5fe9a0d678'),
     Dataset(name=u'my_other_data.csv', id=u'3efc2428g62eaa5f39a6dg7a'), ...]

    # an iterator that lazily retrieves from the server page-by-page
    >>> from itertools import islice
    >>> iterator = dr.Dataset.iterate(offset=2)
    >>> for element in islice(iterator, 3):
    ...    print(element)
    Dataset(name='some_data.csv', id='5e8df2f21a438656e7a23d12')
    Dataset(name='other_data.csv', id='5e8df2e31a438656e7a23d0b')
    Dataset(name='Untitled Dataset', id='5e6127681a438666cc73c2b0')


Managing Datasets
*****************
You can modify, delete and un_delete datasets.  Note that you need the dataset's ID in order to un_delete
it and if you do not keep track of this it will be gone.  If your deleted dataset had been used
to create a project, that project can still access it, but you will not be able to create
new projects using that dataset.

.. code-block:: python

    >>> dataset.modify(name='A Better Name')
    >>> dataset.name
    'A Better Name'

    >>> new_project = dr.Project.create_from_dataset(dataset.id)
    >>> stored_id = dataset.id
    >>> dr.Dataset.delete(dataset.id)

    # new_project is still ok
    >>> dr.Project.create_from_dataset(stored_id)
    Traceback (most recent call last):
     ...
    datarobot.errors.ClientError: 410 client error: {u'message': u'Requested Dataset 5e31cdac39782d0f65842518 was previously deleted.'}

    >>> dr.Dataset.un_delete(stored_id)
    >>> dr.Project.create_from_dataset(stored_id, project_name='Successful')
    Project(Successful)


Managing Dataset Featurelists
*****************************
You can create, modify, and delete custom featurelists on a given dataset. Some featurelists are
automatically created by DataRobot and can not be modified or deleted. There is no option to
un_delete a deleted featurelist.

.. code-block:: python

    >>> dataset.get_featurelists()
    [DatasetFeaturelist(Raw Features),
     DatasetFeaturelist(universe),
     DatasetFeaturelist(Informative Features)]

    >>> dataset_features = [feature.name for feature in dataset.get_all_features()]
    >>> custom_featurelist = dataset.create_featurelist('Custom Features', dataset_features[:5])
    >>> custom_featurelist
    DatasetFeaturelist(Custom Features)

    >>> dataset.get_featurelists()
    [DatasetFeaturelist(Raw Features),
     DatasetFeaturelist(universe),
     DatasetFeaturelist(Informative Features),
     DatasetFeaturelist(Custom Features)]

    >>> custom_featurelist.update('New Name')
    >>> custom_featurelist.name
    'New Name'

    >>> custom_featurelist.delete()
    >>> dataset.get_featurelists()
    [DatasetFeaturelist(Raw Features),
     DatasetFeaturelist(universe),
     DatasetFeaturelist(Informative Features)]


Using Credential Data
=====================

For methods that accept credential data instead of user/password or credential ID, please see :ref:`Credential Data <credential_data>`.
