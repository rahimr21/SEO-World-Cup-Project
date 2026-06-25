import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "worldcup.db")

def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #creating fav team table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT
        )
    """)
    #creating fav player table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_team(team_id, team_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO favorite_teams (team_id, team_name) VALUES (?, ?)", (team_id, team_name))
    conn.commit()
    conn.close()

def remove_team(team_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorite_teams WHERE team_id = ?", (team_id,))
    conn.commit()
    conn.close()

def get_teams():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT team_id, team_name FROM favorite_teams")
    rows = cursor.fetchall()
    conn.close()
    return rows

def is_team_favorite(team_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorite_teams WHERE team_id = ?", (team_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def add_player(player_id, player_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO favorite_players (player_id, player_name) VALUES (?, ?)", (player_id, player_name))
    conn.commit()
    conn.close()

def remove_player(player_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorite_players WHERE player_id = ?", (player_id,))
    conn.commit()
    conn.close()

def get_players():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, player_name FROM favorite_players")
    rows = cursor.fetchall()
    conn.close()
    return rows

def is_player_favorite(player_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorite_players WHERE player_id = ?", (player_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

init_db()

