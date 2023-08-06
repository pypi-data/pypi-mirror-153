#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import pytest
import responses

import datarobot as dr
from datarobot.errors import ClientError, ServerError
from datarobot.utils import parse_time


@pytest.fixture
def autodocs_endpoint(client):
    return "{}/{}".format(client.endpoint, dr.AutomatedDocument._path)


@pytest.fixture
def doc_id():
    return "5f6e3f01bcc52b0ef65bd013"


@pytest.fixture
def doc_url(doc_id):
    return "https://host_name.com/{}{}/".format(dr.AutomatedDocument._path, doc_id)


class TestAutomatedDocument:
    @responses.activate
    def test_list_available_document_types__success(self, client):
        url = "{}/automatedDocumentOptions/".format(client.endpoint)
        response_body = {"data": [{"document_type": "AUTOPILOT_SUMMARY", "locale": "EN_US"}]}
        responses.add(responses.GET, url, status=200, json=response_body)

        options = dr.AutomatedDocument.list_available_document_types()
        assert options == response_body

    @responses.activate
    def test_generate__success(self, autodocs_endpoint, doc_id, doc_url, client):
        document_type = "MODEL_COMPLIANCE"
        entity_id = "6f50cdb77cc4f8d1560c3ed5"
        output_format = "docx"
        locale = "EN_US"
        template_id = "50efc9db8aff6c81a374aeec"

        request_body = {
            "document_type": document_type,
            "entity_id": entity_id,
            "output_format": output_format,
            "locale": locale,
            "template_id": template_id,
        }

        status_url = "{}/status/17f182fa-6562-4cdc-9fe1-46ecbe769629/".format(client.endpoint)

        responses.add(
            responses.POST,
            autodocs_endpoint,
            json=request_body,
            status=202,
            adding_headers={"Location": status_url},
        )

        responses.add(responses.GET, status_url, status=303, adding_headers={"Location": doc_url})

        doc = dr.AutomatedDocument(
            document_type=document_type,
            entity_id=entity_id,
            output_format=output_format,
            locale=locale,
            template_id=template_id,
        )

        response = doc.generate()

        assert response.status_code == 202
        assert doc.id == doc_id
        assert doc.filepath is None
        assert doc.created_at is None

    @responses.activate
    def test_download__success(self, doc_url, doc_id):
        responses.add(
            responses.GET,
            doc_url,
            stream=True,
            status=200,
            content_type="application/docx",
            adding_headers={"Content-Disposition": "attachment;filename=report.docx"},
        )

        doc = dr.AutomatedDocument(id=doc_id)
        response = doc.download()

        assert response.status_code == 200
        assert set(response.headers) == {"Content-Disposition", "Content-Type"}
        assert doc.filepath == "report.docx"

    def test_download__no_doc_id__attr_error(self):
        with pytest.raises(AttributeError):
            dr.AutomatedDocument().download()

    @responses.activate
    def test_delete__success(self, doc_id, doc_url):
        responses.add(responses.DELETE, doc_url, status=204)

        doc = dr.AutomatedDocument(id=doc_id)
        response = doc.delete()

        assert response.status_code == 204

    def test_delete__no_doc_id__attr_error(self):
        with pytest.raises(AttributeError):
            dr.AutomatedDocument().delete()

    @responses.activate
    def test_list_generated_documents__success(self, autodocs_endpoint):

        items = [
            {
                "entity_id": "5e8c6a34d2427053ab4a39ed",
                "document_type": "MODEL_COMPLIANCE",
                "output_format": "docx",
                "locale": "EN_US",
                "template_id": "nul",
                "id": "60548987c297f6053d056f2e",
                "created_at": "2021-03-19 11:22:47.188000",
            },
            {
                "entity_id": "5bdc5f60d25eff701ad8fe91",
                "document_type": "AUTOPILOT_SUMMARY",
                "output_format": "html",
                "locale": "EN_US",
                "template_id": "513dce50edc297fc87a9db13ed6",
                "id": "60548969c297f6053d056f25",
                "created_at": "2020-10-29 10:27:50.866000",
            },
        ]

        json = {"previous": None, "next": None, "count": 2, "totalCount": 2, "data": items}

        responses.add(
            responses.GET, autodocs_endpoint, json=json, status=200,
        )

        [
            item.update({"created_at": parse_time(item["created_at"]), "filepath": None})
            for item in items
        ]

        docs = dr.AutomatedDocument.list_generated_documents()
        docs_for_compare = [doc.__dict__ for doc in docs]

        assert len(docs) == len(items)
        assert docs_for_compare == items


