_______________________
Developer Documentation
_______________________

===========
main module
===========

Name
****

::

    main - Main application module

Description
***********

::

    This module runs a COVID-19 Dashboard application.
    It contains the main logic of the application.
    It also defines functions to schedule and remove updates, and add and remove news articles.

Functions
*********

::

    add_news() -> list
        Adds a news article to the dashboard when one is deleted by the user

        The function goes through the news articles list pulled from the news API.
        If an article has not been deleted by the user and is not currently displayed,
        the function then adds it to the list of articles displayed on the dashboard.

    index() -> None
        Returns the html template as an interactive dashboard on a local server

        The function is triggered when the user accesses the application
        Updates schedulers are set to run.
        The function requests arguments from the url when the user interacts with the dashboard.
        The function schedule/cancels updates and adds/removes articles when prompted by the user.
        The function returns the html template with data from the APIs at http://127.0.0.1:5000/index

    remove_update(update: dict) -> list
        Removes an update that is deleted by the user from the list of updates

        The function checks if an update deleted by the user is in the list of updates.
        If it is in the list, the update is removed from the list.
        Arguments:
        | update -- dictionary containing details about an update (an item of the updates list)

    schedule_data_update(data_update_name: str, data_update_time: str, data_update_repeat: str) -> list
        Schedules a covid data update at a given time

        The function calculates the epoch time of the update given by the user.
        If there isn't already a covid data update scheduled at the same time,
        The planned update is added to the updates list and dictionary,
        And a scheduled event is added to the covid data updates scheduler.
        The function returns both the updates list and the covid data updates list.
        Arguments:
        | data_update_name -- the name of the update given by the user
        | data_update_time -- the time of the update given by the user
        | data_update_repeat -- set to "repeat" if the update is to be repeated

    schedule_double_updates(update_name: str, update_time: str, update_repeat: str) -> list
        Schedules a double (news and covid data) update at a given time

        The function calculates the epoch time of the update given by the user.
        If there isn't already a double update scheduled at the same time,
        The planned update is added to the updates list and dictionary,
        And a scheduled event is added to the double updates scheduler.
        The function returns both the updates list and the double updates list.
        Arguments:
        | update_name -- the name of the update given by the user
        | update_time -- the time of the update given by the user
        | update_repeat -- set to "repeat" if the update is to be repeated

    schedule_news_update(news_update_name: str, news_update_time: str, news_update_repeat: str) -> list
        Schedules a news update at a given time

        The function calculates the epoch time of the update given by the user.
        If there isn't already a news update scheduled at the same time,
        The planned update is added to the updates list and dictionary,
        And a scheduled event is added to the news updates scheduler.
        The function returns both the updates list and the news updates list.
        Arguments:
        | news_update_name -- the name of the update given by the user
        | news_update_time -- the time of the update given by the user
        | news_update_repeat -- set to "repeat" if the update is to be repeated

    update_covid_data()
        Updates covid data

        The function requests updated data from the covid-19 API.
        Variables containing the current covid data are redefined to update the data.

    update_data_and_news() -> None
        Combines the update_covid_data and update_news_articles functions into one function

    update_news_articles() -> list
        Updates news articles

        The function requests updated news articles from the news API.
        The news variable displaying the articles is redefined to update the articles.

Data
****

::

    CANCELED_DATA_UPDATES = []

    CANCELED_DOUBLE_UPDATES = []

    CANCELED_NEWS_UPDATES = []

    DATA_UPDATE_SCHEDULER = <sched.scheduler object>

    DOUBLE_UPDATE_SCHEDULER = <sched.scheduler object>

    NEWS_UPDATE_SCHEDULER = <sched.scheduler object>

    SCHEDULED_DATA_UPDATES = []

    SCHEDULED_DOUBLE_UPDATES = []

    SCHEDULED_NEWS_UPDATES = []

    UPDATES_DICT = {}

    UPDATES_LIST = []

    app = <Flask 'main'>

    request = <LocalProxy unbound>


=========================
covid_data_handler module
=========================

Name
****

::

    covid_data_handler - This module handles the covid data section of the dashboard

Functions
*********

