"""
Scrape historical BAL data for all 7 teams in the case study
Uses Afrobasket and available sources for each team
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# -----------------------------------------------------------------
# CONFIGURATION - 7 Teams Case Study
# -----------------------------------------------------------------

TEAMS_CONFIG = {
    # GROUP A - Tier 1
    "Nairobi City Thunder": {
        "tier": "Tier 1 (BAL Vet)",
        "narrative": "The Hosts - 2025 BAL debutants",
        "afrobasket_url": "https://basketball.afrobasket.com/team/Nairobi-City-Thunder/17638/Stats",
        "has_bal_history": True,
        "bal_season": "2025"
    },
    
    # GROUP A - Tier 2
    "Namuwongo Blazers": {
        "tier": "Tier 2 (New Guard)",
        "narrative": "The Kingslayers - First Ugandan NBL title",
        "search_terms": ["Namuwongo", "Blazers"],
        "has_bal_history": False
    },
    
    "Johannesburg Giants": {
        "tier": "Tier 2 (New Guard)",
        "narrative": "The Undefeated - Perfect 5-0 in qualifiers",
        "search_terms": ["Johannesburg", "Giants"],
        "has_bal_history": False,
        "qualifier_group": "E",
        "qualifier_record": "5-0"
    },
    
    # GROUP B - Tier 1
    "Ferroviario Da Beira": {
        "tier": "Tier 1 (BAL Vet)",
        "narrative": "The Juggernaut - 2x BAL main (2022, 2023)",
        "fiba_url": "https://www.fiba.basketball/en/history/109-basketball-africa-league/208481/teams/ferroviario-da-beira",
        "afrobasket_search": "Ferroviario Beira",
        "has_bal_history": True,
        "bal_seasons": ["2022", "2023"]
    },
    
    # GROUP B - Tier 2
    "Matero Magic": {
        "tier": "Tier 2",
        "narrative": "The Road Warriors - Zambian champions",
        "search_terms": ["Matero", "Magic"],
        "has_bal_history": False,
        "qualifier_group": "E",
        "qualifier_record": "3-2"
    },
    
    # GROUP B - Tier 3
    "Dar City": {
        "tier": "Tier 3 (Dark Horse)",
        "narrative": "Star-Powered Unknown with elite talent",
        "search_terms": ["Dar City", "Dar"],
        "has_bal_history": False,
        "qualifier_group": "D",
        "key_players": ["Solo Diabate", "Raphiael Putney"]
    },
    
    "Bravehearts": {
        "tier": "Tier 3",
        "narrative": "The Underdogs - 5x Malawian champions",
        "search_terms": ["Bravehearts", "Brave Hearts"],
        "has_bal_history": False,
        "qualifier_group": "E",
        "qualifier_record": "2-3",
        "h2h_note": "Lost to NCT 68-91 in previous qualifier"
    }
}

# -----------------------------------------------------------------
# SCRAPING FUNCTIONS
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
        print(f"  ❌ Error: {e}")
        return None

def extract_table_data(soup, team_name):
    """Extract data from HTML tables"""
    data = []
    tables = soup.find_all("table")
    
    for table_idx, table in enumerate(tables):
        try:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data and len(row_data) > 1:
                    data.append({
                        "team": team_name,
                        "table_index": table_idx,
                        "data": " | ".join(row_data)
                    })
        except Exception as e:
            continue
    
    return data

def scrape_afrobasket_team(team_name, url):
    """Scrape team data from Afrobasket"""
    print(f"\n{'='*60}")
    print(f"Scraping Afrobasket: {team_name}")
    print(f"{'='*60}")
    
    soup = get_page(url)
    if not soup:
        return []
    
    all_data = extract_table_data(soup, team_name)
    
    # Parse specific stats
    stats = []
    
    # Look for team summary stats
    text = soup.get_text()
    
    stat_patterns = {
        'PPG': r'Points per game.*?(\d+\.?\d*)',
        '2FG%': r'2FGP%.*?(\d+\.?\d*%)',
        '3FG%': r'3FGP%.*?(\d+\.?\d*%)',
        'FT%': r'FT%.*?(\d+\.?\d*%)',
        'RPG': r'Total rebounds.*?(\d+\.?\d*)',
        'APG': r'Assists per game.*?(\d+\.?\d*)',
        'TOV': r'Turnovers per game.*?(\d+\.?\d*)',
    }
    
    import re
    for stat_name, pattern in stat_patterns.items():
        match = re.search(pattern, text)
        if match:
            stats.append({
                "team": team_name,
                "metric": stat_name,
                "value": match.group(1)
            })
    
    print(f"  ✓ Extracted {len(all_data)} table rows")
    print(f"  ✓ Found {len(stats)} key stats")
    
    return all_data, stats

def scrape_fiba_history(team_name, url):
    """Scrape from FIBA history pages"""
    print(f"\n{'='*60}")
    print(f"Scraping FIBA History: {team_name}")
    print(f"{'='*60}")
    
    soup = get_page(url)
    if not soup:
        return []
    
    all_data = extract_table_data(soup, team_name)
    
    print(f"  ✓ Extracted {len(all_data)} records")
    return all_data

def search_afrobasket_team(team_name, search_term):
    """Search for team on Afrobasket"""
    print(f"\n{'='*60}")
    print(f"Searching Afrobasket: {team_name}")
    print(f"{'='*60}")
    
    # Try common Afrobasket URL patterns
    search_urls = [
        f"https://basketball.afrobasket.com/search?q={search_term.replace(' ', '+')}",
        f"https://basketball.afrobasket.com/team/{search_term.replace(' ', '-')}/Stats"
    ]
    
    for url in search_urls:
        soup = get_page(url, delay=3)
        if soup:
            # Check if we found the team
            text = soup.get_text().lower()
            if team_name.lower() in text:
                print(f"  ✓ Found team data")
                return extract_table_data(soup, team_name)
    
    print(f"  ⚠ No data found")
    return []

def create_team_summary(team_name, config, scraped_data):
    """Create summary for a team"""
    return {
        "Team": team_name,
        "Tier": config["tier"],
        "Narrative": config["narrative"],
        "BAL History": "Yes" if config.get("has_bal_history") else "No",
        "BAL Seasons": ", ".join(config.get("bal_seasons", [])) if config.get("bal_seasons") else config.get("bal_season", "N/A"),
        "Qualifier Group": config.get("qualifier_group", "N/A"),
        "Qualifier Record": config.get("qualifier_record", "N/A"),
        "Data Records Found": len(scraped_data),
        "Key Players": ", ".join(config.get("key_players", [])) if config.get("key_players") else "N/A",
        "Notes": config.get("h2h_note", "")
    }

# -----------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------

def main():
    print("\n" + "="*70)
    print("COMPREHENSIVE TEAM DATA SCRAPER - 7 TEAMS CASE STUDY")
    print("="*70)
    print(f"\nTarget: {len(TEAMS_CONFIG)} teams")
    
    all_raw_data = []
    all_stats = []
    team_summaries = []
    
    for team_name, config in TEAMS_CONFIG.items():
        print(f"\n{'#'*70}")
        print(f"PROCESSING: {team_name}")
        print(f"Tier: {config['tier']}")
        print(f"{'#'*70}")
        
        team_data = []
        team_stats = []
        
        # Scrape based on available sources
        if config.get("afrobasket_url"):
            data, stats = scrape_afrobasket_team(team_name, config["afrobasket_url"])
            team_data.extend(data)
            team_stats.extend(stats)
        
        elif config.get("fiba_url"):
            data = scrape_fiba_history(team_name, config["fiba_url"])
            team_data.extend(data)
        
        elif config.get("search_terms"):
            for term in config["search_terms"]:
                data = search_afrobasket_team(team_name, term)
                team_data.extend(data)
                if data:
                    break  # Stop if we found data
        
        # Create summary
        summary = create_team_summary(team_name, config, team_data)
        team_summaries.append(summary)
        
        all_raw_data.extend(team_data)
        all_stats.extend(team_stats)
        
        print(f"\n✓ {team_name}: {len(team_data)} records collected")
        time.sleep(3)  # Rate limiting
    
    # Save all data
    print("\n" + "="*70)
    print("SAVING DATA")
    print("="*70)
    
    # 1. Team summaries
    if team_summaries:
        df = pd.DataFrame(team_summaries)
        df.to_csv("all_teams_summary.csv", index=False)
        print(f"\n✓ all_teams_summary.csv ({len(df)} teams)")
        print("\n" + df.to_string(index=False))
    
    # 2. Raw scraped data
    if all_raw_data:
        df = pd.DataFrame(all_raw_data)
        df.to_csv("all_teams_raw_data.csv", index=False)
        print(f"\n✓ all_teams_raw_data.csv ({len(df)} records)")
    
    # 3. Extracted stats
    if all_stats:
        df = pd.DataFrame(all_stats)
        df.to_csv("all_teams_stats.csv", index=False)
        print(f"\n✓ all_teams_stats.csv ({len(df)} stats)")
    
    print("\n" + "="*70)
    print("SCRAPING COMPLETE!")
    print("="*70)
    print("\nFiles created:")
    print("  1. all_teams_summary.csv - Overview of all 7 teams")
    print("  2. all_teams_raw_data.csv - All scraped data")
    print("  3. all_teams_stats.csv - Extracted statistics")
    print("\nNext: Run upload_all_data.py to push to Google Sheets")

if __name__ == "__main__":
    main()
