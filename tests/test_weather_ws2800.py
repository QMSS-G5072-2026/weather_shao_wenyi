import weather_ws2800


def test_version_is_defined():
    assert isinstance(weather_ws2800.__version__, str)
