.. _feature_discovery:

#################
Feature Discovery
#################
The Feature Discovery Project allows the user to generate features automatically
from the secondary datasets which is connect to the Primary dataset(Training dataset).
User can create such connection using Relationships Configuration.

Register Primary Dataset to start Project
*****************************************
To start the Feature Discovery Project you need to upload the primary (training) dataset
:ref:`projects`

.. code-block:: python

    import datarobot as dr
    primary_dataset = dr.Dataset.create_from_file(file_path='your-training_file.csv')
    project = dr.Project.create_from_dataset(primary_dataset.id, project_name='Lending Club')

Now, register all the secondary datasets which you want to connect with primary (training) dataset
and among themselves.

Register Secondary Dataset(s) in AI Catalog
*******************************************
You can register the dataset using
:meth:`Dataset.create_from_file<datarobot.Dataset.create_from_file>` which can take either a path to a
local file or any stream-able file object.

.. code-block:: python

    profile_dataset = dr.Dataset.create_from_file(file_path='your_profile_file.csv')
    transaction_dataset = dr.Dataset.create_from_file(file_path='your_transaction_file.csv')

Create Dataset Definitions and Relationships using helper functions
*******************************************************************

Create the :ref:`DatasetDefinition <dataset_definition>` and :ref:`Relationship <relationship>` for the profile and transaction dataset created above using helper functions.

.. code-block:: python

    profile_catalog_id = profile_dataset.id
    profile_catalog_version_id = profile_dataset.version_id

    transac_catalog_id = transaction_dataset.id
    transac_catalog_version_id = transaction_dataset.version_id

    profile_dataset_definition = dr.DatasetDefinition(
        identifier='profile',
        catalog_id=profile_catalog_id,
        catalog_version_id=profile_catalog_version_id
    )

    transaction_dataset_definition = dr.DatasetDefinition(
        identifier='transaction',
        catalog_id=transac_catalog_id,
        catalog_version_id=transac_catalog_version_id,
        primary_temporal_key='Date'
    )

    profile_transaction_relationship = dr.Relationship(
        dataset1_identifier='profile',
        dataset2_identifier='transaction',
        dataset1_keys=['CustomerID'],
        dataset2_keys=['CustomerID']
    )

    primary_profile_relationship = dr.Relationship(
        dataset2_identifier='profile',
        dataset1_keys=['CustomerID'],
        dataset2_keys=['CustomerID'],
        feature_derivation_window_start=-14,
        feature_derivation_window_end=-1,
        feature_derivation_window_time_unit='DAY',
        prediction_point_rounding=1,
        prediction_point_rounding_time_unit='DAY'
    )

    dataset_definitions = [profile_dataset_definition, transaction_dataset_definition]
    relationships = [primary_profile_relationship, profile_transaction_relationship]

Create Relationships Configuration
**********************************

Create the Relationship Configuration using dataset definitions and relationships created above


.. code-block:: python

    # Create the relationships configuration to define connection between the datasets
    relationship_config = dr.RelationshipsConfiguration.create(dataset_definitions=dataset_definitions, relationships=relationships)


Create Feature Discovery Project
********************************

Once done with relationships configuration you can start the Feature Discovery project

.. code-block:: python

    # Set the date-time partition column which is date here
    partitioning_spec = dr.DatetimePartitioningSpecification('date')

    # Set the target for the project and start Feature discovery
    project.set_target(target='BadLoan', relationships_configuration_id=relationship_config.id, mode='manual', partitioning_method=partitioning_spec)
    Project(train.csv)


Start Training a Model
**********************

To start training a model, reference the modeling documentation.

Create Secondary Datasets Configuration for prediction
******************************************************

Create the Secondary dataset configuration using :ref:`Secondary Dataset <secondary_dataset>`


.. code-block:: python

    new_secondary_dataset_config = dr.SecondaryDatasetConfigurations.create(
        project_id=project.id,
        name='My config',
        secondary_datasets=secondary_datasets
    )

