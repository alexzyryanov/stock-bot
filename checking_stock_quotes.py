import requests
import sqlite3
from bs4 import BeautifulSoup


user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

url_ru = "https://smart-lab.ru/q/shares/?utm_source=quotes"


def checker():
    r = requests.get(url=url_ru, params=user_agent)
    print(r.status_code)
    with open("ru.html", "wb") as f:
        f.write(r.content)

    with open("ru.html", "rb") as f:
        content = f.read()
    soup = BeautifulSoup(content, "lxml")

    element = soup.find_all("tr")
    print(len(element))
    for line in range(2, len(element) + 1):
        print(line)
        info = element[line].find_all("td")
        name = info[2].text
        ticker = info[3].text
        cost = info[7].text
        print(name, ticker, cost)
        print("---")
        save_in_db(name, ticker, cost)


def create_db():
    connect_db = sqlite3.connect("cost.db")
    cursor = connect_db.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS ru (name TEXT, ticker TEXT, cost TEXT) """)
    connect_db.commit()
    cursor.close()
    connect_db.close()


def save_in_db(name, ticker, cost):
    connect_db = sqlite3.connect("cost.db")
    cursor = connect_db.cursor()
    param = f""" SELECT ticker FROM ru WHERE ticker = "{ticker}" """
    cursor.execute(param)
    check = cursor.fetchone()

    if check is None:
        cursor.execute(""" INSERT INTO ru VALUES (?, ?, ?) """, (name, ticker, cost))
        connect_db.commit()
    else:
        new = f""" UPDATE ru SET cost = "{cost}" WHERE ticker = "{ticker}" """
        cursor.execute(new)
        connect_db.commit()

    cursor.close()
    connect_db.close()


create_db()
checker()
