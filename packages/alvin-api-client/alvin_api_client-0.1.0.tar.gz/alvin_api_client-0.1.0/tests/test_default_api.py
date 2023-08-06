import pytest


@pytest.fixture(params=[
    (
        'get_client_config_api_v1_client_config_get',
        (
            ((
                [], {}
            ), lambda response: all(x in response for x in (
                'auth_config',
                'experiences_config',
                'notification_config',
                'product_analytics_config',
                'product_onboarding_config',
            ))),
        )
    ),

])
def endpoint_test_data(request):
    """Information to run a test for a Client's method (API endpoint).

    This fixture allows defining a python method of the client to test,
    by inputing sample data and then doing an arbitrary 'verification test' on
    the returned (response) data.

    Each of the Client's python methods corresponds to an API endpoint.
    """
    return type('TestData', (), {
        'method': request.param[0],
        'inputs': (test_data[0] for test_data in request.param[1]),
        'tests': (test_data[1] for test_data in request.param[1]),
    })



def test_endpoint(endpoint_test_data, localhost_api_client, default_api, test_client_method):
    """Test an API endpoint by calling its corresponding client's method.

    Each endpoint can be tested by inputing different parameters (with which the
    client method is invoked) and by testing the output on diverse criteria.
    """
    with localhost_api_client(8000) as api_client:
    
        api_instance = default_api(api_client)

        for (args, kwargs), assert_statement in zip(endpoint_test_data.inputs, endpoint_test_data.tests):
            test_client_method(
                api_instance,
                endpoint_test_data.method,
                (args, kwargs),
                assert_statement
            )