* For more details, reference the :ref:`Secondary Dataset <secondary_dataset>` Configuration docs.

Perform Prediction over trained model
*************************************
To start prediction over a trained model, refer to the `Predictions documentation <https://docs.datarobot.com/en/docs/predictions/index.html>`_.

.. code-block:: python

    dataset_from_path = project.upload_dataset(
        './data_to_predict.csv',
        secondary_datasets_config_id=new_secondary_dataset_config.id
    )

    predict_job_1 = model.request_predictions(dataset_from_path.id)

Common Errors
-------------
Dataset registration Failed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    datasetdr.Dataset.create_from_file(file_path='file.csv')
    datarobot.errors.AsyncProcessUnsuccessfulError: The job did not complete successfully.

Solution

* Check the internet connectivity sometimes network flakiness cause upload error
* Is the dataset file too big then you might want to upload using URL rather than file


Creating relationships configuration throws some error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    datarobot.errors.ClientError: 422 client error: {u'message': u'Invalid field data',
    u'errors': {u'datasetDefinitions': {u'1': {u'identifier': u'value cannot contain characters: $ - " . { } / \\'},
    u'0': {u'identifier': u'value cannot contain characters: $ - " . { } / \\'}}}}

Solution:

* Check the identifier name passed in datasets_definitions and relationships
* ``Pro tip: Dont use name of the dataset if you didnt specified the name of the dataset explicitly while registration``

.. code-block:: python

    datarobot.errors.ClientError: 422 client error: {u'message': u'Invalid field data',
    u'errors': {u'datasetDefinitions': {u'1': {u'primaryTemporalKey': u'date column doesnt exist'},
    }}}

Solution:

* Check if the name of the column passed as primaryTemporalKey is correct, it is case-senstive.

.. _relationships_configuration:

Configure Relationships
***********************
A Relationships configuration specifies specifies additional datasets to be included to a project
and how these datasets are related to each other, and the primary dataset.
When a relationships configuration is specified for a project,
Feature Discovery will create features automatically from these datasets.

You can create a relationships configuration from the uploaded catalog items.
After uploading all the secondary datasets in the AI Catalog

- Create the datasets definiton to define which datasets to be used as secondary datasets along with its details
- Create the relationships among the above datasets

.. code-block:: python

    relationship_config = dr.RelationshipsConfiguration.create(dataset_definitions=dataset_definitions, relationships=relationships)
    >>> relationship_config.id
    u'5506fcd38bd88f5953219da0'



Dataset Definitions and Relationships using helper functions
************************************************************

Create the :ref:`DatasetDefinition <dataset_definition>` and :ref:`Relationship <relationship>` for the profile and transaction dataset using helper functions.

.. code-block:: python

    profile_catalog_id = '5ec4aec1f072bc028e3471ae'
    profile_catalog_version_id = '5ec4aec2f072bc028e3471b1'

    transac_catalog_id = '5ec4aec268f0f30289a03901'
    transac_catalog_version_id = '5ec4aec268f0f30289a03900'

    profile_dataset_definition = dr.DatasetDefinition(
        identifier='profile',
        catalog_id=profile_catalog_id,
        catalog_version_id=profile_catalog_version_id
    )

    transaction_dataset_definition = dr.DatasetDefinition(
        identifier='transaction',
        catalog_id=transac_catalog_id,
        catalog_version_id=transac_catalog_version_id,
        primary_temporal_key='Date'
    )

    profile_transaction_relationship = dr.Relationship(
        dataset1_identifier='profile',
        dataset2_identifier='transaction',
        dataset1_keys=['CustomerID'],
        dataset2_keys=['CustomerID']
    )

    primary_profile_relationship = dr.Relationship(
        dataset2_identifier='profile',
        dataset1_keys=['CustomerID'],
        dataset2_keys=['CustomerID'],
        feature_derivation_window_start=-14,
        feature_derivation_window_end=-1,
        feature_derivation_window_time_unit='DAY',
        prediction_point_rounding=1,
        prediction_point_rounding_time_unit='DAY'
    )

    dataset_definitions = [profile_dataset_definition, transaction_dataset_definition]
    relationships = [primary_profile_relationship, profile_transaction_relationship]

