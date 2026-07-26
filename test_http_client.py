from transport.http_client import HTTPClient


def test_client_creation():
    client = HTTPClient()

    assert client.timeout == 10


def test_custom_timeout():
    client = HTTPClient(timeout=5)

    assert client.timeout == 5


def test_network_error_handling():
    client = HTTPClient(timeout=1)

    try:
        client.get(
            "http://invalid.invalid"
        )
        assert False

    except ConnectionError:
        assert True


if __name__ == "__main__":
    test_client_creation()
    test_custom_timeout()
    test_network_error_handling()

    print("HTTPClient tests PASSED ✅")
