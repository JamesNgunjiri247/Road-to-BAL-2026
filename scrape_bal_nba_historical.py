import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_bal_nba_teams():
    """
    Scrape team data from BAL.NBA.com
    """
    print("=" * 80)
    print("SCRAPING BAL.NBA.COM FOR HISTORICAL TEAMS")
    print("=" * 80)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # BAL teams page
    teams_url = "https://bal.nba.com/teams"
    print(f"\n1. Fetching teams list: {teams_url}")
    
    try:
        response = requests.get(teams_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML
        with open('bal_nba_teams.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("  ✓ Saved to bal_nba_teams.html")
        
        # Look for team links
        team_links = soup.find_all('a', href=lambda x: x and 'team' in str(x).lower())
        print(f"  Found {len(team_links)} team links")
        
        teams_data = []
        
        for link in team_links[:20]:
            team_name = link.get_text(strip=True)
            team_url = link.get('href')
            
            if team_name and 'Ferroviario' in team_name or 'Beira' in team_name:
                print(f"\n  ✓ FOUND FERROVIARIO: {team_name}")
                print(f"    URL: {team_url}")
                
                # Access team page
                if not team_url.startswith('http'):
                    team_url = 'https://bal.nba.com' + team_url
                
                time.sleep(2)
                print(f"    Fetching team page...")
                
                try:
                    team_response = requests.get(team_url, headers=headers, timeout=15)
                    team_response.raise_for_status()
                    team_soup = BeautifulSoup(team_response.content, 'html.parser')
                    
                    # Save team page
                    with open('beira_bal_nba_team_page.html', 'w', encoding='utf-8') as f:
                        f.write(team_soup.prettify())
                    print(f"    ✓ Saved team page")
                    
                    # Look for stats
                    stats_tables = team_soup.find_all('table')
                    print(f"    Found {len(stats_tables)} tables")
                    
                    # Look for players
                    player_divs = team_soup.find_all(['div', 'section'], class_=lambda x: x and 'player' in str(x).lower())
                    print(f"    Found {len(player_divs)} player sections")
                    
                except Exception as e:
                    print(f"    ✗ Error accessing team page: {e}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    time.sleep(2)
    
    # Try BAL statistics page
    stats_url = "https://bal.nba.com/statistics"
    print(f"\n2. Fetching statistics page: {stats_url}")
    
    try:
        response = requests.get(stats_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML
        with open('bal_nba_statistics.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("  ✓ Saved to bal_nba_statistics.html")
        
        # Look for season selectors
        selectors = soup.find_all(['select', 'option'], id=lambda x: x and 'season' in str(x).lower())
        print(f"  Found {len(selectors)} season selectors")
        
        for selector in selectors[:5]:
            print(f"    - {selector.get_text(strip=True)}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    time.sleep(2)
    
    # Try specific BAL seasons
    for season in [2022, 2023]:
        season_url = f"https://bal.nba.com/season/{season}"
        print(f"\n3. Trying BAL {season} season: {season_url}")
        
        try:
            response = requests.get(season_url, headers=headers, timeout=15)
            if response.status_code == 200:
                print(f"  ✓ Page exists!")
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Save HTML
                with open(f'bal_nba_season_{season}.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print(f"  ✓ Saved to bal_nba_season_{season}.html")
                
                # Look for Ferroviario
                page_text = soup.get_text()
                if 'Ferroviario' in page_text or 'Beira' in page_text:
                    print(f"  ✓ Ferroviario found in {season} season!")
            else:
                print(f"  ✗ {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        time.sleep(2)
    
    print("\n\n" + "=" * 80)
    print("BAL.NBA.COM SCRAPING COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    scrape_bal_nba_teams()