Dataset Definition and Relationship using dictionary
****************************************************

Create the dataset definitions and relationships for the profile and transaction dataset using dict directly.

.. code-block:: python

    profile_catalog_id = profile_dataset.id
    profile_catalog_version_id = profile_dataset.version_id

    transac_catalog_id = transaction_dataset.id
    transac_catalog_version_id = transaction_dataset.version_id

    dataset_definitions = [
        {
            'identifier': 'transaction',
            'catalogVersionId': transac_catalog_version_id,
            'catalogId': transac_catalog_id,
            'primaryTemporalKey': 'Date',
            'snapshotPolicy': 'latest',
        },
        {
            'identifier': 'profile',
            'catalogId': profile_catalog_id,
            'catalogVersionId': profile_catalog_version_id,
            'snapshotPolicy': 'latest',
        },
    ]

    relationships = [
        {
            'dataset2Identifier': 'profile',
            'dataset1Keys': ['CustomerID'],
            'dataset2Keys': ['CustomerID'],
            'featureDerivationWindowStart': -14,
            'featureDerivationWindowEnd': -1,
            'featureDerivationWindowTimeUnit': 'DAY',
            'predictionPointRounding': 1,
            'predictionPointRoundingTimeUnit': 'DAY',
        },
        {
            'dataset1Identifier': 'profile',
            'dataset2Identifier': 'transaction',
            'dataset1Keys': ['CustomerID'],
            'dataset2Keys': ['CustomerID'],
        },
    ]

Retrieving Relationships Configuration
**************************************

You can retrieve specific relationships configuration using the ID of the relationship configuration.

.. code-block:: python

    relationship_config_id = '5506fcd38bd88f5953219da0'
    relationship_config = dr.RelationshipsConfiguration(id=relationship_config_id).get()
    >>> relationship_config.id == relationship_config_id
    True
    # Get all the datasets used in this relationships configuration
    >> len(relationship_config.dataset_definitions) == 2
    True
    >> relationship_config.dataset_definitions[0]
    {
        'feature_list_id': '5ec4af93603f596525d382d3',
        'snapshot_policy': 'latest',
        'catalog_id': '5ec4aec268f0f30289a03900',
        'catalog_version_id': '5ec4aec268f0f30289a03901',
        'primary_temporal_key': 'Date',
        'is_deleted': False,
        'identifier': 'transaction',
        'feature_lists':
            [
                {
                    'name': 'Raw Features',
                    'description': 'System created featurelist',
                    'created_by': 'User1',
                    'creation_date': datetime.datetime(2020, 5, 20, 4, 18, 27, 150000, tzinfo=tzutc()),
                    'user_created': False,
                    'dataset_id': '5ec4aec268f0f30289a03900',
                    'id': '5ec4af93603f596525d382d1',
                    'features': [u'CustomerID', u'AccountID', u'Date', u'Amount', u'Description']
                },
                {
                    'name': 'universe',
                    'description': 'System created featurelist',
                    'created_by': 'User1',
                    'creation_date': datetime.datetime(2020, 5, 20, 4, 18, 27, 172000, tzinfo=tzutc()),
                    'user_created': False,
                    'dataset_id': '5ec4aec268f0f30289a03900',
                    'id': '5ec4af93603f596525d382d2',
                    'features': [u'CustomerID', u'AccountID', u'Date', u'Amount', u'Description']
                },
                {
                    'features': [u'CustomerID', u'AccountID', u'Date', u'Amount', u'Description'],
                    'description': 'System created featurelist',
                    'created_by': u'Garvit Bansal',
                    'creation_date': datetime.datetime(2020, 5, 20, 4, 18, 27, 179000, tzinfo=tzutc()),
                    'dataset_version_id': '5ec4aec268f0f30289a03901',
                    'user_created': False,
                    'dataset_id': '5ec4aec268f0f30289a03900',
                    'id': u'5ec4af93603f596525d382d3',
                    'name': 'Informative Features'
                }
            ]
    }
    # Get information regarding how the datasets are connected among themselves as well as primary dataset
    >> relationship_config.relationships
    [
        {
            'dataset2Identifier': 'profile',
            'dataset1Keys': ['CustomerID'],
            'dataset2Keys': ['CustomerID'],
            'featureDerivationWindowStart': -14,
            'featureDerivationWindowEnd': -1,
            'featureDerivationWindowTimeUnit': 'DAY',
            'predictionPointRounding': 1,
            'predictionPointRoundingTimeUnit': 'DAY',
        },
        {
            'dataset1Identifier': 'profile',
            'dataset2Identifier': 'transaction',
            'dataset1Keys': ['CustomerID'],
            'dataset2Keys': ['CustomerID'],
        },
    ]

