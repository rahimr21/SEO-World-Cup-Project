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

#ID's for API to fetch 2026 World Cup Stuff (changing to 2022 for free plan)
LEAGUE_ID = 1
SEASON = 2022

def get_football_headers():
    return {
        "x-apisports-key": FOOTBALL_KEY
    }

#Fetches all teams as a list
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

#gets all wc matches for a specific team
def fetch_fixtures(team_id):
    url = f"{FOOTBALL_URL}/fixtures"
    params = {
        "team": team_id,
        "league": LEAGUE_ID,
        "season": SEASON
    }

    response = requests.get(url, headers=get_football_headers(), params=params)
    data = response.json()
    return data.get("response", [])

#gets current group standings 
def fetch_standings():
    url = f"{FOOTBALL_URL}/standings"
    params = {
        "league": LEAGUE_ID,
        "season": SEASON
    }

    response = requests.get(url, headers=get_football_headers(), params=params)
    data = response.json()

    if data.get("response"):
        return data["response"][0]["league"]["standings"]
    return []

#live scores
def fetch_live_scores():
    url = f"{FOOTBALL_URL}/fixtures"
    params = {
        "live": "all"
    }
    response = requests.get(url, headers=get_football_headers(), params=params)
    data = response.json()
    
    live_matches = []
    for item in data.get("response", []):
        if item.get("league", {}).get("id") == LEAGUE_ID:
            live_matches.append(item)
    return live_matches

#searching for player by name
def search_player(last_name):
    url = f"{FOOTBALL_URL}/players"
    params = {
        "search": last_name,
        "league": LEAGUE_ID,
        "season": SEASON
    }

    response = requests.get(url, headers=get_football_headers(), params=params)
    data = response.json()
    return data.get("response", [])

# print(fetch_teams())
def get_news(team):
    params = {
        "q": f'"{team}" AND "World Cup"',
        "searchIn": "title,description",
        "sortBy": "relevancy",
        "apiKey": NEWS_KEY
    }
    r = requests.get("https://newsapi.org/v2/everything", params=params)
    articles = r.json().get("articles", [])
    return articles[:5]

def get_player_news(player):
    pararms = {
        "q": f'"{player}" AND "World Cup"',
        "searchIn": "title,description",
        "sortBy": "relevancy",
        "apiKey": NEWS_KEY
    }
    r = requests.get("https://newsapi.org/v2/everything", params=params)
    articles = r.json().get("articles", [])
    return articles[:5]

def get_current_news():
    params = {
        "q": '"World Cup"',
        "searchIn": "title",
        "sortBy": "relevancy",
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
