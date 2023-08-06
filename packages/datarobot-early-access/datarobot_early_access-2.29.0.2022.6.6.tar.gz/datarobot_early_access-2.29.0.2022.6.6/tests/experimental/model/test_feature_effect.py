#
# Copyright 2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

import json

import pytest
import responses

from datarobot._experimental import DatetimeModel, Model
from datarobot.models import FeatureEffects


@pytest.fixture
def one_model_exp(model_data):
    return Model.from_data(model_data)


@pytest.fixture
def one_datetime_model_exp(model_id, project_id):
    return DatetimeModel(id=model_id, project_id=project_id)


@pytest.fixture
def feature_effect_server_data():
    return {
        "projectId": "project_id",
        "modelId": "model_id",
        "source": "training",
        "featureEffects": [
            {
                "featureType": "numeric",
                "predictedVsActual": {
                    "isCapped": False,
                    "data": [
                        {
                            "rowCount": 46.5,
                            "actual": 16,
                            "predicted": 15,
                            "label": "[ 1872, 1879 )",
                            "bin": ["1872", "1879"],
                        },
                        {
                            "rowCount": 31.5,
                            "actual": 752,
                            "predicted": 799.43,
                            "label": "[ 1879, 1886 )",
                            "bin": ["1879", "1886"],
                        },
                        {
                            "rowCount": 0.0,
                            "actual": None,
                            "predicted": None,
                            "label": "[ 1879, 1886 )",
                            "bin": ["1879", "1886"],
                        },
                    ],
                },
                "partialDependence": {
                    "isCapped": False,
                    "data": [
                        {"dependence": 41.25, "label": "1999"},
                        {"dependence": 40.64, "label": "1928"},
                        {"dependence": 41.44, "label": "nan"},
                    ],
                },
                "featureName": "record_min_temp_year",
                "weightLabel": None,
                "featureImpactScore": 1,
                "isBinnable": False,
                "isScalable": True,
                "individualConditionalExpectation": {
                    "isCapped": True,
                    "data": [
                        [
                            {"dependence": 3.574459450887747, "label": "3"},
                            {"dependence": 8.398920976345721, "label": "4"},
                        ],
                        [
                            {"dependence": 2.843083411286525, "label": "3"},
                            {"dependence": 1.4162371027540206, "label": "4"},
                        ],
                    ],
                },
            },
            {
                "featureType": "categorical",
                "predictedVsActual": {
                    "isCapped": False,
                    "data": [
                        {"rowCount": 99, "actual": 4107, "predicted": 4110.0, "label": "1"},
                        {"rowCount": 98, "actual": 4175, "predicted": 4119.0, "label": "0"},
                    ],
                },
                "partialDependence": {
                    "isCapped": False,
                    "data": [
                        {"dependence": 41.13, "label": "1"},
                        {"dependence": 41.91, "label": "0"},
                        {"dependence": 41.92, "label": "=Other Unseen="},
                    ],
                },
                "featureName": "date (Day of Week)",
                "weightLabel": None,
                "featureImpactScore": 0.2,
                "isBinnable": False,
                "isScalable": None,
                "individualConditionalExpectation": {
                    "isCapped": True,
                    "data": [
                        [
                            {"dependence": 3.574459450887747, "label": "3"},
                            {"dependence": 8.398920976345721, "label": "4"},
                        ],
                        [
                            {"dependence": 2.843083411286525, "label": "3"},
                            {"dependence": 1.4162371027540206, "label": "4"},
                        ],
                    ],
                },
            },
            {
                "featureType": "categorical",
                "partialDependence": {
                    "isCapped": False,
                    "data": [
                        {"dependence": 41.13, "label": "1"},
                        {"dependence": 41.91, "label": "0"},
                        {"dependence": 41.92, "label": "=Other Unseen="},
                    ],
                },
                "featureName": "date (Day of Week) no pvsa",
                "weightLabel": None,
                "featureImpactScore": 0.1,
                "isBinnable": True,
                "isScalable": None,
                "individualConditionalExpectation": {
                    "isCapped": True,
                    "data": [
                        [
                            {"dependence": 3.574459450887747, "label": "3"},
                            {"dependence": 8.398920976345721, "label": "4"},
                        ],
                        [
                            {"dependence": 2.843083411286525, "label": "3"},
                            {"dependence": 1.4162371027540206, "label": "4"},
                        ],
                    ],
                },
            },
        ],
    }