Updating details of Relationships Configuration
***********************************************

You can update the details of the existing relationships configuration


.. code-block:: python

    relationship_config_id = '5506fcd38bd88f5953219da0'
    relationship_config = dr.RelationshipsConfiguration(id=relationship_config_id)
    # Remove the obsolete datasets definition and its relationships
    new_datasets_definiton =
    [
        {
            'identifier': 'user',
            'catalogVersionId': '5c88a37770fc42a2fcc62759',
            'catalogId': '5c88a37770fc42a2fcc62759',
            'snapshotPolicy': 'latest',
        },
    ]

    # Get information regarding how the datasets are connected among themselves as well as primary dataset
    new_relationships =
    [
        {
            'dataset2Identifier': 'user',
            'dataset1Keys': ['user_id', 'dept_id'],
            'dataset2Keys': ['user_id', 'dept_id'],
        },
    ]
    new_config = relationship_config.replace(new_datasets_definiton, new_relationships)
    >>> new_config.id == relationship_config_id
    True
    >>> new_config.datasets_definition
    [
        {
            'identifier': 'user',
            'catalogVersionId': '5c88a37770fc42a2fcc62759',
            'catalogId': '5c88a37770fc42a2fcc62759',
            'snapshotPolicy': 'latest',
        },
    ]
    >>> new_config.relationships
    [
        {
            'dataset2Identifier': 'user',
            'dataset1Keys': ['user_id', 'dept_id'],
            'dataset2Keys': ['user_id', 'dept_id'],
        },
    ]

Delete Relationships Configuration
**********************************

You can delete the relationships configuration which is not used by any project

.. code-block:: python

    relationship_config_id = '5506fcd38bd88f5953219da0'
    relationship_config = dr.RelationshipsConfiguration(id=relationship_config_id)
    result = relationship_config.get()
    >>> result.id == relationship_config_id
    True
    # Delete the relationships configuration
    >>> relationship_config.delete()
    >>> relationship_config.get()
    ClientError: Relationships Configuration 5506fcd38bd88f5953219da0 not found

.. _secondary_dataset_configuration:

Secondary Dataset Configuration
*******************************
Secondary Dataset Config allows the user to use the different secondary datasets
for Feature Discovery Project during prediction time.


Secondary Datasets using helper functions
*****************************************

Create the :ref:`Secondary Dataset <secondary_dataset>` using helper functions.

.. code-block:: python

    >>> profile_catalog_id = '5ec4aec1f072bc028e3471ae'
    >>> profile_catalog_version_id = '5ec4aec2f072bc028e3471b1'

    >>> transac_catalog_id = '5ec4aec268f0f30289a03901'
    >>> transac_catalog_version_id = '5ec4aec268f0f30289a03900'

    profile_secondary_dataset = dr.SecondaryDataset(
        identifier='profile',
        catalog_id=profile_catalog_id,
        catalog_version_id=profile_catalog_version_id,
        snapshot_policy='latest'
    )

    transaction_secondary_dataset = dr.SecondaryDataset(
        identifier='transaction',
        catalog_id=transac_catalog_id,
        catalog_version_id=transac_catalog_version_id,
        snapshot_policy='latest'
    )

    secondary_datasets = [profile_secondary_dataset, transaction_secondary_dataset]

