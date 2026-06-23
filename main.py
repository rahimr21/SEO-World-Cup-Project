def home_menu():
    print("\nWorld Cup")
    print("1. Team Information")
    print("2. Player Information")
    print("3. Current Games")
    print("4. View Favorites")
    choice = input("Enter the number which you want to select: ")

    if choice == "1":
        team_menu()
    elif choice == "2":
        player_menu()
    elif choice == "3":
        current_games_menu()
    elif choice == "4":
        print(get_favorites())

    
