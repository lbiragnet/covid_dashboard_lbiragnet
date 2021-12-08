'''Main application module

    This module runs a COVID-19 Dashboard application.
    It contains the main logic of the application.
    It also defines functions to schedule and remove updates, and add and remove news articles.
    '''


# IMPORT MODULES

import sched
import time
import logging
import os.path

from flask import Flask, request, render_template

from time_calculations import calc_update_epoch_interval
from covid_data_handler import get_covid_data, process_live_covid_data
from covid_news_handling import news_API_request, select_articles


# FLASK OBJECT

app = Flask(__name__)


# GLOBAL VARIABLES FOR UPDATES SECTION

SCHEDULED_DATA_UPDATES = []         # List of all covid data updates
SCHEDULED_NEWS_UPDATES = []         # List of all news updates
SCHEDULED_DOUBLE_UPDATES = []       # List of all double updates (news + covid data)
UPDATES_LIST = []                   # List of all updates
UPDATES_DICT = {}                   # Dictionary of scheduled events corresponding to updates
CANCELED_DATA_UPDATES = []          # List of canceled covid data updates
CANCELED_NEWS_UPDATES = []          # List of canceled news updates
CANCELED_DOUBLE_UPDATES = []        # List of canceled double updates (news + covid data)


# SCHEDULER OBJECTS FOR UPDATES SECTION

NEWS_UPDATE_SCHEDULER = sched.scheduler(time.time, time.sleep)
DATA_UPDATE_SCHEDULER = sched.scheduler(time.time, time.sleep)
DOUBLE_UPDATE_SCHEDULER = sched.scheduler(time.time, time.sleep)


# CONFIGURE LOGGING

logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.join("./logs/", "app.log"),
                    filemode="a",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S")


def update_covid_data():
    ''' Updates covid data

    The function requests updated data from the covid-19 API.
    Variables containing the current covid data are redefined to update the data. '''

    try:
        local_data, national_data = get_covid_data()
        local_name, local_7_day_cases, nation_name, national_7_day_cases, number_hospital_cases, cumulative_deaths = process_live_covid_data(local_data, national_data)
        logging.debug("Covid data has been updated")
    except:
        logging.critical("Unable to reach the uk covid-19 API")
    return local_name, local_7_day_cases, nation_name, national_7_day_cases, number_hospital_cases, cumulative_deaths


def update_news_articles()->list:
    ''' Updates news articles

    The function requests updated news articles from the news API.
    The news variable displaying the articles is redefined to update the articles. '''

    try:
        requested_news = news_API_request()
        NEWS = select_articles(requested_news)
        logging.debug("News articles have been updated")
    except:
        logging.critical("Unable to reach the news API")
    return NEWS


def update_data_and_news()->None:
    ''' Combines the update_covid_data and update_news_articles functions into one function '''

    update_covid_data()
    update_news_articles()


def add_news()->list:
    ''' Adds a news article to the dashboard when one is deleted by the user

    The function goes through the news articles list pulled from the news API.
    If an article has not been deleted by the user and is not currently displayed,
    the function then adds it to the list of articles displayed on the dashboard. '''

    for article in REQUESTED_NEWS["articles"]:
        if article["title"] not in DELETED_NEWS and article not in NEWS:
            NEWS.append(article)
            break
    return NEWS


def remove_update(update:dict)->list:
    ''' Removes an update that is deleted by the user from the list of updates

    The function checks if an update deleted by the user is in the list of updates.
    If it is in the list, the update is removed from the list.
    Arguments:
    | update -- dictionary containing details about an update (an item of the updates list) '''

    if update in UPDATES_LIST:
        UPDATES_LIST.remove(update)
        logging.info("Update has been deleted by user")
    return UPDATES_LIST


