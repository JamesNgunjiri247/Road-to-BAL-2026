"""
Scrape Elite 16 stats and records for NCT, Ferroviario Da Beira, and Bravehearts
from the FIBA Road to BAL 2026 Elite 16 tournament
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

# Target teams for Elite 16 data collection
TARGET_TEAMS = {
    "nairobi-city-thunder": {
        "name": "Nairobi City Thunder",
        "code": "NCT",
        "tier": "Tier 1",
        "group": "Group A"
    },
    "ferroviario-da-beira": {
        "name": "Ferroviario Da Beira",
        "code": "FBE",
        "tier": "Tier 1", 
        "group": "Group B"
    },
    "bravehearts-basketball-club": {
        "name": "Bravehearts",
        "code": "BHB",
        "tier": "Tier 3",
        "group": "Group B"
    }
}

# FIBA URLs for Elite 16 data
BASE_URL = "https://www.fiba.basketball"
ELITE_16_EVENT = "/en/events/fiba-africa-champions-clubs-road-to-bal-2026"

URLS = {
    "standings": f"{BASE_URL}{ELITE_16_EVENT}/standings",
    "stats": f"{BASE_URL}{ELITE_16_EVENT}/stats",
    "games": f"{BASE_URL}{ELITE_16_EVENT}/games",
    "teams": f"{BASE_URL}{ELITE_16_EVENT}/teams"
}

def get_page(url):
    """Fetch page with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  ❌ Error fetching {url}: {e}")
        return None

def extract_team_stats_from_page(html, team_info):
    """Extract team statistics from HTML content"""
    soup = BeautifulSoup(html, 'html.parser')
    
    stats = {
        "team": team_info["name"],
        "code": team_info["code"],
        "tier": team_info["tier"],
        "group": team_info["group"],
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "points_for": 0,
        "points_against": 0,
        "point_diff": 0
    }
    
    # Look for standings/stats tables
    tables = soup.find_all("table")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            row_text = row.get_text()
            
            # Check if this row contains our team
            if team_info["name"] in row_text or team_info["code"] in row_text:
                cells = row.find_all(["td", "th"])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # Try to extract numeric stats
                numbers = [text for text in cell_texts if text.replace('-','').replace('+','').isdigit()]
                
                if len(numbers) >= 5:
                    try:
                        stats["games_played"] = int(numbers[0]) if numbers else 0
                        stats["wins"] = int(numbers[1]) if len(numbers) > 1 else 0
                        stats["losses"] = int(numbers[2]) if len(numbers) > 2 else 0
                        stats["points_for"] = int(numbers[3]) if len(numbers) > 3 else 0
                        stats["points_against"] = int(numbers[4]) if len(numbers) > 4 else 0
                    except:
                        pass
                
                print(f"  ✓ Found {team_info['name']}: {cell_texts}")
                break
    
    return stats

def scrape_team_games(html, team_info):
    """Extract game results for a specific team"""
    soup = BeautifulSoup(html, 'html.parser')
    games = []
    
    # Look for game cards or game results
    game_cards = soup.find_all(["div", "article"], class_=lambda x: x and ("game" in x.lower() or "match" in x.lower()))
    
    for card in game_cards[:20]:  # Limit to recent games
        text = card.get_text()
        
        # Check if our team is mentioned
        if team_info["name"] in text or team_info["code"] in text:
            games.append({
                "team": team_info["name"],
                "game_info": text[:300],
                "html_snippet": str(card)[:500]
            })
            print(f"  ✓ Found game for {team_info['name']}")
    
    return games

