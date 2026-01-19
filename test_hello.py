from hello import hello_world


def test_hello_world_returns_expected_greeting() -> None:
    result = hello_world()
    assert result == "Hello from Telnyx supervisor orchestration!"


def test_hello_world_returns_string_type() -> None:
    result = hello_world()
    assert isinstance(result, str)
