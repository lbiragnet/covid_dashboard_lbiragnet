from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import select_articles



def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()


def test_update_news():
    update_news('test')


def test_select_articles():
    news = news_API_request()
    selected_news = select_articles(news)
    assert selected_news
    assert len(selected_news) == 7