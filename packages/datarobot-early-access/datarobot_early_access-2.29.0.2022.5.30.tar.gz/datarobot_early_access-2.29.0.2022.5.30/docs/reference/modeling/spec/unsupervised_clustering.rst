.. _unsupervised_clustering:

#########################################
Unsupervised Projects (Clustering)
#########################################

Use clustering when data is not labelled and the problem can be interpreted as grouping a set of
objects in such a way that objects in the same group (called a cluster) are more similar
to each other than to those in other groups (clusters). It is a common task in data exploration
when finding groups and similarities is needed.


Creating Unsupervised Projects
==============================

To create an unsupervised project, set ``unsupervised_mode`` to ``True`` when setting the target.
To specify clustering, set ``unspervised_type`` to ``CLUSTERING``.

Example:

.. code-block:: python

    from datarobot import Project
    from datarobot.enums import UnsupervisedTypeEnum

    project = Project.create("dataset.csv", project_name="unsupervised clustering")
    project.set_target(
        unsupervised_mode=True,
        unsupervised_type=UnsupervisedTypeEnum.CLUSTERING)

You can optionally specify list of explicit cluster numbers. To do this, pass a list of integer
values to optional ``autopilot_cluster_list`` parameter using the ``set_target()`` method.

.. code-block:: python

    project.set_target(
        unsupervised_mode=True,
        unsupervised_type=UnsupervisedTypeEnum.CLUSTERING,
        autopilot_cluster_list=[7, 9, 11, 15, 19]

You can also do both in one step using the ``Project.start()`` method:

.. code-block:: python

    from datarobot import Project
    from datarobot.enums import UnsupervisedTypeEnum

    project = Project.start("dataset.csv",
                  unsupervised_mode=True,
                  project_name="unsupervised clustering project",
                  unsupervised_type=UnsupervisedTypeEnum.CLUSTERING)


Unsupervised Clustering Project Metric
======================================

Unsupervised clustering projects use the ``Silhouette Score`` metric for model ranking (instead of
using it for model optimization). It measures the average similarity of objects within a cluster
and their distance to the other objects in the other clusters.


Retrieving information about Clusters
=====================================

In a trained model, you can retrieve information about clusters in along with standard model
information. To do this, when training completes, retrieve a model and view basic clustering
information:

  - ``n_clusters`` : number of clusters for model
  - ``is_n_clusters_dynamically_determined`` : how clustering model picks number of clusters

Here is a code snippet to retrieve information about the number of clusters for model:

.. code-block:: python

    from datarobot import ClusteringModel
    model = ClusteringModel.get(project_id, model_id)
    print("{} clusters found".format(model.n_clusters))

You can retrieve more details about clusters and their data using cluster insights.

Working with Clusters Insights
==============================

You can compute insights to gain deep insights into clusters and their characteristics. This
process will perform calculations and return detailed information about each feature and its
importance, as well as a detailed per-cluster breakdown.

To compute and retrieve cluster insights, use the ``ClusteringModel`` and its ``compute_insights``
method. The method starts the cluster insights compute job, waits for its completion for the number
of seconds specified in the optional parameter ``max_wait`` (default: 600), and returns results
when insights are ready.

If clusters are already computed,  access them using the ``insights`` property of the
``ClusteringModel`` method.

.. code-block:: python

    from datarobot import ClusteringModel
    model = ClusteringModel.get(project_id, model_id)
    insights = model.compute_insights()

This call, with the specified ``wait_time``, will run and wait for specified time:

.. code-block:: python

    from datarobot import ClusteringModel
    model = ClusteringModel.get(project_id, model_id)
    insights = model.compute_insights(max_wait=60)

If computation fails to finish before ``max_wait`` expires, the method will raise
an ``AsyncTimeoutError``. You can retrieve cluster insights after jobs computation finishes.

To retrieve cluster insights already computed:

.. code-block:: python

    from datarobot import ClusteringModel
    model = ClusteringModel.get(project_id, model_id)
    for insight in model.insights:
        print(insight)


Working with Clusters
=====================
By default, DataRobot names clusters "Cluster 1", "Cluster 2", ... , "Cluster N" .
You can retrieve these names and alter them according to preference. When retrieving
clusters before computing insights, clusters will contain only names. After insight computation
completes, each cluster will also hold information about the percentage of data that is represented
by the Cluster.

For example:

.. code-block:: python

    from datarobot import ClusteringModel
    model = ClusteringModel.get(project_id, model_id)

    # helper function
    def print_summary(name, percent):
        if not percent:
            percent = "?"
        print("'{}' holds {} % of data".format(name, percent))

    for cluster in model.clusters:
        print_summary(cluster.name, cluster.percent)
    model.compute_insights()
    for cluster in model.clusters:
        print_summary(cluster.name, cluster.percent)

For a model with three clusters, the code snippet will output:

.. code-block:: console

    'Cluster 1' holds ? % of data
    'Cluster 2' holds ? % of data
    'Cluster 3' holds ? % of data
    -- Cluster insights computation finished --
    'Cluster 1' holds 27.1704180064 % of data
    'Cluster 2' holds 36.9131832797 % of data
    'Cluster 3' holds 35.9163987138 % of data


Use the following methods of ``ClusteringModel`` class to alter cluster names:
  - ``update_cluster_names`` - changes multiple cluster names using mapping in dictionary
  - ``update_cluster_name`` - changes one cluster name

After update, each method will return a list of clusters with changed names.

For example:

.. code-block:: python

    from datarobot import ClusteringModel
    model = ClusteringModel.get(project_id, model_id)

    # update multiple
    cluster_name_mappings = [
        ("Cluster 1", "AAA"),
        ("Cluster 2", "BBB"),
        ("Cluster 3", "CCC")
    ]
    clusters = model.update_cluster_names(cluster_name_mappings)

    # update single
    clusters = model.update_cluster_name("CCC", "DDD")


Clustering Classes Reference
============================

===============
ClusteringModel
===============

.. autoclass:: datarobot.models.model.ClusteringModel
   :members:

=======
Cluster
=======

.. autoclass:: datarobot.models.model.Cluster
   :members:

============================
ClusterInsight
============================

.. autoclass:: datarobot.models.model.ClusterInsight
   :members:
