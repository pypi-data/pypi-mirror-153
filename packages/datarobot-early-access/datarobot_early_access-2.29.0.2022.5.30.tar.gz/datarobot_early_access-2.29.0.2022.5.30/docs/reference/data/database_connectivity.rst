.. _database_connectivity_overview:

#####################
Database Connectivity
#####################

Databases are a widely used tool for carrying valuable business data. To enable integration
with a variety of enterprise databases, DataRobot provides a "self-service" JDBC product
for database connectivity setup. Once configured, you can read data from production databases
for model building and predictions. This allows you to quickly train and retrain models
on that data, and avoids the unnecessary step of exporting data from your enterprise database
to a CSV for ingest to DataRobot. It allows access to more diverse data,
which results in more accurate models.

The steps describing how to set up your database connections use the following terminology:

- ``DataStore``: A configured connection to a database. It has a name, a specified driver,
  and a JDBC URL. You can register data stores with DataRobot for ease of re-use.
  A data store has one connector but can have many data sources.
- ``DataSource``: A configured connection to the backing data store (the location of data
  within a given endpoint). A data source specifies, via SQL query or selected table
  and schema data, which data to extract from the data store to use for modeling or predictions.
  A data source has one data store and one connector but can have many datasets.
- ``DataDriver``: The software that allows the DataRobot application to interact with a database;
  each data store is associated with either a driver or a connector (created by the admin). The
  driver configuration saves the storage location in DataRobot of the JAR file and any additional
  dependency files associated with the driver.
- ``Connector``: Similarly to data drivers, a connector allows the DataRobot application to interact
  with a database; each data store is associated with either a driver or a connector (created by the
  admin). The connector configuration saves the storage location in DataRobot of the JAR file and
  any additional dependency files associated with the connector.
- ``Dataset``: Data, a file or the content of a data source, at a particular point in time.
  A data source can produce multiple datasets; a dataset has exactly one data source.


The expected workflow when setting up projects or prediction datasets is:

1. The administrator sets up a :py:class:`datarobot.DataDriver` for accessing a particular database.
   For any particular driver, this setup is done once for the entire system and then
   the resulting driver is used by all users.
2. Users create a :py:class:`datarobot.DataStore` which represents an interface
   to a particular database, using that driver.
3. Users create a :py:class:`datarobot.DataSource` representing a particular set of data
   to be extracted from the DataStore.
4. Users create projects and prediction datasets from a DataSource.

Besides the described workflow for creating projects and prediction datasets, users can manage
their DataStores and DataSources and admins can manage Drivers by listing, retrieving, updating
and deleting existing instances.

**Cloud users:** This feature is turned off by default. To enable the feature, contact
your CFDS or DataRobot Support.

Creating Drivers
----------------

The admin should specify ``class_name``, the name of the Java class in the Java archive
which implements the ``java.sql.Driver`` interface; ``canonical_name``, a user-friendly name
for resulting driver to display in the API and the GUI; and ``files``, a list of local files which
contain the driver.

.. code-block:: python

    >>> import datarobot as dr
    >>> driver = dr.DataDriver.create(
    ...     class_name='org.postgresql.Driver',
    ...     canonical_name='PostgreSQL',
    ...     files=['/tmp/postgresql-42.2.2.jar']
    ... )
    >>> driver
    DataDriver('PostgreSQL')

Creating Connectors
-------------------

The admin should specify ``file_path``, the local connector .jar file.

.. code-block:: python

    >>> import datarobot as dr
    >>> connector = dr.Connector.create(file_path='/tmp/connector-s3.jar')
    >>> connector
    Connector('S3 Connector')

Creating DataStores
-------------------

After the admin has created drivers, any user can use them for ``DataStore`` creation.
A DataStore represents a JDBC database. When creating them, users should specify ``type``,
which currently must be ``jdbc``; ``canonical_name``, a user-friendly name to display
in the API and GUI for the DataStore; ``driver_id``, the id of the driver to use to connect
to the database; and ``jdbc_url``, the full URL specifying the database connection settings
like database type, server address, port, and database name.

.. code-block:: python

    >>> import datarobot as dr
    >>> data_store = dr.DataStore.create(
    ...     data_store_type='jdbc',
    ...     canonical_name='Demo DB',
    ...     driver_id='5a6af02eb15372000117c040',
    ...     jdbc_url='jdbc:postgresql://my.db.address.org:5432/perftest'
    ... )
    >>> data_store
    DataStore('Demo DB')
    >>> data_store.test(username='username', password='password')
    {'message': 'Connection successful'}

Creating DataSources
--------------------

Once users have a DataStore, they can can query datasets via the DataSource entity,
which represents a query. When creating a DataSource, users first create a
:py:class:`datarobot.DataSourceParameters` object from a DataStore's id and a query,
and then create the DataSource with a ``type``, currently always ``jdbc``; a ``canonical_name``,
the user-friendly name to display in the API and GUI, and ``params``, the DataSourceParameters
object.

.. code-block:: python

    >>> import datarobot as dr
    >>> params = dr.DataSourceParameters(
    ...     data_store_id='5a8ac90b07a57a0001be501e',
    ...     query='SELECT * FROM airlines10mb WHERE "Year" >= 1995;'
    ... )
    >>> data_source = dr.DataSource.create(
    ...     data_source_type='jdbc',
    ...     canonical_name='airlines stats after 1995',
    ...     params=params
    ... )
    >>> data_source
    DataSource('airlines stats after 1995')

Creating Projects
-----------------

Given a DataSource, users can create new projects from it.

.. code-block:: python

    >>> import datarobot as dr
    >>> project = dr.Project.create_from_data_source(
    ...     data_source_id='5ae6eee9962d740dd7b86886',
    ...     username='username',
    ...     password='password'
    ... )

Creating Predictions
--------------------

Given a DataSource, new prediction datasets can be created for any project.

.. code-block:: python

    >>> import datarobot as dr
    >>> project = dr.Project.get('5ae6f296962d740dd7b86887')
    >>> prediction_dataset = project.upload_dataset_from_data_source(
    ...     data_source_id='5ae6eee9962d740dd7b86886',
    ...     username='username',
    ...     password='password'
    ... )
