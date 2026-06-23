import os
import requests
from dotenv import load_dotenv

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