class TestAutomatedDocumentModelComplianceInitialization:
    _path = dr.AutomatedDocument._model_compliance_initialization_path

    @responses.activate
    @pytest.mark.parametrize(
        "expected_is_initialized, expected_status",
        [(True, "initialized"), (False, "trainingDataAssignmentInProgress")],
    )
    def test_is_model_compliance_initialized__success(
        self, client, expected_is_initialized, expected_status
    ):
        # arrange
        entity_id = "6f50cdb77cc4f8d1560c3ed5"

        model_compliance_initialization_url = "{}/{}{}/".format(
            client.endpoint, self._path, entity_id
        )

        responses.add(
            responses.GET,
            model_compliance_initialization_url,
            json={"initialized": expected_is_initialized, "status": expected_status},
            status=200,
        )

        # act
        doc = dr.AutomatedDocument(
            document_type="MODEL_COMPLIANCE",
            entity_id=entity_id,
            output_format="docx",
            locale="EN_US",
        )

        is_initialized, status = doc.is_model_compliance_initialized

        # assert
        assert is_initialized is expected_is_initialized
        assert status == expected_status

        assert len(responses.calls) == 1

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == model_compliance_initialization_url

    @responses.activate
    def test_is_model_compliance_initialized__error(self, client):
        # arrange
        entity_id = "6f50cdb77cc4f8d1560c3ed5"

        model_compliance_initialization_url = "{}/{}{}/".format(
            client.endpoint, self._path, entity_id
        )

        responses.add(
            responses.GET,
            model_compliance_initialization_url,
            json={"message": "error message"},
            status=422,
        )

        # act
        doc = dr.AutomatedDocument(
            document_type="MODEL_COMPLIANCE",
            entity_id=entity_id,
            output_format="docx",
            locale="EN_US",
        )

        with pytest.raises(ClientError) as e:
            doc.is_model_compliance_initialized

            # assert
            assert e.status_code == 422
            assert e.json == {"message": "error message"}

        assert len(responses.calls) == 1

        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == model_compliance_initialization_url

    @responses.activate
    def test_initialize_model_compliance__success(self, client):
        # arrange
        entity_id = "6f50cdb77cc4f8d1560c3ed5"

        status_url = "{}/status/17f182fa-6562-4cdc-9fe1-46ecbe769629/".format(client.endpoint)
        model_compliance_initialization_url = "{}/{}{}/".format(
            client.endpoint, self._path, entity_id
        )

        responses.add(
            responses.POST,
            model_compliance_initialization_url,
            status=202,
            adding_headers={"Location": status_url},
        )

        responses.add(
            responses.GET,
            status_url,
            status=303,
            adding_headers={"Location": model_compliance_initialization_url},
        )

        responses.add(
            responses.GET,
            model_compliance_initialization_url,
            json={"initialized": True, "status": "initialized"},
            status=200,
            adding_headers={"Location": status_url},
        )

        # act
        doc = dr.AutomatedDocument(
            document_type="MODEL_COMPLIANCE",
            entity_id=entity_id,
            output_format="docx",
            locale="EN_US",
        )

        is_initialized, status = doc.initialize_model_compliance()

        # assert
        assert is_initialized is True
        assert status == "initialized"

        assert len(responses.calls) == 3

        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == model_compliance_initialization_url

        assert responses.calls[1].request.method == "GET"
        assert responses.calls[1].request.url == status_url

        assert responses.calls[2].request.method == "GET"
        assert responses.calls[2].request.url == model_compliance_initialization_url

    @responses.activate
    def test_initialize_model_compliance__error(self, client):
        # arrange
        entity_id = "6f50cdb77cc4f8d1560c3ed5"

        model_compliance_initialization_url = "{}/{}{}/".format(
            client.endpoint, self._path, entity_id
        )

        responses.add(
            responses.POST,
            model_compliance_initialization_url,
            json={"message": "error message"},
            status=422,
        )

        # act
        doc = dr.AutomatedDocument(
            document_type="MODEL_COMPLIANCE",
            entity_id=entity_id,
            output_format="docx",
            locale="EN_US",
        )

        with pytest.raises(ClientError) as e:
            doc.initialize_model_compliance()

            # assert
            assert e.status_code == 422
            assert e.json == {"message": "error message"}

        assert len(responses.calls) == 1

        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == model_compliance_initialization_url

    @responses.activate
    def test_initialize_model_compliance__async_error(self, client):
        # arrange
        entity_id = "6f50cdb77cc4f8d1560c3ed5"

        status_url = "{}/status/17f182fa-6562-4cdc-9fe1-46ecbe769629/".format(client.endpoint)
        model_compliance_initialization_url = "{}/{}{}/".format(
            client.endpoint, self._path, entity_id
        )

        responses.add(
            responses.POST,
            model_compliance_initialization_url,
            status=202,
            adding_headers={"Location": status_url},
        )

        responses.add(
            responses.GET, status_url, status=500,
        )

        # act
        doc = dr.AutomatedDocument(
            document_type="MODEL_COMPLIANCE",
            entity_id=entity_id,
            output_format="docx",
            locale="EN_US",
        )

        with pytest.raises(ServerError) as e:
            doc.initialize_model_compliance()

            # assert
            assert e.status_code == 500

        assert len(responses.calls) == 2

        assert responses.calls[0].request.method == "POST"
        assert responses.calls[0].request.url == model_compliance_initialization_url

        assert responses.calls[1].request.method == "GET"
        assert responses.calls[1].request.url == status_url
