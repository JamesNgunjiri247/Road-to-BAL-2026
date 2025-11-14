"""
Scrape historical BAL and Road to BAL data for specific teams
Focuses on the 7 teams in Groups A & B with their performance metrics
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json

# -----------------------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------------------
BASE_URL = "https://www.fiba.basketball"

# Target teams with their slugs (from teams_roster_links.csv)
TARGET_TEAMS = {
    # Group A
    "nairobi-city-thunder": {
        "name": "Nairobi City Thunder",
        "tier": "Tier 1 (BAL Vet)",
        "narrative": "The Hosts - 2025 BAL debutants"
    },
    "namuwongo-blazers": {
        "name": "Namuwongo Blazers",
        "tier": "Tier 2 (New Guard)",
        "narrative": "The Kingslayers - First Ugandan NBL title"
    },
    "johannesburg-giants": {
        "name": "Johannesburg Giants",
        "tier": "Tier 2 (New Guard)",
        "narrative": "The Undefeated - Perfect 5-0 in qualifiers"
    },
    # Group B
    "ferroviario-da-beira": {
        "name": "Ferroviario Da Beira",
        "tier": "Tier 1 (BAL Vet)",
        "narrative": "The Juggernaut - 2x BAL main tournament (2022, 2023)"
    },
    "matero-magic": {
        "name": "Matero Magic",
        "tier": "Tier 2",
        "narrative": "The Road Warriors - Zambian champions"
    },
    "dar-city": {
        "name": "Dar City",
        "tier": "Tier 3 (Dark Horse)",
        "narrative": "Star-Powered Unknown with elite talent"
    },
    "bravehearts-basketball-club": {
        "name": "Bravehearts Basketball Club",
        "tier": "Tier 3",
        "narrative": "The Underdogs - 5x Malawian champions"
    }
}

# Key data sources based on official BAL/FIBA sites
DATA_SOURCES = {
    # Road to BAL 2026 (Current)
    "rtb_2026_stats": "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/stats",
    "rtb_2026_games": "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/games",
    "rtb_2026_standings": "https://en.wikipedia.org/wiki/2026_BAL_qualification",
    
    # BAL Main Tournament Stats
    "bal_main_stats": "https://bal.nba.com/statistics",
    
    # Team-specific historical data
    "nct_2025_stats": "https://basketball.afrobasket.com/team/Nairobi-City-Thunder/17638/Stats",
    "fbeira_2023_stats": "https://www.fiba.basketball/en/history/109-basketball-africa-league/208481/teams/ferroviario-da-beira",
}

# Road to BAL events
ROAD_TO_BAL_EVENTS = [
    "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026",
]

OUTPUT_FILE = "historical_teams_data.csv"

# -----------------------------------------------------------------
# 2. SCRAPING FUNCTIONS
# -----------------------------------------------------------------

def get_page(url):
    """Fetch page with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_team_profile(team_slug, team_info):
    """Scrape individual team profile page for historical data"""
    url = f"{BASE_URL}/en/events/fiba-africa-champions-clubs-road-to-bal-2026/teams/{team_slug}"
    print(f"\nScraping {team_info['name']}...")
    
    soup = get_page(url)
    if not soup:
        return None
    
    team_data = {
        "team_name": team_info["name"],
        "team_slug": team_slug,
        "tier": team_info["tier"],
        "narrative": team_info["narrative"],
        "profile_url": url
    }
    
    # Try to extract stats from the page
    # This will vary based on FIBA's HTML structure
    stats_sections = soup.find_all("div", class_="stats-container")
    
    return team_data

def scrape_team_games(team_slug, event_url):
    """Scrape games for a specific team in an event"""
    games_url = f"{event_url}/games"
    print(f"  Checking games at {games_url}...")
    
    soup = get_page(games_url)
    if not soup:
        return []
    
    games = []
    # Look for game cards that include the team
    game_cards = soup.find_all("a", attrs={"data-testid": "game-card"})
    
    for card in game_cards:
        try:
            # Extract team names
            teams = card.find_all("div", class_="team-name")
            if len(teams) >= 2:
                team1 = teams[0].get_text(strip=True)
                team2 = teams[1].get_text(strip=True)
                
                # Check if our target team is in this game
                target_name = TARGET_TEAMS[team_slug]["name"]
                if target_name.lower() in team1.lower() or target_name.lower() in team2.lower():
                    
                    # Extract scores
                    scores = card.find_all("div", class_="score")
                    score1 = scores[0].get_text(strip=True) if len(scores) > 0 else "N/A"
                    score2 = scores[1].get_text(strip=True) if len(scores) > 1 else "N/A"
                    
                    # Extract date
                    date_elem = card.find("div", class_="date")
                    game_date = date_elem.get_text(strip=True) if date_elem else "N/A"
                    
                    games.append({
                        "team": target_name,
                        "opponent": team2 if target_name.lower() in team1.lower() else team1,
                        "score": f"{score1}-{score2}",
                        "date": game_date,
                        "event_url": event_url
                    })
        except Exception as e:
            print(f"    Error parsing game card: {e}")
            continue
    
    return games

