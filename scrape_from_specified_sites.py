"""
Comprehensive scraper for case study teams using specified BAL/FIBA sources
Targets: Road to BAL 2025, FIBA History, BAL.NBA.com, Basketball24
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# -----------------------------------------------------------------
# CONFIGURATION - Case Study Teams
# -----------------------------------------------------------------

CASE_STUDY_TEAMS = [
    "Nairobi City Thunder",
    "Namuwongo Blazers", 
    "Johannesburg Giants",
    "Ferroviario Da Beira",
    "Matero Magic",
    "Dar City",
    "Bravehearts"
]

# Alternative name variations for matching
TEAM_VARIATIONS = {
    "Ferroviario Da Beira": ["Ferroviario", "Beira", "Ferroviário", "FBE"],
    "Nairobi City Thunder": ["NCT", "Nairobi", "Thunder"],
    "Namuwongo Blazers": ["Namuwongo", "Blazers"],
    "Johannesburg Giants": ["Johannesburg", "Giants", "JHB"],
    "Matero Magic": ["Matero", "Magic"],
    "Dar City": ["Dar", "Dar City"],
    "Bravehearts": ["Bravehearts", "Brave Hearts", "BRA"]
}

DATA_SOURCES = {
    "rtb_2025": "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2025",
    "fiba_history": "https://www.fiba.basketball/en/history/104-africa-champions-clubs-road-to-bal/208719",
    "bal_teams": "https://bal.nba.com/teams",
    "bal_stats": "https://bal.nba.com/statistics",
    "basketball24": "https://www.basketball24.com/africa/bal-2022/"
}

# -----------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------

def get_page(url, delay=2):
    """Fetch page with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        print(f"  Fetching: {url[:80]}...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        time.sleep(delay)
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
        return None

def team_matches(text, team_name):
    """Check if team name or variations appear in text"""
    text_lower = text.lower()
    if team_name.lower() in text_lower:
        return True
    
    variations = TEAM_VARIATIONS.get(team_name, [])
    for var in variations:
        if var.lower() in text_lower:
            return True
    return False

def extract_tables(soup, team_name):
    """Extract all table data"""
    tables_data = []
    tables = soup.find_all("table")
    
    for idx, table in enumerate(tables):
        try:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_text = [cell.get_text(strip=True) for cell in cells]
                row_string = " ".join(row_text)
                
                # Check if this row mentions our team
                if team_matches(row_string, team_name):
                    tables_data.append({
                        "team": team_name,
                        "table_index": idx,
                        "row_data": " | ".join(row_text)
                    })
        except Exception as e:
            continue
    
    return tables_data

# -----------------------------------------------------------------
# SCRAPING FUNCTIONS BY SOURCE
# -----------------------------------------------------------------

def scrape_road_to_bal_2025(team_name):
    """Scrape Road to BAL 2025 data"""
    print(f"\n{'='*60}")
    print(f"Road to BAL 2025: {team_name}")
    print(f"{'='*60}")
    
    all_data = []
    
    # Main event page
    soup = get_page(DATA_SOURCES["rtb_2025"])
    if soup:
        data = extract_tables(soup, team_name)
        all_data.extend(data)
        print(f"  Main page: {len(data)} records")
    
    # Games page
    soup = get_page(DATA_SOURCES["rtb_2025"] + "/games")
    if soup:
        data = extract_tables(soup, team_name)
        all_data.extend(data)
        
        # Also look for game cards
        game_cards = soup.find_all(["div", "a"], class_=re.compile("game|match"))
        for card in game_cards:
            text = card.get_text(strip=True)
            if team_matches(text, team_name):
                all_data.append({
                    "team": team_name,
                    "type": "game_card",
                    "data": text[:200]
                })
        print(f"  Games page: {len(data)} records")
    
    # Stats page
    soup = get_page(DATA_SOURCES["rtb_2025"] + "/stats")
    if soup:
        data = extract_tables(soup, team_name)
        all_data.extend(data)
        print(f"  Stats page: {len(data)} records")
    
    # Standings page
    soup = get_page(DATA_SOURCES["rtb_2025"] + "/standings")
    if soup:
        data = extract_tables(soup, team_name)
        all_data.extend(data)
        print(f"  Standings: {len(data)} records")
    
    return all_data

def scrape_fiba_history(team_name):
    """Scrape FIBA historical data"""
    print(f"\n{'='*60}")
    print(f"FIBA History: {team_name}")
    print(f"{'='*60}")
    
    soup = get_page(DATA_SOURCES["fiba_history"])
    if not soup:
        return []
    
    data = extract_tables(soup, team_name)
    
    # Look for links to team-specific pages
    links = soup.find_all("a", href=True)
    for link in links:
        if team_matches(link.get_text(), team_name):
            team_url = link['href']
            if not team_url.startswith('http'):
                team_url = "https://www.fiba.basketball" + team_url
            
            print(f"  Found team page: {team_url[:60]}...")
            team_soup = get_page(team_url, delay=3)
            if team_soup:
                team_data = extract_tables(team_soup, team_name)
                data.extend(team_data)
                print(f"  Team page: {len(team_data)} records")
    
    print(f"  Total: {len(data)} records")
    return data

def scrape_bal_nba_teams(team_name):
    """Scrape BAL.NBA.com teams page"""
    print(f"\n{'='*60}")
    print(f"BAL.NBA.com Teams: {team_name}")
    print(f"{'='*60}")
    
    soup = get_page(DATA_SOURCES["bal_teams"])
    if not soup:
        return []
    
    data = extract_tables(soup, team_name)
    
    # Look for team cards/links
    team_links = soup.find_all("a", href=re.compile("/team/"))
    for link in team_links:
        if team_matches(link.get_text(), team_name):
            team_url = link['href']
            if not team_url.startswith('http'):
                team_url = "https://bal.nba.com" + team_url
            
            print(f"  Found: {team_url[:60]}...")
            team_soup = get_page(team_url, delay=3)
            if team_soup:
                team_data = extract_tables(team_soup, team_name)
                data.extend(team_data)
    
    print(f"  Total: {len(data)} records")
    return data

def scrape_bal_nba_stats(team_name):
    """Scrape BAL.NBA.com statistics page"""
    print(f"\n{'='*60}")
    print(f"BAL.NBA.com Stats: {team_name}")
    print(f"{'='*60}")
    
    soup = get_page(DATA_SOURCES["bal_stats"])
    if not soup:
        return []
    
    data = extract_tables(soup, team_name)
    print(f"  Total: {len(data)} records")
    return data

def scrape_basketball24(team_name):
    """Scrape Basketball24.com BAL data"""
    print(f"\n{'='*60}")
    print(f"Basketball24: {team_name}")
    print(f"{'='*60}")
    
    all_data = []
    
    # Try different years
    for year in [2022, 2023, 2024, 2025]:
        url = f"https://www.basketball24.com/africa/bal-{year}/"
        soup = get_page(url, delay=2)
        if soup:
            data = extract_tables(soup, team_name)
            if data:
                all_data.extend(data)
                print(f"  BAL {year}: {len(data)} records")
    
    print(f"  Total: {len(all_data)} records")
    return all_data

# -----------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------

def main():
    print("\n" + "="*70)
    print("COMPREHENSIVE DATA SCRAPER - CASE STUDY TEAMS")
    print("="*70)
    print(f"\nTarget: {len(CASE_STUDY_TEAMS)} teams")
    print(f"Sources: {len(DATA_SOURCES)}")
    
    for team in CASE_STUDY_TEAMS:
        print(f"\n{'#'*70}")
        print(f"TEAM: {team}")
        print(f"{'#'*70}")
    
    print("\n" + "="*70)
    print("Press Enter to start scraping (this will take ~15-20 minutes)")
    print("="*70)
    input()
    
    all_data = {}
    
    for team_name in CASE_STUDY_TEAMS:
        print(f"\n\n{'█'*70}")
        print(f"█  SCRAPING: {team_name}")
        print(f"{'█'*70}")
        
        team_data = {
            "rtb_2025": [],
            "fiba_history": [],
            "bal_teams": [],
            "bal_stats": [],
            "basketball24": []
        }
        
        # Scrape each source
        try:
            team_data["rtb_2025"] = scrape_road_to_bal_2025(team_name)
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ RTB 2025 failed: {e}")
        
        try:
            team_data["fiba_history"] = scrape_fiba_history(team_name)
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ FIBA History failed: {e}")
        
        try:
            team_data["bal_teams"] = scrape_bal_nba_teams(team_name)
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ BAL Teams failed: {e}")
        
        try:
            team_data["bal_stats"] = scrape_bal_nba_stats(team_name)
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ BAL Stats failed: {e}")
        
        try:
            team_data["basketball24"] = scrape_basketball24(team_name)
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ Basketball24 failed: {e}")
        
        all_data[team_name] = team_data
        
        # Summary
        total = sum(len(v) for v in team_data.values())
        print(f"\n✓ {team_name}: {total} total records")
        
        time.sleep(3)  # Rate limiting between teams
    
    # Save all data
    print("\n" + "="*70)
    print("SAVING DATA")
    print("="*70)
    
    all_records = []
    for team_name, sources in all_data.items():
        for source_name, records in sources.items():
            for record in records:
                record["source"] = source_name
                all_records.append(record)
    
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv("case_study_teams_comprehensive_data.csv", index=False)
        print(f"\n✓ case_study_teams_comprehensive_data.csv")
        print(f"  Total records: {len(df)}")
        
        # Create summary by team
        summary = []
        for team in CASE_STUDY_TEAMS:
            team_records = df[df['team'] == team]
            summary.append({
                "Team": team,
                "Total Records": len(team_records),
                "RTB 2025": len(team_records[team_records['source'] == 'rtb_2025']),
                "FIBA History": len(team_records[team_records['source'] == 'fiba_history']),
                "BAL Teams": len(team_records[team_records['source'] == 'bal_teams']),
                "BAL Stats": len(team_records[team_records['source'] == 'bal_stats']),
                "Basketball24": len(team_records[team_records['source'] == 'basketball24'])
            })
        
        df_summary = pd.DataFrame(summary)
        df_summary.to_csv("scraping_summary_by_team.csv", index=False)
        print(f"\n✓ scraping_summary_by_team.csv")
        print("\n" + df_summary.to_string(index=False))
    
    print("\n" + "="*70)
    print("SCRAPING COMPLETE!")
    print("="*70)
    print("\nNext: Review data and upload to Google Sheets")

if __name__ == "__main__":
    main()
