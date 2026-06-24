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
        print("5. Exit")
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
    if not in query:
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
        is_fav = database.is_team_favoite(selected_team["id"])
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

