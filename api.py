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

