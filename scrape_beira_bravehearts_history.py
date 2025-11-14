import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

def scrape_ferroviario_beira_history():
    """
    Scrape Ferroviario Da Beira's BAL history (2022, 2023)
    """
    print("=" * 80)
    print("SCRAPING FERROVIARIO DA BEIRA HISTORICAL DATA")
    print("=" * 80)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_data = []
    
    # FIBA History page
    fiba_url = "https://www.fiba.basketball/en/history/109-basketball-africa-league/208481/teams/ferroviario-da-beira"
    print(f"\n1. Fetching FIBA History: {fiba_url}")
    
    try:
        response = requests.get(fiba_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open('beira_fiba_history.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("  ✓ Saved HTML to beira_fiba_history.html")
        
        # Look for statistics tables
        tables = soup.find_all('table')
        print(f"  Found {len(tables)} tables")
        
        # Look for team records
        stats_sections = soup.find_all(['div', 'section'], class_=lambda x: x and 'stat' in str(x).lower())
        print(f"  Found {len(stats_sections)} stat sections")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    time.sleep(2)
    
    # Try Afrobasket - search for Ferroviario
    afrobasket_search_url = "https://basketball.afrobasket.com/search.asp?search=Ferroviario"
    print(f"\n2. Searching Afrobasket: {afrobasket_search_url}")
    
    try:
        response = requests.get(afrobasket_search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for team links
        team_links = soup.find_all('a', href=lambda x: x and 'team' in str(x).lower())
        print(f"  Found {len(team_links)} team links")
        
        for link in team_links[:5]:
            print(f"    - {link.get_text(strip=True)}: {link.get('href')}")
            
            # Try to access team page
            team_url = link.get('href')
            if not team_url.startswith('http'):
                team_url = 'https://basketball.afrobasket.com/' + team_url
            
            print(f"\n    Accessing: {team_url}")
            time.sleep(2)
            
            try:
                team_response = requests.get(team_url, headers=headers, timeout=15)
                team_response.raise_for_status()
                team_soup = BeautifulSoup(team_response.content, 'html.parser')
                
                # Look for stats tables
                stats_tables = team_soup.find_all('table')
                if stats_tables:
                    print(f"      ✓ Found {len(stats_tables)} stat tables")
                    
                    for idx, table in enumerate(stats_tables[:3]):
                        rows = table.find_all('tr')
                        print(f"        Table {idx+1}: {len(rows)} rows")
                        
                        # Try to parse table
                        for row in rows[:5]:
                            cells = row.find_all(['td', 'th'])
                            if cells:
                                print(f"          {[cell.get_text(strip=True) for cell in cells]}")
                
            except Exception as e:
                print(f"      ✗ Error accessing team page: {e}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    time.sleep(2)
    
    # Try Basketball24 for BAL 2022 and 2023
    for year in [2022, 2023]:
        b24_url = f"https://www.basketball24.com/africa/bal-{year}/"
        print(f"\n3. Fetching Basketball24 BAL {year}: {b24_url}")
        
        try:
            response = requests.get(b24_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Ferroviario in standings or teams
            page_text = soup.get_text()
            if 'Ferroviario' in page_text or 'Beira' in page_text:
                print(f"  ✓ Found Ferroviario mention in BAL {year}")
                
                # Save HTML
                with open(f'beira_bal_{year}_b24.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print(f"  ✓ Saved to beira_bal_{year}_b24.html")
            else:
                print(f"  ✗ Ferroviario not found in BAL {year}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        time.sleep(2)
    
    # Try direct Afrobasket team ID search
    # Common pattern: /team/Team-Name/XXXXX/Stats
    possible_ids = [17639, 17640, 17641, 17642, 17643, 17644, 17645]
    
    print(f"\n4. Trying Afrobasket direct team IDs...")
    for team_id in possible_ids:
        url = f"https://basketball.afrobasket.com/team/Ferroviario-da-Beira/{team_id}/Stats"
        print(f"\n  Trying ID {team_id}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"    ✓ SUCCESS! Found team page")
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Save HTML
                with open(f'beira_afrobasket_{team_id}.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print(f"    ✓ Saved to beira_afrobasket_{team_id}.html")
                
                # Look for stats
                tables = soup.find_all('table')
                print(f"    ✓ Found {len(tables)} tables")
                
                break
            else:
                print(f"    ✗ {response.status_code}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        time.sleep(1)
    
    return all_data

def scrape_bravehearts_history():
    """
    Scrape Bravehearts historical data
    """
    print("\n\n" + "=" * 80)
    print("SCRAPING BRAVEHEARTS HISTORICAL DATA")
    print("=" * 80)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_data = []
    
    # Try Afrobasket search
    afrobasket_search_url = "https://basketball.afrobasket.com/search.asp?search=Bravehearts"
    print(f"\n1. Searching Afrobasket: {afrobasket_search_url}")
    
    try:
        response = requests.get(afrobasket_search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for team links
        team_links = soup.find_all('a', href=lambda x: x and 'team' in str(x).lower())
        print(f"  Found {len(team_links)} team links")
        
        for link in team_links[:5]:
            print(f"    - {link.get_text(strip=True)}: {link.get('href')}")
            
            team_url = link.get('href')
            if not team_url.startswith('http'):
                team_url = 'https://basketball.afrobasket.com/' + team_url
            
            print(f"\n    Accessing: {team_url}")
            time.sleep(2)
            
            try:
                team_response = requests.get(team_url, headers=headers, timeout=15)
                team_response.raise_for_status()
                team_soup = BeautifulSoup(team_response.content, 'html.parser')
                
                # Save HTML
                with open('bravehearts_afrobasket_page.html', 'w', encoding='utf-8') as f:
                    f.write(team_soup.prettify())
                print(f"      ✓ Saved to bravehearts_afrobasket_page.html")
                
                # Look for stats
                stats_tables = team_soup.find_all('table')
                if stats_tables:
                    print(f"      ✓ Found {len(stats_tables)} stat tables")
                    
                    for idx, table in enumerate(stats_tables):
                        rows = table.find_all('tr')
                        print(f"        Table {idx+1}: {len(rows)} rows")
                
            except Exception as e:
                print(f"      ✗ Error: {e}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    time.sleep(2)
    
    # Try direct team ID search
    possible_ids = [17646, 17647, 17648, 17649, 17650]
    
    print(f"\n2. Trying Afrobasket direct team IDs...")
    for team_id in possible_ids:
        url = f"https://basketball.afrobasket.com/team/Bravehearts/{team_id}/Stats"
        print(f"\n  Trying ID {team_id}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"    ✓ SUCCESS! Found team page")
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Save HTML
                with open(f'bravehearts_afrobasket_{team_id}.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print(f"    ✓ Saved to bravehearts_afrobasket_{team_id}.html")
                
                # Look for stats
                tables = soup.find_all('table')
                print(f"    ✓ Found {len(tables)} tables")
                
                break
            else:
                print(f"    ✗ {response.status_code}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        time.sleep(1)
    
    # Try searching for Elite 16 history
    print(f"\n3. Searching for Road to BAL Elite 16 history...")
    
    # Try FIBA search
    fiba_search_url = "https://www.fiba.basketball/en/search?q=Bravehearts"
    print(f"\n  FIBA Search: {fiba_search_url}")
    
    try:
        response = requests.get(fiba_search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for team results
        results = soup.find_all(['a', 'div'], class_=lambda x: x and 'result' in str(x).lower())
        print(f"  Found {len(results)} results")
        
        for result in results[:5]:
            print(f"    - {result.get_text(strip=True)[:100]}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return all_data

def main():
    print("COMPREHENSIVE HISTORICAL DATA SCRAPER")
    print("Ferroviario Da Beira (2022, 2023 BAL)")
    print("Bravehearts (Elite 16 history)")
    print("=" * 80)
    
    # Scrape Ferroviario Da Beira
    beira_data = scrape_ferroviario_beira_history()
    
    # Scrape Bravehearts
    bravehearts_data = scrape_bravehearts_history()
    
    print("\n\n" + "=" * 80)
    print("SCRAPING COMPLETE")
    print("=" * 80)
    print("\nFiles created:")
    print("- beira_fiba_history.html")
    print("- beira_bal_2022_b24.html (if found)")
    print("- beira_bal_2023_b24.html (if found)")
    print("- beira_afrobasket_*.html (if found)")
    print("- bravehearts_afrobasket_page.html")
    print("- bravehearts_afrobasket_*.html (if found)")
    print("\nNext steps:")
    print("1. Review HTML files for data structure")
    print("2. Extract specific stats from tables")
    print("3. Parse player data")
    print("4. Compile into comprehensive CSV")

if __name__ == "__main__":
    main()
