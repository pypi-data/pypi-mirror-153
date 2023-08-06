.. _automated_documentation_overview:

Automated Documentation
=======================

DataRobot can generate Automated Documentation about various entities within the platform, such
as specific models or projects. These reports can be downloaded and shared to help with
regulatory compliance as well as to provide a general understanding of the AI lifecycle.

##############################
Check Available Document Types
##############################

Automated Documentation is available behind different feature flags set up according to your POC
settings or subscription plan. ``MODEL_COMPLIANCE`` documentation is a premium add-on DataRobot
product, while ``AUTOPILOT_SUMMARY`` report is available behind an optional feature flag for
Self-Service and other platforms.

.. code-block:: python

    import datarobot as dr

    # Connect to your DataRobot platform with your token
    dr.Client(token=my_token, endpoint=endpoint)
    options = dr.AutomatedDocument.list_available_document_types()

In response, you get a ``data`` dictionary with a list of document types that are available for
generation with your account.

############################
Generate Automated Documents
############################

Now that you know which documents you can generate, create one with ``AutomatedDocument
.generate`` method. Note that for ``AUTOPILOT_SUMMARY`` report, you need to assign a project ID
to the ``entity_id`` parameter, while ``MODEL_COMPLIANCE`` expects an ID of a model with the
``entity_id`` parameter.

.. code-block:: python

    import datarobot as dr

    dr.Client(token=my_token, endpoint=endpoint)

    doc_type = "AUTOPILOT_SUMMARY"
    entity_id = "5e8b6a34d2426053ab9a39ed"  #  This is an ID of a project
    file_format="docx"

    doc = dr.AutomatedDocument(document_type=doc_type, entity_id=entity_id, output_format=file_format)
    doc.generate()

You can specify other attributes. For example, ``filepath`` presets the file location and name to
use when downloading the document. Please see the :ref:`API
Reference<automated_documentation_api>` for more details.

############################
Download Automated Documents
############################

If you followed the steps above to generate an automated document, you can use the
``AutomatedDocument.download`` method right away to get the document.

.. code-block:: python

    doc.filepath = "Users/jeremy/DR_project_docs/autopilot_report_staff_2021.docx"
    doc.download()

You can set a desired ``filepath`` (that includes the future file's name) before you download a
document. Otherwise, it will be automatically downloaded to the directory from which you launched
your script.

Please note that to download the document, you need its ID. When you generate a document with the
Python client, the ID is set automatically without your interference. However, if the document
has already been generated from the application interface (or REST API) and you want to download
it using the Python client, you need to provide the ID of the document you want to download:

.. code-block:: python

    import datarobot as dr

    dr.Client(token=my_token, endpoint=endpoint)

    doc_id = "604f81f0f3d6397d250c35bc"
    path = "Users/jeremy/DR_project_docs/xgb_model_doc_staff_project_2021.docx"
    doc = dr.AutomatedDocument(id=doc_id, filepath=path)
    doc.download()

#############################################
List Previously Generated Automated Documents
#############################################

You can retrieve information about previously generated documents available for your account. The
information includes document ID and type, ID of the entity it was generated for, time of
creation, and other information. Documents are sorted by creation time  -- ``created_at`` key --
from most recent to oldest.

.. code-block:: python

    import datarobot as dr

    dr.Client(token=my_token, endpoint=endpoint)
    docs = dr.AutomatedDocument.list_generated_documents()

This returns list of ``AutomatedDocument`` objects. You can request a list of specific documents.
For example, get a list of all ``MODEL_COMPLIANCE`` documents:

.. code-block:: python

    model_docs = dr.AutomatedDocument.list_generated_documents(document_types=["MODEL_COMPLIANCE"])

Or get a list of documents created for specific entities:

.. code-block:: python

    otv_project_reports = dr.AutomatedDocument.list_generated_documents(
        entity_ids=["604f81f0f3d6397d250c35bc", "5ed60de32f18d97d250c3db5"]
        )

For more information about all query options, see ``AutomatedDocument
.list_generated_documents`` in the :ref:`API Reference<automated_documentation_api>`.

##########################
Delete Automated Documents
##########################

To delete a document from the DataRobot application, use the ``AutomatedDocument.delete`` method.

.. code-block:: python

    import datarobot as dr

    dr.Client(token=my_token, endpoint=endpoint)
    doc = dr.AutomatedDocument(id="604f81f0f3d6397d250c35bc")
    doc.delete()

All locally saved automated documents will remain intact.
