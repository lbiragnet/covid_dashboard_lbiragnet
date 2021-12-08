''' This module handles the covid data section of the dashboard '''


# IMPORT LIBRARIES

import csv
import json
import sched
import time
import os.path

from uk_covid19 import Cov19API



# HANDLE THE CONFIGURATION FILE

with open(os.path.join("./config/", "config.json"), "r", encoding="utf-8") as config_file:
    # Open the configuration file and retrieve relevant settings
    CONFIG_DATA = json.load(config_file)
    COVID_DATA_FILTERS = [f'areaType={CONFIG_DATA["Covid Data Configuration"]["Location Type"]}',
                          f'areaName={CONFIG_DATA["Covid Data Configuration"]["Location"]}']
    OUTPUT_FORMAT = CONFIG_DATA["Covid Data Configuration"]["Output Format"]



# THE FOLLOWING FUNCTIONS ARE NOT USED IN THE APPLICATION

def parse_csv_data(csv_filename:str)->list:
    ''' Return the data from the csv file as a list

    csv_filename is a csv file
    The function turns the data from this file into a list
    Each item of the list is a list, the first of which specifies how the data is formatted.
    Each further item corresponds to a particular day (following the most recent order)'''

    with open(csv_filename, newline="", encoding="utf-8") as csv_data:
        csv_reader = csv.reader(csv_data)
        data_list = list(csv_reader)
    return data_list


def process_covid_csv_data(covid_csv_data:list)->int:
    ''' Process the parsed covid csv data to return basic data to the user

    The function returns the number of cases in the past 7 days,
    The number of hospital cases, and the number of cumulative deaths
    Arguments:
    | covid_csv_data -- list containing the covid data as would be returned by parse_csv_data '''

    # Calculate number of cases in the past 7 days based on latest data
    cases_past_7_days = 0
    past_days_count = 0
    for day in covid_csv_data[3:]:
        # The data seems to be incomplete for the first two entries
        if day[6] != "":
            cases_past_7_days += int(day[6])
            past_days_count += 1
        if past_days_count == 7:
            break
    # Calculate the number of hospital cases based on latest data
    for day in covid_csv_data[1:]:
        if day[5] != "":
            hospital_cases = int(day[5])
            break
    # Calculate the number of cumulative deaths based on latest data
    for day in covid_csv_data[1:]:
        if day[4] != "":
            cumulative_deaths = int(day[4])
            break
    return cases_past_7_days, hospital_cases, cumulative_deaths


def covid_API_request(location:str="Exeter", location_type:str="ltla")->json:
    ''' Retrieve live covid data from the uk covid-19 API

    The function requests data from the covid-19 API using the given arguments
    The response is returned in the json format
    Arguments:
    | location -- the location given by the user
    | location_type -- the location type given by the user'''

    covid_data_api = Cov19API(filters = [f"areaType={location_type}",
                                         f"areaName={location}"],
                                         structure=OUTPUT_FORMAT)
    covid_data = covid_data_api.get_json()
    return covid_data


def update_data()->json:
    ''' Update covid data for a scheduled update

    The function uses the covid_API_request function to update the data. '''

    data_update = covid_API_request()
    return data_update


def schedule_covid_updates(update_interval:str, update_name:str):
    ''' Schedule a covid data update
    The function creates a scheduler object.
    An event is added at a given time interval, to update the data.
    The function returns the name of the update, and the time interval at which it is scheduled
    Arguments:
    | update_interval -- the interval time of the update as given by the user
    | update_name -- the name of the scheduled update as given by the user '''

    covid_updates = sched.scheduler(time.time, time.sleep)
    update = covid_updates.enter(float(update_interval), 1, update_data)
    covid_updates.run()
    return update_name, update_interval



# THE FOLLOWING FUNCTIONS ARE USED IN THE APPLICATION

def get_covid_data()->json:
    ''' Retrieve live covid data from the uk covid-19 API

    The function requests data from the covid-19 API the filters and structure arguments.
    These can be modified by the user from the configuration file.
    The function makes a request for local data and another for national data.
    Both responses are then returned in the json format. '''
    
    local_api = Cov19API(filters=COVID_DATA_FILTERS, structure=OUTPUT_FORMAT)
    national_api = Cov19API(filters=['areaType=nation',
                                     f'areaName={CONFIG_DATA["Covid Data Configuration"]["Nation"]}'],
                                     structure=OUTPUT_FORMAT)
    local_data = local_api.get_json()
    national_data = national_api.get_json()
    local_data_file = open(os.path.join("./datafiles/", "local_data.json"), "w", encoding="utf-8")
    local_data_file.write(json.dumps(local_data, sort_keys=False, indent=4))
    national_data_file = open(os.path.join("./datafiles/", "national_data.json"), "w", encoding="utf-8")
    national_data_file.write(json.dumps(national_data, sort_keys=False, indent=4))
    return local_data, national_data


def process_live_covid_data(local_data: dict, national_data: dict)->int:
    ''' Process live covid data to return basic data to the user

    The function calculates the number of local cases in the past 7 days.
    The function calculates the number of national cases in the past 7 days.
    The function retrieves the most recent number of nationwide hospital cases.
    The function retrieves the most recent number of nationwide cumulative deaths.
    The function returns these numbers.
    Arguments:
    | local_data -- local data in json format as returned by the get_covid_data function
    | national_data -- national data in json format as returned by the get_covid_data function '''

    # Retrieve location name
    local_name = local_data["data"][0]["areaName"]
    # Calculate local 7-day cases
    local_7_day_cases = 0
    for i in range(7):
        local_7_day_cases += local_data["data"][i]["newCasesByPublishDate"]
    # Retrieve nation name
    nation_name = national_data["data"][0]["areaName"]
    # Calculate national 7-day cases
    national_7_day_cases = 0
    for i in range (7):
        national_7_day_cases += national_data["data"][i]["newCasesByPublishDate"]
    # Retrieve number of nationwide hospital cases
    hospital = str(national_data["data"][0]["hospitalCases"])
    if hospital == "None":
        # Access the most recent available data
        number_hospital_cases = "Hospital cases: " + str(national_data["data"][1]["hospitalCases"])
    else:
        number_hospital_cases = "Hospital cases: " + str(national_data["data"][0]["hospitalCases"])
    # Retrieve number of nationwide cumulative deaths
    deaths = str(national_data["data"][0]["cumDeaths28DaysByDeathDate"])
    if deaths == "None":
        # Access the most recent available data
        cumulative_deaths = "Total deaths: " + str(national_data["data"][1]["cumDeaths28DaysByDeathDate"])
    else:
        cumulative_deaths = "Hospital cases: " + str(national_data["data"][0]["hospitalCases"])
    return local_name, local_7_day_cases, nation_name, national_7_day_cases, number_hospital_cases, cumulative_deaths