def schedule_data_update(data_update_name:str, data_update_time:str, data_update_repeat:str)->list:
    ''' Schedules a covid data update at a given time

    The function calculates the epoch time of the update given by the user.
    If there isn't already a covid data update scheduled at the same time,
    The planned update is added to the updates list and dictionary,
    And a scheduled event is added to the covid data updates scheduler.
    The function returns both the updates list and the covid data updates list.
    Arguments:
    | data_update_name -- the name of the update given by the user
    | data_update_time -- the time of the update given by the user
    | data_update_repeat -- set to "repeat" if the update is to be repeated '''

    data_update_interval = calc_update_epoch_interval(data_update_time)
    # Calculate epoch time of the update
    if data_update_time not in SCHEDULED_DATA_UPDATES:
        # If the update time is not already in the list of scheduled covid data updates
        UPDATES_LIST.append({"title":data_update_name,
                             "update_time": data_update_time,
                             "update_interval": data_update_interval,
                             "content": "update covid data",
                             "repeat_update":data_update_repeat})
        SCHEDULED_DATA_UPDATES.append(data_update_time)
        # The update is added to the list of all updates and the list of covid data updates
        scheduled_update=DATA_UPDATE_SCHEDULER.enterabs(data_update_interval, 1, update_covid_data)
        # An event is scheduled to update the data at a given time
        UPDATES_DICT[data_update_name] = scheduled_update
        # The event is added to a dictionary in case it is cancelled later
    else:
        # If there already is a covid data update scheduled at this time
        logging.error("There is already a covid data update scheduled at this time")
    return SCHEDULED_DATA_UPDATES, UPDATES_LIST


def schedule_news_update(news_update_name:str, news_update_time:str, news_update_repeat:str)->list:
    ''' Schedules a news update at a given time

    The function calculates the epoch time of the update given by the user.
    If there isn't already a news update scheduled at the same time,
    The planned update is added to the updates list and dictionary,
    And a scheduled event is added to the news updates scheduler.
    The function returns both the updates list and the news updates list.
    Arguments:
    | news_update_name -- the name of the update given by the user
    | news_update_time -- the time of the update given by the user
    | news_update_repeat -- set to "repeat" if the update is to be repeated '''

    news_update_interval = calc_update_epoch_interval(news_update_time)
    # Calculate epoch time of the update
    if news_update_time not in SCHEDULED_NEWS_UPDATES:
        # If the update time is not already in the list of scheduled news updates
        SCHEDULED_NEWS_UPDATES.append(news_update_time)
        UPDATES_LIST.append({"title":news_update_name,
                             "update_time": news_update_time,
                             "update_interval": news_update_interval,
                             "content": "update news",
                             "repeat_update": news_update_repeat})
        # The update is added to the list of all updates and the list of news updates
        scheduled_update=NEWS_UPDATE_SCHEDULER.enterabs(news_update_interval,1,update_news_articles)
        # An event is scheduled to update the news at a given time
        UPDATES_DICT[news_update_name] = scheduled_update
        # The event is added to a dictionary in case it is cancelled later
    else:
        # If there already is a news update scheduled at this time
        logging.error("There is already a news update scheduled at this time")
    return SCHEDULED_NEWS_UPDATES, UPDATES_LIST


def schedule_double_updates(update_name:str, update_time:str, update_repeat:str)->list:
    ''' Schedules a double (news and covid data) update at a given time

    The function calculates the epoch time of the update given by the user.
    If there isn't already a double update scheduled at the same time,
    The planned update is added to the updates list and dictionary,
    And a scheduled event is added to the double updates scheduler.
    The function returns both the updates list and the double updates list.
    Arguments:
    | update_name -- the name of the update given by the user
    | update_time -- the time of the update given by the user
    | update_repeat -- set to "repeat" if the update is to be repeated '''

    double_update_interval = calc_update_epoch_interval(update_time)
    # Calculate epoch time of the update
    if update_time in SCHEDULED_NEWS_UPDATES:
        # If there already is a news update scheduled at this time
        logging.error("There is already a news update scheduled at this time")
    elif update_time in SCHEDULED_DATA_UPDATES:
        # If there already is a covid data update scheduled at this time
        logging.error("There is already a covid data update scheduled at this time")
    elif update_time in SCHEDULED_DOUBLE_UPDATES:
        # If there already is a double (news and covid data) update scheduled at this time
        logging.error("There is already a double update scheduled at this time")
    else:
        # If the update time is not already in a list of scheduled updates
        SCHEDULED_DOUBLE_UPDATES.append(update_time)
        UPDATES_LIST.append(({"title":update_name,
                              "update_time": update_time,
                              "update_interval": double_update_interval,
                              "content": "update covid data and news",
                              "repeat_update": update_repeat}))
        # The update is added to the list of all updates and the list of double updates
        scheduled_update = DOUBLE_UPDATE_SCHEDULER.enterabs(double_update_interval, 1, update_data_and_news)
        # An event is scheduled to update the news and covid data at a given time
        UPDATES_DICT[update_name] = scheduled_update
        # The event is added to a dictionary in case it is cancelled later
    return SCHEDULED_DOUBLE_UPDATES, UPDATES_LIST