::

    covid_API_request(location: str = 'Exeter', location_type: str = 'ltla') -> <module 'json' from 'C:\\Users\\luc biragnet\\AppData\\Local\\Programs\\Python\\Python39\\lib\\json\\__init__.py'>
        Retrieve live covid data from the uk covid-19 API

        The function requests data from the covid-19 API using the given arguments
        The response is returned in the json format
        Arguments:
        | location -- the location given by the user
        | location_type -- the location type given by the user

    get_covid_data() -> <module 'json' from 'C:\\Users\\luc biragnet\\AppData\\Local\\Programs\\Python\\Python39\\lib\\json\\__init__.py'>
        Retrieve live covid data from the uk covid-19 API

        The function requests data from the covid-19 API the filters and structure arguments.
        These can be modified by the user from the configuration file.
        The function makes a request for local data and another for national data.
        Both responses are then returned in the json format.

    parse_csv_data(csv_filename: str) -> list
        Return the data from the csv file as a list

        csv_filename is a csv file
        The function turns the data from this file into a list
        Each item of the list is a list, the first of which specifies how the data is formatted.
        Each further item corresponds to a particular day (following the most recent order)

    process_covid_csv_data(covid_csv_data: list) -> int
        Process the parsed covid csv data to return basic data to the user

        The function returns the number of cases in the past 7 days,
        The number of hospital cases, and the number of cumulative deaths
        Arguments:
        | covid_csv_data -- list containing the covid data as would be returned by parse_csv_data

    process_live_covid_data(local_data: dict, national_data: dict) -> int
        Process live covid data to return basic data to the user

        The function calculates the number of local cases in the past 7 days.
        The function calculates the number of national cases in the past 7 days.
        The function retrieves the most recent number of nationwide hospital cases.
        The function retrieves the most recent number of nationwide cumulative deaths.
        The function returns these numbers.
        Arguments:
        | local_data -- local data in json format as returned by the get_covid_data function
        | national_data -- national data in json format as returned by the get_covid_data function

    schedule_covid_updates(update_interval: str, update_name: str)
        Schedule a covid data update
        The function creates a scheduler object.
        An event is added at a given time interval, to update the data.
        The function returns the name of the update, and the time interval at which it is scheduled
        Arguments:
        | update_interval -- the interval time of the update as given by the user
        | update_name -- the name of the scheduled update as given by the user

    update_data() -> <module 'json' from 'C:\\Users\\luc biragnet\\AppData\\Local\\Programs\\Python\\Python39\\lib\\json\\__init__.py'>
        Update covid data for a scheduled update

        The function uses the covid_API_request function to update the data.


Data
****

::

    CONFIG_DATA = {'Covid Data Configuration': {'Location': 'Exeter', 'Loc...
    COVID_DATA_FILTERS = ['areaType=ltla', 'areaName=Exeter']
    OUTPUT_FORMAT = {'areaCode': 'areaCode', 'areaName': 'areaName', 'cumC...
    config_file = <_io.TextIOWrapper name='./config/config.json' mode='r' ...




==========================
covid_news_handling module
==========================

Name
****

::

    covid_news_handling - This module handles the news articles section of the dashboard

Functions
*********

::

    news_API_request(covid_terms: str = 'Covid COVID-19 coronavirus') -> dict
        Request news articles from the news api in the json format

        The covid_terms argument is formatted for the API request: <term> OR <term> OR <term>...
        The function requests news articles whose titles include relevant terms as given in the argument
        The articles are sorted by popularity and are at most from the previous day
        The response is returned in the json format.
        Arguments:
        | covid_terms -- terms to look for in article titles when retrieving articles from the API

    select_articles(news_dict_list: dict) -> list
        Select a limited number of articles which have not been deleted by the user

        The function returns a list of 7 articles from the API response returned by news_API_request
        It is also executed when the page is refreshed, allowing the removal of deleted articles.
        Arguments:
        | news_dict_list -- list of dictionaries (news articles), as returned by news_API_request

    update_news(article) -> list
        Updates news articles

        The function adds a news article to the list of current articles
        The list of updated articles is returned.

Data
****

::

    API_KEY = ''
    CONFIG_NEWS = {'Covid Data Configuration': {'Location': 'Exeter', 'Loc...
    config_file = <_io.TextIOWrapper name='./config/config.json' mode='r' ...
    news_articles = []





========================
time_calculations module
========================

Name
****

::

    time_calculations - This module includes functions used for calculations including time

Functions
*********

::

    calc_update_epoch_interval(update_time_hhmm: str) -> float
        Calculate interval between current epoch time and update epoch time

    calc_update_interval(update_time_hhmm: str) -> int
        Calculates interval in seconds between current time and scheduled time for an update

    current_time_hhmm() -> str
        Returns local time in the HH:MM format

    hhmm_to_seconds(hhmm: str) -> int
        Converts time in the HH:MM format to seconds

    hours_to_minutes(hours: str) -> int
        Converts hours to minutes

    minutes_to_seconds(minutes: str) -> int
        Converts minutes to seconds