from api import *
def home_menu():
    print("\nWorld Cup")
    print("1. Team Information")
    print("2. Player Information")
    print("3. Current Games")
    print("4. View Favorites")
    print("5. News")
    choice = input("Enter the number which you want to select: ")

    if choice == "1":
        team_menu()
    elif choice == "2":
        player_menu()
    elif choice == "3":
        current_games_menu()
    elif choice == "4":
        print(get_favorites())
    elif choice == "5":
        news_menu()

def news_menu():
    print("\nNews Menu")
    print("1. General World Cup News")
    print("2. Team News")
    choice = input("Enter the number which you want to select: ")
    if choice == "1":
        articles = get_current_news()
    elif choice == "2":
        team = input("Enter the team name: ")
        articles = get_news(team)
    else:
        print("Invalid choice. Please try again.")
        return

    if not articles:
        print("No news found")
        return
    for article in articles:
        print(f"\n> {article['title']}")
        print(f" URL: {article['url']}")

        

    
home_menu()