import requests
from bs4 import BeautifulSoup as bs

def get_last_article():
    URL = "https://www.rbc.ru/search/ajax/?tag=%D0%A1%D0%B1%D0%B5%D1%80%D0%B1%D0%B0%D0%BD%D0%BA&dateFrom=01.03.2012&dateTo={CURRENT_DATE}&project=rbcnews&page=0"
    response = requests.get(URL)
    data = response.json()

    response = requests.get(data["items"][0]["fronturl"])
    soup = bs(response.content, "html.parser")
    last_article_text = soup.find("div", class_="article__text article__text_free").text.replace("\n", "")

    last_article = {
        "id": data["items"][0]["id"],
        "url": data["items"][0]["fronturl"],
        "title": data["items"][0]["title"],
        "text": last_article_text
    }

    return last_article

