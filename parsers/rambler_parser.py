import requests
from bs4 import BeautifulSoup as bs

def get_last_article():
    URL = "https://finance.rambler.ru/organization/sberbank-rossii/"
    response = requests.get(URL)
    soup = bs(response.content, "html.parser")
    
    last_article_url = soup.find("div", class_="_3Q3a3 _3TiUi").find_all("div", class_="_4Niiv JbKe8")[0].find_next("a", class_="_1uRkW").attrs["href"]
    last_article_title = soup.find("div", class_="_3Q3a3 _3TiUi").find_all("div", class_="_4Niiv JbKe8")[0].find_next("a", class_="_1uRkW").find("div", class_="_2VIgt _1z1vG").find("img", class_="_3hvpU").attrs["alt"]

    last_article = {
            "id": None,
            "url": last_article_url,
            "title": last_article_title,
    }

    return last_article

