import pytest
import alvin_api_client


@pytest.fixture
def config_class():
    """The Configuration class, used to configure instances of ApiClient class.
    
    Instances of the Configuration class are passed in the constructor of the
    ApiClient class.
    """
    from alvin_api_client import Configuration
    return Configuration


@pytest.fixture
def localhost_configuration(config_class):
    """Create a Configuration for localhost with the specified port number.

    Create an instance for the Configuration class, assigning as the 'host'
    parameter 'localhost' and appending 'port number' parameter at runtime.

    Usefull when running tests and the API service (the one that the ApiClient
    "wraps around") is served on localhost.
    """
    def localhost_configuration(port_number: int):
        """Create a Configuration for localhost with the specified port number.

        Args:
            port_number (int): port number on localhost to "listen" to

        Returns:
            Configuration: instance of a localhost configuration
        """
        return config_class(
            host=f'http://localhost:{port_number}'
        )
    return localhost_configuration


@pytest.fixture
def api_client():
    from alvin_api_client import ApiClient
    def get_api_client_instance(configuration):
        return ApiClient(configuration)
    return get_api_client_instance



@pytest.fixture
def localhost_api_client(api_client, localhost_configuration):
    def get_localhost_api_client_instance(port_number):
        return api_client(localhost_configuration(port_number))
    return get_localhost_api_client_instance



@pytest.fixture
def default_api():
    """Create instances of the DefaultApi class."""
    from alvin_api_client.api.default_api import DefaultApi
    return DefaultApi



@pytest.fixture
def call_api():
    """Make a call to the API, through the API client."""
    def call_client_method(api_instance, method: str, *args, **kwargs):
        """Call a method on the client, matching an endpoint of the API."""
        return getattr(api_instance, method)(*args, **kwargs)
    return call_client_method



@pytest.fixture
def test_client_method(call_api):
    """Make a call to the API and validate expected results."""
    def test_api_client_call(api_instance, method: str, input, assert_callback):
        """Call a method of the API client, and validate expected results."""
        result = call_api(api_instance, method, *input[0], **input[1])
        assert_callback(result)
    return test_api_client_call
