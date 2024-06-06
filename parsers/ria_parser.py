import requests
from bs4 import BeautifulSoup as bs

def get_last_article():
    URL = "https://ria.ru/organization_Sberbank_Rossii/"
    response = requests.get(URL)
    soup = bs(response.content, "html.parser")

    last_article_url = soup.find("div", class_="list list-tags").find_all("div", class_="list-item")[0].find_next("div", class_="list-item__content").find("a", class_="list-item__title color-font-hover-only").attrs["href"]
    last_article_title = soup.find("div", class_="list list-tags").find_all("div", class_="list-item")[0].find_next("div", class_="list-item__content").find("a", class_="list-item__title color-font-hover-only").text



    last_article = {
            "id": None,
            "url": last_article_url,
            "title": last_article_title,

    }

    return last_article