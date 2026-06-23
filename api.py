import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".env"))

load_dotenv()

FOOTBALL_KEY = os.getenv("FOOTBALL_KEY")
NEWS_KEY = os.getenv("NEWS_KEY")

#Base URLs
FOOTBALL_URL = "https://v3.football.api-sports.io"

#ID's for API to fetch 2026 World Cup Stuff
LEAGUE_ID = 1
SEASON = 2026

def get_football_headers():
    return {
        "x-apisports-key": FOOTBALL_KEY
    }

def fetch_teams():
    url = f"{FOOTBALL_URL}/teams"
    params = {
        "league": LEAGUE_ID,
        "season": SEASON
    }

    response = requests.get(url, headers=get_football_headers(), params=params)
    data = response.json()

    teams_list = []
    for item in data.get("response", []):
        team_data = item.get("team", {})
        teams_list.append({
            "id": team_data.get("id"),
            "name": team_data.get("name"),
            "code": team_data.get("code")
        })
    return teams_list

print(fetch_teams())
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

# r = requests.get("https://newsapi.org/v2/everything", params = {
#     "q": "World Cup 2026",
#     "sortBy": "publishedAt",
#     "apiKey": NEWS_KEY
# })
# print(r.status_code)
# print(r.json())
    
# print(get_current_news())
