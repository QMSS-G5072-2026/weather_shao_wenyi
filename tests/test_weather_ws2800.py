import weather_ws2800


def test_version_is_defined():
    assert isinstance(weather_ws2800.__version__, str)

"""
Test file for the weather station functions - Template

Copy this file to `test_weather.py` and replace every TODO with your own tests.
Keep `weather.py` in the same folder so the import below works.
"""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_ws2800 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


# TODO: add @pytest.mark.parametrize with at least 5 (celsius, expected) cases,
# including absolute zero itself.
@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0),            # freezing
        (100, 212.0),         # boiling
        (-40, -40.0),         # both scales meet
        (37, 98.6),           # body temperature (actual: 98.60000000000001)
        (-273.15, -459.67),   # absolute zero itself is allowed
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """TODO: One assertion (using pytest.approx) that works for every case."""
    """approx handles floating point error such as 98.60000000000001."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)

# TODO: add @pytest.mark.parametrize with at least 4 (bad_input, expected_error) cases.
@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("37", TypeError),       # string
        (None, TypeError),       # None
        (True, TypeError),       # bool is explicitly rejected
        (-273.16, ValueError),   # just below absolute zero
        (-500, ValueError),      # far below absolute zero
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """TODO: One pytest.raises block that works for every case."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)
    """Invalid inputs raise the documented exception type."""

def test_summarize_temperatures():
    """
    TODO: Use the Arrange / Act / Assert pattern to test a list that contains one NaN.
    Check all four keys of the returned dictionary.
    """
    # Arrange
    temps = [10.0, float("nan"), 20.0]
 
    # Act
    summary = summarize_temperatures(temps)
 
    # Assert
    assert summary["mean"] == pytest.approx(15.0)
    assert summary["min"] == 10.0
    assert summary["max"] == 20.0
    assert summary["n_missing"] == 1
    """NaN readings are excluded from the statistics and counted in n_missing."""

# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """TODO: Return the station DataFrame given in Part 2 of hw06.md."""
    """Unsorted raw readings with one missing and one implausible (999.0) temperature."""
    return pd.DataFrame(
        {
            "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
            "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
            "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
        }
    )

def test_raw_readings_fixture(raw_readings):
    """TODO: Check the fixture has the columns, number of rows, and missing values you expect."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1
    """The fixture has the expected columns, row count and one missing temperature."""

# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """TODO: Build the expected DataFrame by hand and compare with assert_frame_equal."""
    """Cleaning drops missing and implausible rows, adds temp_f, and sorts by station and date."""
    # Arrange: the NaN row (JFK 07-01) and the 999.0 row (CPK 07-02) are dropped;
    # survivors are sorted by station, then date, with a fresh 0..n-1 index
    expected = pd.DataFrame(
        {
            "station": ["CPK", "JFK", "LGA"],
            "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
            "temp_c": [25.0, 30.0, 28.0],
            "temp_f": [77.0, 86.0, 82.4],
        }
    )
 
    # Act
    result = clean_readings(raw_readings)
 
    # Assert
    assert_frame_equal(result, expected)

