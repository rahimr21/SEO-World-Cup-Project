import os
import requests
from dotenv import load_dotenv

FOOTBALL_KEY = os.getenv("FOOTBALL_KEY")
NEWS_KEY = os.getenv("NEWS_KEY")

def get_news(team):
    params = {
        "q": f"{team} AND World Cup 2026",
        "sortBy": "publishedAt",
        "apiKey": NEWS_KEY
    }
    r = requests.get("https://newsapi.org/v2/everything", params=params)
    articles = r.json().get("articles", [])
    return articles[:5]

def get_current_news():
    params = {
        "q": "World Cup 2026",
        "sortBy": "publishedAt",
        "apiKey": NEWS_KEY
    }
    r = requests.get("https://newsapi.org/v2/everything", params=params)
    articles = r.json().get("articles", [])
    return articles[:5]
    