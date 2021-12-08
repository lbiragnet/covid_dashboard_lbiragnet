from main import update_covid_data
from main import update_news_articles
from main import remove_update
from main import schedule_data_update
from main import schedule_news_update
from main import schedule_double_updates

from covid_data_handler import get_covid_data
from covid_data_handler import process_live_covid_data



def test_update_covid_data():
    updated_covid_data = update_covid_data()
    local_covid_data, national_covid_data = get_covid_data()
    processed_data = process_live_covid_data(local_covid_data, national_covid_data)
    assert updated_covid_data == processed_data


def test_update_news_articles():
    updated_news = update_news_articles()
    assert updated_news


def test_remove_update():
    removed_update = remove_update({"title": "update test",
                                    "update_time": "15:15",
                                    "content":"update test",
                                    "repeat_update": "repeat"})
    assert not removed_update


def test_schedule_data_update():
    data_updates_list, updates_list = schedule_data_update("data update test", "15:15", "repeat")
    assert data_updates_list[0]
    assert updates_list[0]["title"] == "data update test"
    assert updates_list[0]["update_time"] == "15:15"
    assert updates_list[0]["content"] == "update covid data"
    assert updates_list[0]["repeat_update"] == "repeat"


def test_schedule_news_update():
    news_updates_list, updates_list = schedule_news_update("news update test", "15:15", "repeat")
    assert news_updates_list[0]
    assert updates_list[1]["title"] == "news update test"
    assert updates_list[1]["update_time"] == "15:15"
    assert updates_list[1]["content"] == "update news"
    assert updates_list[1]["repeat_update"] == "repeat"


def test_schedule_double_updates():
    double_updates_list, updates_list = schedule_double_updates("double update test", "16:16", "repeat")
    assert double_updates_list[0]
    assert updates_list[2]["title"] == "double update test"
    assert updates_list[2]["update_time"] == "16:16"
    assert updates_list[2]["content"] == "update covid data and news"
    assert updates_list[2]["repeat_update"] == "repeat"
