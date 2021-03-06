# Welcome to the Covid-19 Dashboard Documentation!



# Introduction

This Covid Dashboard Application was developped as part of my coursework for programming. It displays current coronavirus data, such as the number of infections in the past 7 days, the number of hospital cases, etc., as well as up to date news articles from various sources.

The application is built using Python, and uses Flask to run on a local server. It uses live data from the uk-covid19 API, and NewsAPI for news articles.



# Prerequisites


The application requires a version of Python that is at least 3.8.0 or above. 

Certain packages / modules are also required to be installed:
 * os
 * sched
 * time
 * datetime
 * requests
 * csv
 * json
 * logging

These can be installed via pip in the command line: ` $ pip install <package> `



# Installation


You can download the application directly from GitHub, at https://github.com/lbiragnet/covid_dashboard_lbiragnet by clicking "Download ZIP" and then extracting the files to the application of your choice.

The application is also available as a Python package on PyPi. It can be installed using pip in the command line:

``` $ pip install covid19_dashboard_lucbiragnet ```


# Getting Started


## Configuring the application

Once the application has been installed, it needs to be configured using your chosen location and API key. These are necessary to extract the correct data from the uk-covid19 api, and to provide access to the news api. You can register for an API key on https://newsapi.org/. This will usually look like a long sequence of different characters. Do not share your API key, as this might lead to you losing access to the news API.

If you have download the application from GitHub, navigate to the application folder named `covid19_dashboard_lbiragnet` and head over to `\src\config` and open `config.json`. This will open the application configuration file.

If installed using pip, the configuration file will most likely be under a different directory.

Enter your API key in quotation marks in the `API key` section.

The configuration file can be edited for covid data to correspond to the location of your choice: to do this, enter the name of your chosen city in quotation marks in the `location` section, which is set to `Exeter` by default. The `location type` section can also be modified. The full list of valid metrics for this section can be found in the uk-covid19 api documentation at https://coronavirus.data.gov.uk/details/developers-guide/main-api#methods-get. The `Output Format` section defines which data is requested to the uk-covid19 API. Note that modifying this section will require the source code to be changed in order to process the data accordingly.


## Running the application

Once the application has been configured with your API key and the location of your choice, navigate to the src folder via the command line. To run the application, type:

```$ python -m main```

The application will be run on a local server, and will be accessible in your browser at the address: http://127.0.0.1:5000/index.

The dashboard contains an updates section (on the left), a covid data section (in the center), and a news articles section (on the right). The bottom section also allows you to schedule updates for covid data and/or news articles.

Note that the dashboard will retain full functionality as long as it is being run. Exiting or interrupting the command line when the application is running will stop the execution. Any scheduled updates will be deleted.


## Covid Data

The Dashboard provides up-to-date covid data, including the following metrics:
 * The local 7-day infection rate
 * The national 7-day infection rate
 * The national number of hospital cases
 * The national number of cumulative deaths

These metrics can be modified in the configuration file, but it will also be necessary to change the source code in order to process different metrics, as well as the html code for the dashboard to correctly label the different data.


## Scheduling updates

The dashboard allows you to schedule updates to the covid data and news articles. If no updates have been scheduled, the left side of the dashboard will appear empty. To schedule an update, first enter the name of your update in the designated area. Then, enter the time at which you wish the update to occur in the designated area. You are then able to check three different options:
 * Update Covid data (updates the covid data using the uk covid-19 API)
 * Update news articles (updates the news articles using the newsAPI)
 * Repeat update (repeats the update every 24 hours)

Scheduled updates will then be displayed in the left section of the dashboard, and will be labelled using the name given to them by the user.

Checking certain options will schedule the relevant update (covid data or news articles) at the given time, and will repeat every 24 hours if "Repeat" is checked. Checking both the "Update Covid data" and "Update news articles" options will schedule a separate double update (covid data and news articles), which can be repeated. Hence there are three types of updates: covid data updates, news articles updates and double updates. Note that scheduling an update of a certain type at the same time as another of the same type will fail. When scheduling a double update, this applies if an update of any kind has already been scheduled at the same time.