def scrape_elite16_stats():
    """Main scraping function for Elite 16 statistics"""
    print("\n" + "="*70)
    print("SCRAPING ELITE 16 STATS FOR 3 CASE STUDY TEAMS")
    print("="*70)
    print("\nTarget Teams:")
    for slug, info in TARGET_TEAMS.items():
        print(f"  • {info['name']} ({info['code']}) - {info['tier']}, {info['group']}")
    
    all_stats = []
    all_games = []
    
    # 1. Scrape standings page
    print("\n" + "-"*70)
    print("PHASE 1: Scraping Standings Page")
    print("-"*70)
    
    standings_html = get_page(URLS["standings"])
    if standings_html:
        print("✓ Downloaded standings page")
        
        # Save HTML for manual inspection
        with open("elite16_standings_page.html", "w", encoding="utf-8") as f:
            f.write(standings_html)
        print("✓ Saved to: elite16_standings_page.html")
        
        # Extract stats for each team
        for slug, info in TARGET_TEAMS.items():
            print(f"\n  Searching for: {info['name']}")
            stats = extract_team_stats_from_page(standings_html, info)
            all_stats.append(stats)
    
    time.sleep(2)
    
    # 2. Scrape games page
    print("\n" + "-"*70)
    print("PHASE 2: Scraping Games Page")
    print("-"*70)
    
    games_html = get_page(URLS["games"])
    if games_html:
        print("✓ Downloaded games page")
        
        # Save HTML for manual inspection
        with open("elite16_games_page.html", "w", encoding="utf-8") as f:
            f.write(games_html)
        print("✓ Saved to: elite16_games_page.html")
        
        # Extract games for each team
        for slug, info in TARGET_TEAMS.items():
            print(f"\n  Searching games for: {info['name']}")
            team_games = scrape_team_games(games_html, info)
            all_games.extend(team_games)
    
    time.sleep(2)
    
    # 3. Scrape stats page
    print("\n" + "-"*70)
    print("PHASE 3: Scraping Stats Page")
    print("-"*70)
    
    stats_html = get_page(URLS["stats"])
    if stats_html:
        print("✓ Downloaded stats page")
        
        # Save HTML for manual inspection
        with open("elite16_stats_page.html", "w", encoding="utf-8") as f:
            f.write(stats_html)
        print("✓ Saved to: elite16_stats_page.html")
        
        # Look for player stats or team rankings
        soup = BeautifulSoup(stats_html, 'html.parser')
        
        # Check for embedded JSON data
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and "stats" in script.string.lower():
                script_content = script.string[:1000]
                print(f"\n  Found stats-related script: {script_content[:200]}...")
    
    # 4. Try to find embedded JSON data in standings
    print("\n" + "-"*70)
    print("PHASE 4: Searching for Embedded JSON Data")
    print("-"*70)
    
    if standings_html:
        soup = BeautifulSoup(standings_html, 'html.parser')
        scripts = soup.find_all("script")
        
        print(f"  Found {len(scripts)} script tags")
        
        for idx, script in enumerate(scripts):
            if script.get("src"):
                src = script.get("src")
                if "standings" in src or "stats" in src or "data" in src:
                    full_url = src if src.startswith("http") else BASE_URL + src
                    print(f"\n  Script {idx}: {full_url}")
                    
                    # Try to download the script
                    script_content = get_page(full_url)
                    if script_content and len(script_content) > 1000:
                        filename = f"elite16_script_{idx}.js"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(script_content)
                        print(f"  ✓ Saved to: {filename}")
    
    # Save results
    print("\n" + "="*70)
    print("SAVING RESULTS")
    print("="*70)
    
    if all_stats:
        df_stats = pd.DataFrame(all_stats)
        df_stats.to_csv("elite16_team_stats_scraped.csv", index=False)
        print(f"\n✓ Team Stats: elite16_team_stats_scraped.csv ({len(df_stats)} teams)")
        print(df_stats)
    
    if all_games:
        df_games = pd.DataFrame(all_games)
        df_games.to_csv("elite16_team_games_scraped.csv", index=False)
        print(f"\n✓ Team Games: elite16_team_games_scraped.csv ({len(df_games)} games)")
    
    print("\n" + "="*70)
    print("SCRAPING COMPLETE!")
    print("="*70)
    print("\n📝 NEXT STEPS:")
    print("  1. Review HTML files for manual data extraction")
    print("  2. Check JavaScript files for embedded JSON data")
    print("  3. Use browser inspector to find API endpoints")
    print("  4. Consider manual entry if scraping fails")

if __name__ == "__main__":
    scrape_elite16_stats()
