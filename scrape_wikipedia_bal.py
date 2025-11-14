"""
Scrape Road to BAL 2026 qualification data from Wikipedia
Wikipedia has complete static HTML tables with all the data we need
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# -----------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------

TARGET_TEAMS = {
    "Nairobi City Thunder": {"tier": "Tier 1", "group": "Finals Group A"},
    "Namuwongo Blazers": {"tier": "Tier 2", "group": "Finals Group A"},
    "Johannesburg Giants": {"tier": "Tier 2", "group": "Finals Group A"},
    "Ferroviario Da Beira": {"tier": "Tier 1", "group": "Finals Group B"},
    "Matero Magic": {"tier": "Tier 2", "group": "Finals Group B"},
    "Dar City": {"tier": "Tier 3", "group": "Finals Group B"},
    "Bravehearts": {"tier": "Tier 3", "group": "Finals Group B"},
}

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/2026_BAL_qualification"

# -----------------------------------------------------------------
# SCRAPING FUNCTIONS
# -----------------------------------------------------------------

def scrape_wikipedia_bal_qualification():
    """Scrape the comprehensive Wikipedia page for 2026 BAL qualification"""
    print("="*70)
    print("SCRAPING: Wikipedia - 2026 BAL Qualification")
    print("="*70)
    print(f"\nURL: {WIKIPEDIA_URL}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(WIKIPEDIA_URL, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        print("✓ Page loaded successfully\n")
        
        # Extract all tables
        tables = soup.find_all("table", class_="wikitable")
        print(f"Found {len(tables)} wikitables\n")
        
        all_standings = []
        all_results = []
        
        # Process each table
        for table_idx, table in enumerate(tables, 1):
            print(f"Processing Table {table_idx}...")
            
            # Get table caption/header to identify which group
            caption = table.find_previous(["h2", "h3", "h4"])
            group_name = caption.get_text(strip=True) if caption else f"Table {table_idx}"
            print(f"  Group/Section: {group_name}")
            
            # Extract headers
            headers = []
            header_row = table.find("tr")
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
            
            # Extract data rows
            rows = table.find_all("tr")[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all(["td", "th"])
                row_data = [cell.get_text(strip=True) for cell in cells]
                
                if not row_data or len(row_data) < 2:
                    continue
                
                # Check if this row contains any of our target teams
                row_text = " ".join(row_data)
                
                for team_name in TARGET_TEAMS.keys():
                    # Flexible matching (check for partial names)
                    team_words = team_name.split()
                    if any(word in row_text for word in team_words if len(word) > 4):
                        
                        record = {
                            "team": team_name,
                            "tier": TARGET_TEAMS[team_name]["tier"],
                            "group": group_name,
                            "table_index": table_idx,
                        }
                        
                        # Map columns dynamically
                        for i, header in enumerate(headers):
                            if i < len(row_data):
                                record[header] = row_data[i]
                        
                        all_standings.append(record)
                        print(f"    ✓ Found: {team_name}")
                        break
        
        print(f"\n{'='*70}")
        print(f"EXTRACTION COMPLETE")
        print(f"{'='*70}")
        print(f"Total records extracted: {len(all_standings)}")
        
        return all_standings
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return []

def save_to_csv(data, filename):
    """Save data to CSV"""
    if not data:
        print(f"\n⚠ No data to save for {filename}")
        return False
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved: {filename}")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    
    # Show preview
    print(f"\nPreview:")
    print(df.head().to_string())
    
    return True

# -----------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------

def main():
    print("\n" + "="*70)
    print("ROAD TO BAL 2026 - HISTORICAL DATA SCRAPER")
    print("="*70)
    print(f"\nTarget Teams: {len(TARGET_TEAMS)}")
    for team, info in TARGET_TEAMS.items():
        print(f"  - {team} ({info['tier']})")
    
    print("\n" + "="*70)
    print("PHASE 1: Wikipedia Qualification Data")
    print("="*70 + "\n")
    
    # Scrape Wikipedia
    qualification_data = scrape_wikipedia_bal_qualification()
    
    # Save data
    if qualification_data:
        save_to_csv(qualification_data, "bal_2026_qualification_data.csv")
    
    print("\n" + "="*70)
    print("SCRAPING COMPLETE!")
    print("="*70)
    
    if qualification_data:
        print(f"\n✓ Successfully scraped data for {len(qualification_data)} team records")
        print(f"✓ File: bal_2026_qualification_data.csv")
        print("\nNext steps:")
        print("  1. Review the CSV file")
        print("  2. Upload to Google Sheets using upload_to_sheets.py")
        print("  3. Additional data sources can be manually added from:")
        print("     - https://basketball.afrobasket.com/ (for detailed stats)")
        print("     - https://bal.nba.com/statistics (for BAL main tournament)")
    else:
        print("\n⚠ No data extracted. Check the Wikipedia page structure.")

if __name__ == "__main__":
    main()
