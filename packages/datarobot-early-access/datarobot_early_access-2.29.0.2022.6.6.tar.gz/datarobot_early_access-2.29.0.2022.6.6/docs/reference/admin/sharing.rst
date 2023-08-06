.. _sharing:

Sharing
=======

Once you have created data stores or data sources, you may want to share them with collaborators.
DataRobot provides an API for sharing the following entities:

  - Data Sources and Data Stores ( see :ref:`Database Connectivity <database_connectivity_overview>` for more info on connecting to JDBC databases)
  - Projects
  - Calendar Files
  - Model Deployments (Only in the REST API, not yet in this Python client)

Access Levels
-------------

Entities can be shared at varying access levels. For example, you can allow someone to
create projects from a data source you have built without letting them delete it.

Each entity type uses slightly different permission names intended to convey more specifically what
kind of actions are available, and these roles fall into three categories. These generic role names
can be used in the sharing API for any entity.

For the complete set of actions granted by each role on a given entity, please see the user documentation in the web application.

  - ``OWNER``

    - used for all entities
    - allows any action including deletion

  - ``READ_WRITE``

    - known as as ``EDITOR`` on data sources and data stores
    - allows modifications to the state, e.g. renaming and creating data sources from a data store, but *not* deleting the entity

  - ``READ_ONLY``

    - known as ``CONSUMER`` on data sources and data stores
    - for data sources, enables creating projects and predictions; for data stores, allows viewing them only.

Finally, when a user's new role is specified as ``None``, their access will be revoked.

In addition to the role, some entities (currently only data sources and data stores) allow
separate control over whether a new user should be able to share that entity further. When granting access to a user,
the ``can_share`` parameter determines whether that user can, in turn, share this entity with another user.
When this parameter is specified as false, the user in question will have all the access to the entity granted by their
role and be able to remove themselves if desired, but be unable to change the role of any other user.

Examples
--------

Transfer access to the data source from old_user@datarobot.com to new_user@datarobot.com

.. code-block:: python

   import datarobot as dr

   new_access = dr.SharingAccess(new_user@datarobot.com,
                                 dr.enums.SHARING_ROLE.OWNER, can_share=True)
   access_list = [dr.SharingAccess(old_user@datarobot.com, None), new_access]

   dr.DataSource.get('my-data-source-id').share(access_list)


Checking access to a project

.. code-block:: python

   import datarobot as dr

   project = dr.Project.create('mydata.csv', project_name='My Data')

   access_list = project.get_access_list()

   access_list[0].username

Transfer ownership of all projects owned by your account to new_user@datarobot.com without sending notifications.

.. code-block:: python

   import datarobot as dr

   # Put path to YAML credentials below
   dr.Client(config_path= '.yaml')

   # Get all projects for your account and store the ids in a list
   projects = dr.Project.list()

   project_ids = [project.id for project in projects]

   # List of emails to share with
   share_targets = ['new_user@datarobot.com']

   # Target role
   target_role = dr.enums.SHARING_ROLE.OWNER

   for pid in project_ids:

      project = dr.Project.get(project_id=pid)

      shares = []

      for user in share_targets:

         shares.append(dr.SharingAccess(username=user, role=target_role))

      project.share(shares, send_notification=False)
