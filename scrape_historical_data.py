"""
Comprehensive Historical Data Scraper for BAL/Road to BAL Teams
Scrapes from official FIBA, BAL, and Afrobasket sources

Target: 7 teams across Groups A & B
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re

# -----------------------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------------------
BASE_URL = "https://www.fiba.basketball"

# Target teams with metadata
TARGET_TEAMS = {
    # Group A
    "nairobi-city-thunder": {
        "name": "Nairobi City Thunder",
        "short": "NCT",
        "tier": "Tier 1 (BAL Vet)",
        "narrative": "The Hosts - 2025 BAL debutants",
        "afrobasket_id": "17638",
        "bal_2025": True
    },
    "namuwongo-blazers": {
        "name": "Namuwongo Blazers",
        "short": "NAM",
        "tier": "Tier 2 (New Guard)",
        "narrative": "The Kingslayers - First Ugandan NBL title",
        "bal_history": False
    },
    "johannesburg-giants": {
        "name": "Johannesburg Giants",
        "short": "JHG",
        "tier": "Tier 2 (New Guard)",
        "narrative": "The Undefeated - Perfect 5-0 in qualifiers",
        "preliminary_group": "E"
    },
    # Group B
    "ferroviario-da-beira": {
        "name": "Ferroviario Da Beira",
        "short": "FBE",
        "tier": "Tier 1 (BAL Vet)",
        "narrative": "The Juggernaut - 2x BAL main (2022, 2023)",
        "bal_2023": True,
        "fiba_history_id": "208481"
    },
    "matero-magic": {
        "name": "Matero Magic",
        "short": "MAT",
        "tier": "Tier 2",
        "narrative": "The Road Warriors - Zambian champions",
        "preliminary_group": "Various"
    },
    "dar-city": {
        "name": "Dar City",
        "short": "DAR",
        "tier": "Tier 3 (Dark Horse)",
        "narrative": "Star-Powered Unknown with elite talent",
        "preliminary_group": "D"
    },
    "bravehearts-basketball-club": {
        "name": "Bravehearts Basketball Club",
        "short": "BRA",
        "tier": "Tier 3",
        "narrative": "The Underdogs - 5x Malawian champions"
    }
}

# Data sources
DATA_SOURCES = {
    "rtb_2026_stats": "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/stats",
    "rtb_2026_games": "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/games",
    "rtb_2026_standings": "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/standings",
}

# -----------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------

def get_page(url):
    """Fetch page with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        print(f"  Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

# -----------------------------------------------------------------
# 3. SCRAPING FUNCTIONS
# -----------------------------------------------------------------

def scrape_rtb_2026_games():
    """Scrape all games from Road to BAL 2026"""
    print("\n" + "="*60)
    print("SCRAPING: Road to BAL 2026 Games")
    print("="*60)
    
    soup = get_page(DATA_SOURCES["rtb_2026_games"])
    if not soup:
        return []
    
    games = []
    
    # Try multiple selectors for game cards
    game_cards = soup.find_all("a", class_=re.compile("game|match"))
    if not game_cards:
        game_cards = soup.find_all("div", class_=re.compile("game|match"))
    
    print(f"  Found {len(game_cards)} potential game cards")
    
    for idx, card in enumerate(game_cards[:50], 1):  # Limit to first 50
        try:
            # Extract all text from card
            text = card.get_text(separator="|", strip=True)
            
            # Look for team names from our target list
            teams_found = []
            for slug, info in TARGET_TEAMS.items():
                if info["name"] in text or info["short"] in text:
                    teams_found.append(info["name"])
            
            # If we found target teams, extract details
            if len(teams_found) >= 1:
                # Try to extract scores
                score_pattern = r'\b(\d{2,3})\s*[-:]\s*(\d{2,3})\b'
                scores = re.findall(score_pattern, text)
                
                game_link = card.get('href', '')
                if game_link and not game_link.startswith('http'):
                    game_link = BASE_URL + game_link
                
                games.append({
                    "team_involved": ", ".join(teams_found),
                    "game_text": text[:200],
                    "scores": scores[0] if scores else "N/A",
                    "game_url": game_link,
                    "source": "RTB 2026 Games"
                })
                
                print(f"  ✓ Game {idx}: {teams_found}")
        
        except Exception as e:
            continue
    
    print(f"\n  Total games with target teams: {len(games)}")
    return games

def scrape_rtb_2026_stats():
    """Scrape player/team stats from Road to BAL 2026"""
    print("\n" + "="*60)
    print("SCRAPING: Road to BAL 2026 Stats")
    print("="*60)
    
    soup = get_page(DATA_SOURCES["rtb_2026_stats"])
    if not soup:
        return []
    
    stats = []
    
    # Look for stat tables
    tables = soup.find_all("table")
    print(f"  Found {len(tables)} tables")
    
    for table_idx, table in enumerate(tables):
        try:
            rows = table.find_all("tr")
            print(f"\n  Table {table_idx + 1}: {len(rows)} rows")
            
            for row in rows[:20]:  # First 20 rows per table
                cells = row.find_all(["td", "th"])
                row_text = [cell.get_text(strip=True) for cell in cells]
                
                # Check if any target team appears in the row
                row_str = " ".join(row_text)
                for slug, info in TARGET_TEAMS.items():
                    if info["name"] in row_str or info["short"] in row_str:
                        stats.append({
                            "team": info["name"],
                            "stat_row": " | ".join(row_text),
                            "table_index": table_idx,
                            "source": "RTB 2026 Stats"
                        })
                        break
        
        except Exception as e:
            continue
    
    print(f"\n  Total stat rows with target teams: {len(stats)}")
    return stats

def scrape_rtb_2026_standings():
    """Scrape standings from Road to BAL 2026"""
    print("\n" + "="*60)
    print("SCRAPING: Road to BAL 2026 Standings")
    print("="*60)
    
    soup = get_page(DATA_SOURCES["rtb_2026_standings"])
    if not soup:
        return []
    
    standings = []
    
    # Look for standings tables
    tables = soup.find_all("table", class_=re.compile("standing|ranking|table"))
    if not tables:
        tables = soup.find_all("table")
    
    print(f"  Found {len(tables)} tables")
    
    for table in tables:
        try:
            rows = table.find_all("tr")
            
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                
                # Check for target teams
                row_str = " ".join(row_data)
                for slug, info in TARGET_TEAMS.items():
                    if info["name"] in row_str or info["short"] in row_str:
                        standings.append({
                            "team": info["name"],
                            "standing_data": " | ".join(row_data),
                            "source": "RTB 2026 Standings"
                        })
                        print(f"  ✓ Found: {info['name']}")
                        break
        
        except Exception as e:
            continue
    
    print(f"\n  Total standings rows: {len(standings)}")
    return standings

def scrape_nct_2025_bal_stats():
    """Scrape Nairobi City Thunder 2025 BAL stats from Afrobasket"""
    print("\n" + "="*60)
    print("SCRAPING: NCT 2025 BAL Stats (Afrobasket)")
    print("="*60)
    
    url = "https://basketball.afrobasket.com/team/Nairobi-City-Thunder/17638/Stats"
    soup = get_page(url)
    if not soup:
        return []
    
    stats = []
    
    # Extract team stats
    stat_sections = soup.find_all("div", class_=re.compile("stat|team"))
    
    # Look for tables with player data
    tables = soup.find_all("table")
    print(f"  Found {len(tables)} tables")
    
    for table in tables:
        try:
            rows = table.find_all("tr")
            headers = []
            
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                
                if row_data:
                    stats.append({
                        "team": "Nairobi City Thunder",
                        "season": "2025 BAL",
                        "data": " | ".join(row_data),
                        "source": "Afrobasket"
                    })
        
        except Exception as e:
            continue
    
    print(f"  Extracted {len(stats)} stat rows for NCT")
    return stats

def scrape_fbeira_2023_bal_stats():
    """Scrape Ferroviario Da Beira 2023 BAL stats from FIBA"""
    print("\n" + "="*60)
    print("SCRAPING: F. Da Beira 2023 BAL Stats (FIBA)")
    print("="*60)
    
    url = "https://www.fiba.basketball/en/history/109-basketball-africa-league/208481/teams/ferroviario-da-beira"
    soup = get_page(url)
    if not soup:
        return []
    
    stats = []
    
    # Extract player leaders and stats
    tables = soup.find_all("table")
    print(f"  Found {len(tables)} tables")
    
    for table in tables:
        try:
            rows = table.find_all("tr")
            
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                
                if row_data and len(row_data) > 1:
                    stats.append({
                        "team": "Ferroviario Da Beira",
                        "season": "2023 BAL",
                        "data": " | ".join(row_data),
                        "source": "FIBA History"
                    })
        
        except Exception as e:
            continue
    
    print(f"  Extracted {len(stats)} stat rows for F. Da Beira")
    return stats

# -----------------------------------------------------------------
# 4. MAIN EXECUTION
# -----------------------------------------------------------------

def main():
    print("\n" + "="*70)
    print("HISTORICAL DATA SCRAPER - BAL & ROAD TO BAL 2026")
    print("="*70)
    print(f"\nTarget Teams: {len(TARGET_TEAMS)}")
    for slug, info in TARGET_TEAMS.items():
        print(f"  - {info['name']} ({info['tier']})")
    
    all_data = {
        "games": [],
        "stats": [],
        "standings": [],
        "nct_bal": [],
        "fbeira_bal": []
    }
    
    # Scrape Road to BAL 2026 data
    all_data["games"] = scrape_rtb_2026_games()
    time.sleep(2)
    
    all_data["stats"] = scrape_rtb_2026_stats()
    time.sleep(2)
    
    all_data["standings"] = scrape_rtb_2026_standings()
    time.sleep(2)
    
    # Scrape historical BAL data for specific teams
    all_data["nct_bal"] = scrape_nct_2025_bal_stats()
    time.sleep(2)
    
    all_data["fbeira_bal"] = scrape_fbeira_2023_bal_stats()
    
    # Save all data to CSV files
    print("\n" + "="*70)
    print("SAVING DATA TO CSV FILES")
    print("="*70)
    
    saved_files = []
    
    if all_data["games"]:
        df = pd.DataFrame(all_data["games"])
        filename = "rtb_2026_games.csv"
        df.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(df)} records)")
        saved_files.append(filename)
    
    if all_data["stats"]:
        df = pd.DataFrame(all_data["stats"])
        filename = "rtb_2026_stats.csv"
        df.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(df)} records)")
        saved_files.append(filename)
    
    if all_data["standings"]:
        df = pd.DataFrame(all_data["standings"])
        filename = "rtb_2026_standings.csv"
        df.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(df)} records)")
        saved_files.append(filename)
    
    if all_data["nct_bal"]:
        df = pd.DataFrame(all_data["nct_bal"])
        filename = "nct_2025_bal_stats.csv"
        df.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(df)} records)")
        saved_files.append(filename)
    
    if all_data["fbeira_bal"]:
        df = pd.DataFrame(all_data["fbeira_bal"])
        filename = "fbeira_2023_bal_stats.csv"
        df.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(df)} records)")
        saved_files.append(filename)
    
    # Summary
    print("\n" + "="*70)
    print("SCRAPING COMPLETE!")
    print("="*70)
    print(f"\nFiles created: {len(saved_files)}")
    for f in saved_files:
        print(f"  - {f}")
    
    print("\n✓ Ready to upload to Google Sheets!")

if __name__ == "__main__":
    main()