@app.route("/index", methods=["POST", "GET"])
def index()->None:
    ''' Returns the html template as an interactive dashboard on a local server

    The function is triggered when the user accesses the application
    Updates schedulers are set to run.
    The function requests arguments from the url when the user interacts with the dashboard.
    The function schedule/cancels updates and adds/removes articles when prompted by the user.
    The function returns the html template with data from the APIs at http://127.0.0.1:5000/index
    '''



    # UPDATES SECTION

    # Run the schedulers with blocking set to False
    DATA_UPDATE_SCHEDULER.run(blocking=False)
    NEWS_UPDATE_SCHEDULER.run(blocking=False)
    DOUBLE_UPDATE_SCHEDULER.run(blocking=False)


    # Request arguments from the url to schedule or cancel an update
    update_name = request.args.get("two")
    update_data = request.args.get("covid-data")
    update_news = request.args.get("news")
    update_time = str(request.args.get("update")).replace("%3A", ":")
    update_repeat = request.args.get("repeat")
    cancel_update = request.args.get("update_item")
    delete_article = request.args.get("notif")


    # Schedule updates based on the received arguments
    if update_name:
        # If the user has scheduled an update
        if update_data=="covid-data" and update_news=="news":
            # If the user has checked both the "update covid data" and "update news" checkboxes
            schedule_double_updates(update_name, update_time, update_repeat)
            logging.info("User is attempting to schedule a  double update")
        elif update_data:
            # If the user has only checked the "update covid data" checkbox
            schedule_data_update(update_name, update_time, update_repeat)
            logging.info("User is attempting to schedule a covid data update")
        elif update_news:
            # If the user has only checked the "update news" checkbox
            schedule_news_update(update_name, update_time, update_repeat)
            logging.info("User is attempting to schedule a news update")


    # Repeat updates
    if cancel_update is None:
        # If the user is not cancelling an update
        for update in UPDATES_LIST:
            current_epoch_time = time.time()
            # Calculate current epoch time
            if round((update["update_interval"] - current_epoch_time), 0) < 86400:
                # If a given update will happen in less than 24 hours
                repeat_status = update["repeat_update"]
                if repeat_status == "repeat":
                    # If an update has been set to "repeat" by the user
                    if update["content"] == "update covid data":
                        scheduled_update = DATA_UPDATE_SCHEDULER.enterabs(update["update_interval"] + 86400.0, 1, update_data)
                        UPDATES_DICT[update["title"]+" (repeat)"] = scheduled_update
                    elif update["content"] == "update news":
                        scheduled_update = NEWS_UPDATE_SCHEDULER.enterabs(update["update_interval"] + 86400.0, 1, update_news)
                        UPDATES_DICT[update["title"]+" (repeat)"] = scheduled_update
                    elif update["content"] == "update covid data and news":
                        scheduled_update = DOUBLE_UPDATE_SCHEDULER.enterabs(update["update_interval"] + 86400.0, 1, update_data_and_news)
                        UPDATES_DICT[update["title"]+" (repeat)"] = scheduled_update
                    # An event is scheduled 24 hours after the update, in order to repeat it
                    UPDATES_LIST.append({"title":update["title"]+" (repeat)",
                                         "update_time": update["update_time"],
                                         "update_interval": (update["update_interval"] + 86400.0),
                                         "content": update["content"],
                                         "repeat_update:": update["repeat_update"]})
                    # The repeated update is added to the list of updates
                    logging.debug("A repeated update has been added")
            break


    # Cancel scheduled updates
    if cancel_update:
        # If the user is trying to cancel an update
        logging.info("User is attempting to cancel an update")
        for update in UPDATES_LIST:
            if cancel_update==update["title"] and update["content"]=="update covid data and news":
                # If the update in question is a double update
                CANCELED_DOUBLE_UPDATES.append(cancel_update)
                update_to_cancel = UPDATES_DICT[cancel_update]
                # Accesses the event corresponding to the update in the scheduler queue
                if update_to_cancel in DOUBLE_UPDATE_SCHEDULER.queue:
                    # Check if the double updates scheduler queue contains the update to cancel
                    DOUBLE_UPDATE_SCHEDULER.cancel(update_to_cancel)
                    logging.info("A double update has been removed from queue")
                    # Cancels the event from the double update scheduler
                UPDATES_LIST.remove(update)
            if update["title"] == cancel_update and update["content"] == "update covid data":
                # If the update in question is a covid data update
                CANCELED_DATA_UPDATES.append(cancel_update)
                update_to_cancel = UPDATES_DICT[cancel_update]
                # Check if the data update scheduler queue contains the update to cancel
                if update_to_cancel in DATA_UPDATE_SCHEDULER.queue:
                    DATA_UPDATE_SCHEDULER.cancel(update_to_cancel)
                    logging.info("A covid data update has been removed from queue")
                    # Cancels the event from the double update scheduler
                UPDATES_LIST.remove(update)
            elif update["title"] == cancel_update and update["content"] == "update news":
                # If the update in question is a covid data update
                CANCELED_NEWS_UPDATES.append(cancel_update)
                update_to_cancel = UPDATES_DICT[cancel_update]
                # Check if the news update scheduler queue contains the update to cancel
                if update_to_cancel in NEWS_UPDATE_SCHEDULER.queue:
                    NEWS_UPDATE_SCHEDULER.cancel(update_to_cancel)
                    logging.info("A news update has been removed from queue")
                    # Cancels the event from the double update scheduler
                UPDATES_LIST.remove(update)


    # Remove past updates from the dashboard
    for update in UPDATES_LIST:
        current_epoch_time = round(time.time())
        # Calculate current epoch time
        if update["update_interval"] <= current_epoch_time:
            # If the update was scheduled for a time prior to current epoch time
            UPDATES_LIST.remove(update)
            logging.debug("A past update has been removed")



    # NEWS ARTICLES SECTION


    # Remove and add news articles
    if delete_article is not None:
        # If the user has deleted a news article
        delete_article_title = str(delete_article).replace("+", " ")
        # Creates a string containing the article title
        if delete_article_title not in DELETED_NEWS:
            # If the article in question has not already been deleted
            DELETED_NEWS.append(delete_article_title)
        for article in NEWS:
            if article["title"] == delete_article_title:
                # If the article title is found in the list of displayed articles
                NEWS.remove(article)
                logging.info("An article has been deleted")
                # Remove the article from the list
                add_news()
                logging.info("An article has been added")
                # Add another article to replace it



    # LOGGING UPDATES LIST AND SCHEDULER QUEUES

    logging.debug("List of updates: %s", UPDATES_LIST)
    logging.debug("News updates scheduler queue: %s", NEWS_UPDATE_SCHEDULER.queue)
    logging.debug("Covid data update scheduler queue: %s", DATA_UPDATE_SCHEDULER.queue)
    logging.debug("Double update scheduler queue: %s", DOUBLE_UPDATE_SCHEDULER.queue)



    # RETURN THE INDEX.HTML TEMPLATE


    return(render_template("index.html",
                           title="COVID-19 updates",
                           news_articles=NEWS,
                           location=local_name,
                           local_7day_infections=local_7_day_cases,
                           nation_location=nation_name,
                           national_7day_infections=national_7_day_cases,
                           hospital_cases=number_hospital_cases,
                           deaths_total=cumulative_deaths,
                           updates=UPDATES_LIST,
                           image="virus.png"))
    # The html template is embedded with the data from the APIs, and returned by the function



# RUN THE APPLICATION

if __name__ == "__main__":
    try:
        local_data, national_data = get_covid_data()
        local_name, local_7_day_cases, nation_name, national_7_day_cases, number_hospital_cases, cumulative_deaths = process_live_covid_data(local_data, national_data)
    except:
        logging.critical("")
    # Start the application with initial covid data
    try:
        REQUESTED_NEWS = news_API_request()
        NEWS = select_articles(REQUESTED_NEWS)
    except:
        logging.critical("Unable to reach the news API")
    DELETED_NEWS = []
    app.run()
    # Run the application
