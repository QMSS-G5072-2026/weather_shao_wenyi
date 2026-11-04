# read version from installed package
from importlib.metadata import version
__version__ = version("weather_ws2800")

from .weather_ws2800 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)