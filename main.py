from api import *
import api
import database

def home_menu():
    while True:
        print("\n--- WORLD CUP CLI COMPANION ---")
        print("1. Team Information")
        print("2. Player Information")
        print("3. Current Games")
        print("4. View Favorites")
        print("5. News")
        print("6. Exit")
        choice = input("Enter the number which you want to select: ").strip()

        if choice == "1":
            team_menu()
        elif choice == "2":
            player_menu()
        elif choice == "3":
            current_games_menu()
        elif choice == "4":
            favorites_menu()
        elif choice == "5":
            news_menu()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def news_menu():
    print("\nNews Menu")
    print("1. General World Cup News")
    print("2. Team News")
    print("3. Player News")
    choice = input("Enter the number which you want to select: ").strip()
    if choice == "1":
        articles = api.get_current_news()
    elif choice == "2":
        team = input("Enter the team name: ").strip()
        articles = api.get_news(team)
    elif choice == "3":
        player = input("Enter the player name: ").strip()
        articles = api.get_player_news(player)
    else:
        print("Invalid choice. Please try again.")
        return

    if not articles:
        print("No news found")
        return
    for article in articles:
        print(f"\n> {article['title']}")
        print(f" URL: {article['url']}")

def team_menu():
    print("\n--- Team Info Menu ---")
    query = input("Enter team name (full or short, eg. Argentina, ARG): ").strip()
    if not query:
        return
    
    print("Fetching teams...")
    all_teams = api.fetch_teams()
    matched_teams = []

    #filtering teams
    for team in all_teams:
        name_match = query.lower() in team["name"].lower()
        code_match = team["code"] and query.lower() == team["code"].lower()
        if name_match or code_match:
            matched_teams.append(team)
    
    if not matched_teams:
        print("No matching team found.")
        return

    #2nd choice list in case multiple teams found
    print("\nSelect a team:")
    for idx, team in enumerate(matched_teams, 1):
        print(f"{idx}. {team['name']} ({team['code'] or 'N/A'})")
    
    sel = input("Enter selection number: ").strip()

    try:
        team_idx = int(sel) - 1
        selected_team = matched_teams[team_idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    
    #submenu inside teams
    while True:
        is_fav = database.is_team_favorite(selected_team["id"])
        fav_label = "[Favorite]" if is_fav else "[Not Favorite]"
        print(f"n\--- {selected_team['name']} Menu {fav_label} ---")
        print("1. View Standings and Group Info")
        print("2. View Matches and News")
        print("3. Add/Remove Favorite")
        print("4. Return to Main Menu")

        choice = input("Enter option: ").strip()
        if choice == "1":
            show_team_standings(selected_team["name"])
        elif choice == "2":
            show_team_matches(selected_team["name"])
        elif choice == "3":
            if is_fav:
                database.remove_team(selected_team["id"])
                print("Removed from favorites.")
            else:
                database.add_team(selected_team["id"], selected_team["name"])
                print("Added to favorites.")
        elif choice == "4":
            break

def show_team_standings(team_name):
    print("\nFetching standings...")
    groups = api.fetch_standings()

    #searching for team in table
    target_group = None
    for group in groups:
        for row in group:
            if row["team"]["name"].lower == team_name.lower():
                target_group = group
                break
        if target_group:
            break
    
    if not target_group:
        print("Standings not found.")
        return

    print(f"\nGroup Standings:")
    print(f"{'Rank':<5} {'Team':<20} {'Played':<8} {'GD':<5} {'Points':<6}")
    print("-" * 50)

    for row in target_group:
        name = row["team"]["name"]
        rank = row["rank"]
        played = row["all"]["played"]
        gd = row["goalsDiff"]
        points = row["points"]

        #highlighting right team in cli
        marker = "-> " if name.lower() == team_name.lower() else "   "
        print(f"{marker}{rank:<2} {name:<20} {played:<8} {gd:<5} {points:<6}")

def show_team_matches(team_id, team_name):
    print(f"\nFetching matches for {team_name}...")
    fixtures = api.fetch_fixtures(team_id)

    past_matches = []
    future_matches = []

    for f in fixtures:
        status = f["fixture"]["status"]["short"]
        if status in ["FT", "AET", "PEN"]:
            past_matches.append(f)
        else:
            future_matches.append(f)

    print("\nPrevious Matches:")
    if not past_matches:
        print("  No previous matches found.")
    else:
        for f in past_matches:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            home_score = f["goals"]["home"]
            away_score = f["goals"]["away"]
            print(f"  {home} {home_score} - {away_score} {away}")

    print("\nUpcoming Matches:")
    if not future_matches:
        print("  No upcoming matches scheduled.")
    else:
        for f in future_matches:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            date = f["fixture"]["date"]
            print(f"  {home} vs {away} (Date: {date[:16]})")


    print("\nRecent Match News:")
    articles = api.get_news(team_name)
    if not articles:
        print("No recent news found.")
    else:
        for idx, art in enumerate(articles, 1):
            print(f"  {idx}. {art['title']}")
            print(f"     Source: {art['source']['name']} | Link: {art['url']}")
    
def player_menu():
    print("\n--- Player Info Menu ---")
    name = input("Enter player last name (min 3 characters): ").strip()
    if len(name) < 3:
        print("Search query must be at least 3 characters.")
        return
        
    print("Searching players...")
    results = api.search_player(name)
    if not results:
        print("No player found.")
        return
        
    # selecting from search results
    print("\nSelect a player:")
    for idx, item in enumerate(results, 1):
        p = item["player"]
        team_name = "Unknown"
        if item.get("statistics"):
            team_name = item["statistics"][0]["team"]["name"]
        print(f"{idx}. {p['name']} (Nationality: {p['nationality']}, Team: {team_name})")
        
    sel = input("Enter choice: ").strip()
    try:
        player_idx = int(sel) - 1
        selected = results[player_idx]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return
        
    p = selected["player"]
    player_id = p["id"]
    player_name = p["name"]
    
    # statistics
    stats = selected.get("statistics", [])
    games = 0
    goals = 0
    assists = 0
    team_name = "Unknown"
    
    if stats:
        s = stats[0]
        team_name = s["team"]["name"]
        games = s["games"]["appearences"] or 0
        goals = s["goals"]["total"] or 0
        assists = s["goals"]["assists"] or 0
        
    while True:
        is_fav = database.is_player_favorite(player_id)
        fav_label = "[Favorite]" if is_fav else "[Not Favorite]"
        print(f"\n--- {player_name} {fav_label} ---")
        print(f"Team: {team_name}")
        print(f"Nationality: {p['nationality']}")
        print(f"Age: {p['age']}")
        print(f"Matches Played: {games}")
        print(f"Goals: {goals}")
        print(f"Assists: {assists}")
        print("\n1. Toggle Favorite")
        print("2. Back to Main Menu")
        
        choice = input("Enter option: ").strip()
        if choice == "1":
            if is_fav:
                database.remove_player(player_id)
                print("Removed from favorites.")
            else:
                database.add_player(player_id, player_name)
                print("Added to favorites.")
        elif choice == "2":
            break

def current_games_menu():
    print("\n--- Current Games Menu ---")
    print("Checking live games...")
    live_games = api.fetch_live_scores()

    if live_games:
        for f in live_games:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            home_score = f["goals"]["home"]
            away_score = f["goals"]["away"]
            time = f["fixture"]["status"]["elapsed"]
            print(f"[LIVE {time}'] {home} {home_score} - {away_score} {away}")

home_menu()