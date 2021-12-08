''' This module includes functions used for calculations including time '''


# IMPORT MODULES

import time



# TIME RELATED FUNCTIONS

def current_time_hhmm()->str:
    ''' Returns local time in the HH:MM format '''

    local_time = time.localtime()
    current_time = time.strftime("%H:%M", local_time)
    return current_time


def minutes_to_seconds(minutes:str)->int:
    """ Converts minutes to seconds """

    return int(minutes)*60


def hours_to_minutes(hours:str)->int:
    """ Converts hours to minutes """

    return int(hours)*60


def hhmm_to_seconds(hhmm:str)->int:
    ''' Converts time in the HH:MM format to seconds '''

    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])


def calc_update_interval(update_time_hhmm:str)->int:
    ''' Calculates interval in seconds between current time and scheduled time for an update '''

    current_time_sec = hhmm_to_seconds(current_time_hhmm())
    update_time_sec = hhmm_to_seconds(update_time_hhmm)
    if update_time_sec >= current_time_sec:
        update_interval_sec = update_time_sec - current_time_sec
        # Subtract current time from update time if both are in the same day
    else:
        update_interval_sec = (86400 - current_time_sec) + update_time_sec
        # Calculate interval if current time and update time are not on the same day
    return update_interval_sec


def calc_update_epoch_interval(update_time_hhmm:str)->float:
    ''' Calculate interval between current epoch time and update epoch time '''

    time_since_epoch = round(time.time(), 0)
    update_time_since_epoch = calc_update_interval(update_time_hhmm) + time_since_epoch
    return update_time_since_epoch
