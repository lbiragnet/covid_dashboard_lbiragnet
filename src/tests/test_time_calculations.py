import time

from time_calculations import current_time_hhmm
from time_calculations import minutes_to_seconds
from time_calculations import hours_to_minutes
from time_calculations import hhmm_to_seconds
from time_calculations import calc_update_interval
from time_calculations import calc_update_epoch_interval

def test_current_time_hhmm():
    current_time = current_time_hhmm()
    assert isinstance(current_time, str)
    actual_time = time.strftime("%H:%M", time.localtime())
    assert current_time == actual_time


def test_minutes_to_seconds():
    seconds = minutes_to_seconds(60)
    assert isinstance(seconds, int)
    assert seconds == 3600

def test_hours_to_minutes():
    minutes = hours_to_minutes(60)
    assert isinstance(minutes, int)
    assert minutes == 3600


def test_hhmm_to_seconds():
    seconds = hhmm_to_seconds("15:15")
    assert isinstance(seconds, int)
    assert seconds == 54900

def test_calc_update_interval():
    interval = calc_update_interval("15:15")
    assert isinstance(interval, int)

def test_calc_update_epoch_interval():
    current_epoch_time = round(time.time(), 0)
    epoch_time = calc_update_epoch_interval("18:15")
    assert isinstance(epoch_time, float)
    assert epoch_time >= current_epoch_time