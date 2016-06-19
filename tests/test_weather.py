"""Tests of the weather module."""
import datetime

import weather


def test_weather_date_generation_defaults_to_most_recent():

    current_datetime = datetime.datetime(2016, 9, 6, 13, 4, 23)
    expected_datetime = datetime.datetime(2016, 9, 6, 13, 0, 0)

    assert weather.file_date(start=current_datetime) == expected_datetime


def test_weather_date_generation_can_step_back():

    current_datetime = datetime.datetime(2016, 9, 6, 13, 29, 23)
    expected_datetime = datetime.datetime(2016, 9, 6, 13, 12, 0)

    assert weather.file_date(start=current_datetime, steps=2) == expected_datetime


def test_weather_date_generation_rounds_down():

    current_datetime = datetime.datetime(2016, 9, 6, 13, 0, 0)
    expected_datetime = datetime.datetime(2016, 9, 6, 12, 48, 0)

    assert weather.file_date(start=current_datetime, steps=2) == expected_datetime


def test_weather_image_filename_is_from_date():

    current_datetime = datetime.datetime(2016, 9, 6, 13, 12, 19)
    expected_filename = 'IDR763.T.201609061312.png'

    assert weather.filename(current_datetime) == expected_filename