Secondary Datasets using dict
*****************************

Create the secondary datasets using raw dict structure

.. code-block:: python

    secondary_datasets = [
        {
            'snapshot_policy': u'latest',
            'identifier': u'profile',
            'catalog_version_id': u'5fd06b4af24c641b68e4d88f',
            'catalog_id': u'5fd06b4af24c641b68e4d88e'
        },
        {
            'snapshot_policy': u'dynamic',
            'identifier': u'transaction',
            'catalog_version_id': u'5fd1e86c589238a4e635e98e',
            'catalog_id': u'5fd1e86c589238a4e635e98d'
        }
    ]

Create Secondary Dataset Configuration
**************************************

Create the secondary dataset configuration for the Feature discovery Project which uses
two secondary datasets: `profile` and `transaction`.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get(project_id='54e639a18bd88f08078ca831')

    new_secondary_dataset_config = dr.SecondaryDatasetConfigurations.create(
        project_id=project.id,
        name='My config',
        secondary_datasets=secondary_datasets
    )


    >>> new_secondary_dataset_config.id
    '5fd1e86c589238a4e635e93d'

Retrieve Secondary Dataset Config
*********************************

You can retrieve specific secondary dataset configuration using the ID


.. code-block:: python

    >>> config_id = '5fd1e86c589238a4e635e93d'

    secondary_dataset_config = dr.SecondaryDatasetConfigurations(id=config_id).get()
    >>> secondary_dataset_config.id == config_id
    True
    >>> secondary_dataset_config
        {
             'created': datetime.datetime(2020, 12, 9, 6, 16, 22, tzinfo=tzutc()),
             'creator_full_name': u'abc@datarobot.com',
             'creator_user_id': u'asdf4af1gf4bdsd2fba1de0a',
             'credential_ids': None,
             'featurelist_id': None,
             'id': u'5fd1e86c589238a4e635e93d',
             'is_default': True,
             'name': u'My config',
             'project_id': u'5fd06afce2456ec1e9d20457',
             'project_version': None,
             'secondary_datasets': [
                    {
                        'snapshot_policy': u'latest',
                        'identifier': u'profile',
                        'catalog_version_id': u'5fd06b4af24c641b68e4d88f',
                        'catalog_id': u'5fd06b4af24c641b68e4d88e'
                    },
                    {
                        'snapshot_policy': u'dynamic',
                        'identifier': u'transaction',
                        'catalog_version_id': u'5fd1e86c589238a4e635e98e',
                        'catalog_id': u'5fd1e86c589238a4e635e98d'
                    }
             ]
        }

List All the Secondary Dataset Configs
**************************************

You can list all the secondary dataset configurations created in the project


.. code-block:: python

    >>> secondary_dataset_configs = dr.SecondaryDatasetConfigurations.list(project.id)
    >>> secondary_dataset_configs[0]
        {
             'created': datetime.datetime(2020, 12, 9, 6, 16, 22, tzinfo=tzutc()),
             'creator_full_name': u'abc@datarobot.com',
             'creator_user_id': u'asdf4af1gf4bdsd2fba1de0a',
             'credential_ids': None,
             'featurelist_id': None,
             'id': u'5fd1e86c589238a4e635e93d',
             'is_default': True,
             'name': u'My config',
             'project_id': u'5fd06afce2456ec1e9d20457',
             'project_version': None,
             'secondary_datasets': [
                    {
                        'snapshot_policy': u'latest',
                        'identifier': u'profile',
                        'catalog_version_id': u'5fd06b4af24c641b68e4d88f',
                        'catalog_id': u'5fd06b4af24c641b68e4d88e'
                    },
                    {
                        'snapshot_policy': u'dynamic',
                        'identifier': u'transaction',
                        'catalog_version_id': u'5fd1e86c589238a4e635e98e',
                        'catalog_id': u'5fd1e86c589238a4e635e98d'
                    }
             ]
        }