def scrape_bal_history(team_slug):
    """Check BAL main tournament history for a team"""
    print(f"  Checking BAL history...")
    bal_appearances = []
    
    for season_url in BAL_SEASONS:
        soup = get_page(season_url)
        if not soup:
            continue
        
        # Check if team appears in this season
        page_text = soup.get_text().lower()
        team_name = TARGET_TEAMS[team_slug]["name"].lower()
        
        if team_name in page_text:
            season_year = season_url.split("/")[-2]
            bal_appearances.append({
                "team": TARGET_TEAMS[team_slug]["name"],
                "season": season_year,
                "tournament": "BAL Main",
                "url": season_url
            })
            print(f"    ✓ Found in BAL {season_year}")
    
    return bal_appearances

def scrape_road_to_bal_history(team_slug):
    """Check Road to BAL qualifier history"""
    print(f"  Checking Road to BAL history...")
    rtb_appearances = []
    
    for event_url in ROAD_TO_BAL_EVENTS:
        # Check teams page
        teams_url = f"{event_url}/teams"
        soup = get_page(teams_url)
        if not soup:
            continue
        
        page_text = soup.get_text().lower()
        team_name = TARGET_TEAMS[team_slug]["name"].lower()
        
        if team_name in page_text:
            year = "2026" if "2026" in event_url else ("2025" if "2025" in event_url else "2024")
            rtb_appearances.append({
                "team": TARGET_TEAMS[team_slug]["name"],
                "season": year,
                "tournament": "Road to BAL",
                "url": event_url
            })
            print(f"    ✓ Found in Road to BAL {year}")
            
            # Also scrape games for this event
            games = scrape_team_games(team_slug, event_url)
            if games:
                print(f"    ✓ Found {len(games)} games")
    
    time.sleep(1)  # Rate limiting
    return rtb_appearances

def scrape_all_teams():
    """Main scraper for all target teams"""
    all_data = []
    all_appearances = []
    all_games = []
    
    print("="*60)
    print("SCRAPING HISTORICAL DATA FOR 7 TARGET TEAMS")
    print("="*60)
    
    for team_slug, team_info in TARGET_TEAMS.items():
        print(f"\n{'='*60}")
        print(f"Processing: {team_info['name']} ({team_info['tier']})")
        print(f"{'='*60}")
        
        # 1. Get basic profile data
        profile_data = scrape_team_profile(team_slug, team_info)
        if profile_data:
            all_data.append(profile_data)
        
        # 2. Check BAL main tournament history
        bal_history = scrape_bal_history(team_slug)
        all_appearances.extend(bal_history)
        
        # 3. Check Road to BAL history
        rtb_history = scrape_road_to_bal_history(team_slug)
        all_appearances.extend(rtb_history)
        
        # 4. Scrape games from current Road to BAL
        games = scrape_team_games(team_slug, ROAD_TO_BAL_EVENTS[0])
        all_games.extend(games)
        
        time.sleep(2)  # Rate limiting between teams
    
    return all_data, all_appearances, all_games

# -----------------------------------------------------------------
# 3. EXECUTION
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("\nStarting historical data scrape...")
    print(f"Target: {len(TARGET_TEAMS)} teams")
    print(f"Checking: {len(BAL_SEASONS)} BAL seasons + {len(ROAD_TO_BAL_EVENTS)} Road to BAL events")
    
    teams_data, appearances, games = scrape_all_teams()
    
    print("\n" + "="*60)
    print("SCRAPING COMPLETE - SAVING DATA")
    print("="*60)
    
    # Save teams overview
    if teams_data:
        df_teams = pd.DataFrame(teams_data)
        df_teams.to_csv("teams_overview.csv", index=False)
        print(f"\n✓ Teams Overview: teams_overview.csv ({len(df_teams)} teams)")
    
    # Save tournament appearances
    if appearances:
        df_appearances = pd.DataFrame(appearances)
        df_appearances.to_csv("tournament_appearances.csv", index=False)
        print(f"✓ Tournament Appearances: tournament_appearances.csv ({len(df_appearances)} records)")
    
    # Save games data
    if games:
        df_games = pd.DataFrame(games)
        df_games.to_csv("team_games_history.csv", index=False)
        print(f"✓ Games History: team_games_history.csv ({len(df_games)} games)")
    
    # Create summary report
    print("\n" + "="*60)
    print("SUMMARY BY TEAM")
    print("="*60)
    
    for team_slug, team_info in TARGET_TEAMS.items():
        team_name = team_info["name"]
        team_apps = [a for a in appearances if a["team"] == team_name]
        team_games_count = len([g for g in games if g["team"] == team_name])
        
        print(f"\n{team_name} ({team_info['tier']})")
        print(f"  Appearances: {len(team_apps)}")
        print(f"  Games Found: {team_games_count}")
        if team_apps:
            for app in team_apps:
                print(f"    - {app['tournament']} {app['season']}")
    
    print("\n" + "="*60)
    print("All data saved! Ready for Google Sheets upload.")
    print("="*60)
