import pytest


@pytest.fixture
def data_entity_usage_request():
    from alvin_api_client.model.data_entity_usage_stats_request import DataEntityUsageStatsRequest
    return DataEntityUsageStatsRequest


def test_data_entity_usage_request(
    data_entity_usage_request,
    query_builder,
    operator_type,
):
    OPERATOR = 'AND'
    query_builder_instance = query_builder(
        operator_type(OPERATOR)
    )
    model = data_entity_usage_request(
        query_builder_instance
    )
    assert {
        'query_builder': {
            'operator_type': OPERATOR
        }
    } == model.to_dict()