## Repeating updates

If an update has been scheduled as a repeated update, the dashboard will schedule a (repeat) update with the same name as the initial update, 24 hours after the inital update is completed. Note that the dashboard will only generate a single repeated update: this avoids an infinite number of updates from being displayed on the dashboard. However, the repeated update will also repeat itself 24 hours later.


## Cancelling updates

Updates shown in the updates section can be cancelled by clicking the dismiss button. For repeated updates, both the update and its repetition will need to be cancelled in order for the "repetition" cycle to be cancelled


## Deleting news articles

The dashboard displays a list of 7 news articles on its right section, each of which contains a title and relevant content. The articles can be individually deleted by clicking the dismiss button. This will add a new article to the list, and this process can be repeated as many times as the number of articles received from the newsAPI (which is very large) if these are not updated, giving the user the possibility to consult multiple articles.


## Exiting the application

The application can be exited by terminating it in the command line (Ctrl + C for Windows), or by closing the command line.



# Testing

The application comes with a variety of tests designed to verify that the different modules are functioning correctly. Hence the `tests` folder within the application folder contains tests for multiple functions included in the application modules. The tests are grouped within modules, each containing test functions of one particular module.

Running the tests requires the `pytest` module, which can be installed using pip. To run the tests, open the command line navigate to the `src` folder within the `covid19-dashboard-lbiragnet` folder:

``` $ cd <path to the application folder>\covid19-dashboard-lbiragnet\src ```

Then type:

``` $ python -m pytest ```

After a few seconds, the tests will have completed and pytest will return a detailed report describing their outcomes and the potential errors which were encountered.



# Developer Documentation

The source code contains 4 Python modules:
 * main.py
 * covid_data_handler.py
 * covid_news_handling.py
 * time_calculations.py

The source code also includes:
 * A configuration file `config.json` 
 * A logging file `app.log`
 * A sample csv data file `nation_2021-10-28.csv`
 * Data files stored in the `datafiles` folder
 * An html template `index.html`
 * A PNG image stored in `\static\images`
 * Test files stored in `\tests`
 * The `__init__.py` file used to package the source code


## main module


NAME

    main - Main application module

DESCRIPTION

    This module runs a COVID-19 Dashboard application.
    It contains the main logic of the application.
    It also defines functions to schedule and remove updates, and add and remove news articles.

FUNCTIONS

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

DATA

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


## covid_data_handler module

NAME

    covid_data_handler - This module handles the covid data section of the dashboard

FUNCTIONS

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

DATA

    CONFIG_DATA = {'Covid Data Configuration': {'Location': 'Exeter', 'Loc...

    COVID_DATA_FILTERS = ['areaType=ltla', 'areaName=Exeter']

    OUTPUT_FORMAT = {'areaCode': 'areaCode', 'areaName': 'areaName', 'cumC...

    config_file = <_io.TextIOWrapper name='./config/config.json' mode='r' ...


## covid_news_handling module

NAME

    covid_news_handling - This module handles the news articles section of the dashboard

FUNCTIONS

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

DATA

    API_KEY = ''

    CONFIG_NEWS = {'Covid Data Configuration': {'Location': 'Exeter', 'Loc...

    config_file = <_io.TextIOWrapper name='./config/config.json' mode='r' ...

    news_articles = []


## time_calculations module


NAME

    time_calculations - This module includes functions used for calculations including time

FUNCTIONS

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



# Details


## Authors

 * Luc Biragnet (Python)
 * Matt Collison (HTML/Flask template)


## License

Copyright (c) [2021] [Luc Biragnet]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Acknowledgements

I would like to thank Matt Collison for his guidance and help throughout the project!
