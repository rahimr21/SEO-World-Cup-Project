# SEO-World-Cup-Project

A command line tool to follow the 2026 FIFA World Cup. 
Look up live scores, team info, player stats, and the latest news - all in one place.

## Features
- Live game scores
- Team info: past results, upcoming matches, and group standings
- Player search and stats
- Latest World Cup news (general, by team, or by player)
- Save favorite teams and players

## APIs Used
- [NewsAPI](https://newsapi.org/) — latest World Cup headlines

## Setup
1. Clone the repo:
git clone  https://github.com/rahimr21/SEO-World-Cup-Project.git
2. Cd into the folder it is in
3. Install dependancies
pip install requests python-dotenv
4. Create a '.env' file in the project folder:
FOOTBALL_KEY=your_api_football_key
NEWS_KEY=your_newsapi_key

## Usage
Run the app:
python3 main.ppy
Then navigate the menu:
1. Team Information
2. Player Information
3. Current Games
4. View Favorites
5. News

- **Team Information** - enter a team name to see past results, upcoming games, and standings
- **Player Standings** - search a player by name to see their stats
- **Current Games** - view live scores
- **View Favorites** - see your saved teams and players
- **News** - get general World Cup headlines or news by team or player

## Database
Uses SQLite to store favorite teams and players

## Contact
- Anika Hakim - hakimanika3529@gmail.com - [GitHub](https://github.com/Anikahakim)
- Rahim Rashid - EMAIL - [GitHub]