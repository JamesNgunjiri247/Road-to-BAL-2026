"""
Quick diagnostic script to see what's actually on the FIBA pages
"""

import requests
from bs4 import BeautifulSoup

def check_page(url, description):
    print(f"\n{'='*60}")
    print(f"Checking: {description}")
    print(f"URL: {url}")
    print('='*60)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Check for team mentions
        text = soup.get_text()
        
        teams_to_check = [
            "Nairobi", "Thunder", "NCT",
            "Namuwongo", "Blazers",
            "Johannesburg", "Giants",
            "Ferroviario", "Beira",
            "Matero", "Magic",
            "Dar City",
            "Bravehearts"
        ]
        
        print("\nTeam mentions found:")
        for team in teams_to_check:
            count = text.count(team)
            if count > 0:
                print(f"  ✓ '{team}': {count} times")
        
        # Check tables
        tables = soup.find_all("table")
        print(f"\nTables found: {len(tables)}")
        
        if tables:
            print("\nFirst table preview:")
            rows = tables[0].find_all("tr")[:5]
            for i, row in enumerate(rows, 1):
                cells = row.find_all(["td", "th"])
                row_text = " | ".join([c.get_text(strip=True) for c in cells])
                print(f"  Row {i}: {row_text[:100]}")
        
        # Check for game cards or divs
        game_divs = soup.find_all("div", class_=lambda x: x and ("game" in x.lower() or "match" in x.lower()))
        print(f"\nGame-related divs: {len(game_divs)}")
        
        print("\n✓ Page loaded successfully")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

# Check key pages
check_page(
    "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/games",
    "Road to BAL 2026 - Games"
)

check_page(
    "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/stats",
    "Road to BAL 2026 - Stats"
)

check_page(
    "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/standings",
    "Road to BAL 2026 - Standings"
)

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
