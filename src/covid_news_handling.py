''' This module handles the news articles section of the dashboard '''


# IMPORT LIBRARIES

import json
import datetime
import os.path
import requests




# HANDLE THE CONFIGURATION FILE

with open(os.path.join("./config/", "config.json"), "r", encoding="utf-8") as config_file:
    # Open the configuration file and retrieve relevant settings
    CONFIG_NEWS = json.load(config_file)
    API_KEY = CONFIG_NEWS["News Section Configuration"]["APIkey"]


# GLOBAL LIST OF NEWS ARTICLES (NOT USED IN THE APPLICATION)
news_articles = []



# NEWS RELATED FUNCTIONS

def news_API_request(covid_terms:str="Covid COVID-19 coronavirus")->dict:
    '''Request news articles from the news api in the json format

    The covid_terms argument is formatted for the API request: <term> OR <term> OR <term>...
    The function requests news articles whose titles include relevant terms as given in the argument
    The articles are sorted by popularity and are at most from the previous day
    The response is returned in the json format.
    Arguments:
    | covid_terms -- terms to look for in article titles when retrieving articles from the API '''

    covid_terms_list = []
    for term in covid_terms.split(" "):
        covid_terms_list.append(term)
    covid_terms_request = covid_terms_list[0]
    # Create a string separating the chosen terms by "OR" for the API request
    for item in covid_terms_list[1:]:
        covid_terms_request += f" OR {item}"
    # Set the publish date limit for articles to be relatively recent
    previous_date = str(datetime.datetime.today() - datetime.timedelta(days=2))
    news_date_set = previous_date.split(" ")[0]
    # Format the API request with the relevant terms, date and API key
    url = ('https://newsapi.org/v2/everything?'
           f'qInTitle={covid_terms_request}&'
           f'from={news_date_set}&'
           'sortBy=popularity&'
           'language=en&'
           f'apiKey={API_KEY}')
    # Return the API response in json format
    response = requests.get(url).json()
    news_articles = open(os.path.join("./datafiles/", "news_articles.json"), "w", encoding="utf-8")
    news_articles.write(json.dumps(response, sort_keys=False, indent=4))
    return response


def select_articles(news_dict_list:dict)->list:
    ''' Select a limited number of articles which have not been deleted by the user

    The function returns a list of 7 articles from the API response returned by news_API_request
    It is also executed when the page is refreshed, allowing the removal of deleted articles.
    Arguments:
    | news_dict_list -- list of dictionaries (news articles), as returned by news_API_request '''

    selected_articles_list = []
    article_count = 0
    while article_count < 7:
        # Iterate until the number of articles reaches 7
        this_article = news_dict_list["articles"][article_count]
        selected_articles_list.append(this_article)
        article_count += 1
    # Return the list of selected articles in json format
    selected_articles_file = open(os.path.join("./datafiles/", "selected_articles_file.json"), "w", encoding="utf-8")
    selected_articles_file.write(json.dumps(selected_articles_list, sort_keys=False, indent=4))
    return selected_articles_list


def update_news(article)->list:
    ''' Updates news articles

    The function adds a news article to the list of current articles
    The list of updated articles is returned. '''
    news_articles.append({article})
    return news_articles