@pytest.fixture
def feature_effect_response(feature_effect_server_data, feature_effect_url):
    source = "training"
    include_ice_plots = True
    body = json.dumps(feature_effect_server_data)
    responses.add(
        responses.GET,
        "{}?source={},includeIcePlots={}".format(feature_effect_url, source, include_ice_plots),
        status=200,
        content_type="application/json",
        body=body,
    )


@pytest.fixture
def feature_effect_url(project_id, model_id):
    return "https://host_name.com/projects/{}/models/{}/featureEffects/".format(
        project_id, model_id
    )


@pytest.fixture
def feature_effect_url_datetime(project_id, model_id):
    return "https://host_name.com/projects/{}/datetimeModels/{}/featureEffects/".format(
        project_id, model_id
    )


@pytest.fixture
def feature_effect_server_data_datetime(feature_effect_server_data):

    feature_effect_server_data_datetime = dict(feature_effect_server_data)
    feature_effect_server_data_datetime["backtestIndex"] = "0"
    return feature_effect_server_data_datetime


@pytest.fixture
def feature_effect_response_datetime(
    feature_effect_server_data_datetime, feature_effect_url_datetime
):
    source = "training"
    backtest_index = "0"
    include_ice_plots = True
    responses.add(
        responses.GET,
        "{}?source={}&backtestIndex={},includeIcePlots={}".format(
            feature_effect_url_datetime, source, backtest_index, include_ice_plots
        ),
        status=200,
        content_type="application/json",
        body=json.dumps(feature_effect_server_data_datetime),
    )


@responses.activate
@pytest.mark.usefixtures("feature_effect_response")
def test_get_feature_effect_assumed_complete(one_model_exp, feature_effect_server_data):
    feature_effect = one_model_exp.get_feature_effect(source="training", include_ice_plots=True)

    assert feature_effect.project_id == feature_effect_server_data["projectId"]
    assert feature_effect.model_id == feature_effect_server_data["modelId"]
    assert feature_effect.source == feature_effect_server_data["source"]
    assert feature_effect.project_id == feature_effect_server_data["projectId"]
    assert len(feature_effect.feature_effects) == len(feature_effect_server_data["featureEffects"])

    expected_fe = FeatureEffects.from_server_data(feature_effect_server_data)
    assert expected_fe == feature_effect


@responses.activate
@pytest.mark.usefixtures("feature_effect_response_datetime")
def test_get_feature_effect_assumed_complete_datetime(
    one_datetime_model_exp, feature_effect_server_data_datetime
):
    backtest_index = "0"
    source = "invalid"
    feature_effect = one_datetime_model_exp.get_feature_effect(
        source=source, backtest_index=backtest_index, include_ice_plots=True
    )
    assert feature_effect.project_id == feature_effect_server_data_datetime["projectId"]
    assert feature_effect.model_id == feature_effect_server_data_datetime["modelId"]
    assert feature_effect.source == feature_effect_server_data_datetime["source"]
    assert feature_effect.project_id == feature_effect_server_data_datetime["projectId"]
    assert feature_effect.backtest_index == feature_effect_server_data_datetime["backtestIndex"]
    assert len(feature_effect.feature_effects) == len(
        feature_effect_server_data_datetime["featureEffects"]
    )
    expected_fe = FeatureEffects.from_server_data(feature_effect_server_data_datetime)
    assert expected_fe == feature_effect
