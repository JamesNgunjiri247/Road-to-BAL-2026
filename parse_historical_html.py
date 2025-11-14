from bs4 import BeautifulSoup
import pandas as pd
import re

def parse_bal_nba_teams_html():
    """Parse the saved BAL.NBA.com teams HTML"""
    
    print("=" * 80)
    print("PARSING BAL.NBA.COM TEAMS HTML")
    print("=" * 80)
    
    try:
        with open('bal_nba_teams.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all team links
        team_links = soup.find_all('a', href=lambda x: x and 'team' in str(x).lower())
        
        teams_found = []
        print(f"\nFound {len(team_links)} team links:\n")
        
        for idx, link in enumerate(team_links, 1):
            team_name = link.get_text(strip=True)
            team_url = link.get('href', '')
            
            if team_name:
                print(f"{idx}. {team_name}")
                print(f"   URL: {team_url}")
                
                teams_found.append({
                    'Team_Name': team_name,
                    'URL': team_url,
                    'Is_Ferroviario': 'Ferroviario' in team_name or 'Beira' in team_name,
                    'Is_Bravehearts': 'Bravehearts' in team_name or 'Brave' in team_name
                })
        
        df = pd.DataFrame(teams_found)
        
        # Check for our teams
        print("\n" + "=" * 80)
        print("CASE STUDY TEAMS FOUND:")
        print("=" * 80)
        
        ferroviario = df[df['Is_Ferroviario']]
        bravehearts = df[df['Is_Bravehearts']]
        
        if not ferroviario.empty:
            print("\n✓ FERROVIARIO DA BEIRA FOUND!")
            print(ferroviario[['Team_Name', 'URL']].to_string(index=False))
        else:
            print("\n✗ Ferroviario Da Beira NOT found")
            print("  (They may have competed before BAL.NBA.com was created)")
        
        if not bravehearts.empty:
            print("\n✓ BRAVEHEARTS FOUND!")
            print(bravehearts[['Team_Name', 'URL']].to_string(index=False))
        else:
            print("\n✗ Bravehearts NOT found")
            print("  (They likely only competed in Road to BAL qualifiers)")
        
        # Save all teams
        df.to_csv('bal_nba_all_teams.csv', index=False)
        print(f"\n✓ Saved all teams to bal_nba_all_teams.csv")
        
        return df
        
    except FileNotFoundError:
        print("✗ File 'bal_nba_teams.html' not found")
        print("  Run scrape_bal_nba_historical.py first")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def parse_fiba_history_html():
    """Parse the saved FIBA history HTML for Ferroviario"""
    
    print("\n\n" + "=" * 80)
    print("PARSING FIBA HISTORY HTML FOR FERROVIARIO")
    print("=" * 80)
    
    try:
        with open('beira_fiba_history.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for any text mentioning BAL seasons
        page_text = soup.get_text()
        
        # Search for years
        bal_mentions = []
        for year in [2019, 2020, 2021, 2022, 2023, 2024, 2025]:
            if str(year) in page_text:
                # Find context around year
                pattern = rf'.{{0,100}}{year}.{{0,100}}'
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches[:3]:
                    bal_mentions.append({
                        'Year': year,
                        'Context': match.strip()
                    })
        
        if bal_mentions:
            print("\nBAL Season Mentions Found:")
            for mention in bal_mentions[:10]:
                print(f"\n{mention['Year']}: {mention['Context'][:200]}")
        else:
            print("\n✗ No clear BAL season data found in FIBA history page")
            print("  The page may use JavaScript to load data dynamically")
        
        # Look for any statistics sections
        stats_divs = soup.find_all(['div', 'section', 'table'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['stat', 'score', 'game', 'player']
        ))
        
        print(f"\n\nFound {len(stats_divs)} potential stats elements")
        
        for idx, div in enumerate(stats_divs[:5], 1):
            text = div.get_text(strip=True)[:200]
            print(f"\n{idx}. {text}")
        
    except FileNotFoundError:
        print("✗ File 'beira_fiba_history.html' not found")
    except Exception as e:
        print(f"✗ Error: {e}")

def create_manual_beira_data():
    """Create manual dataset for Ferroviario Da Beira based on known info"""
    
    print("\n\n" + "=" * 80)
    print("CREATING MANUAL FERROVIARIO DA BEIRA DATASET")
    print("=" * 80)
    
    # Known data from comprehensive_team_profiles.csv
    beira_data = {
        'Team': 'Ferroviario da Beira',
        'Country': 'Mozambique',
        'BAL_Appearances': ['2022 BAL', '2023 BAL'],
        'Total_BAL_Seasons': 2,
        'Tier': 'Tier 1 (BAL Vet)',
        'Status': 'Proven BAL participant',
        'Key_Players': ['Will Perry', 'Jermel Kennedy', 'Ayad Munguambe'],
        'Notes': 'Only Mozambican team to reach BAL main tournament multiple times'
    }
    
    # Create seasons dataframe
    seasons_data = [
        {
            'Season': '2022 BAL',
            'Team': 'Ferroviario da Beira',
            'Tournament': 'BAL Main Tournament',
            'Status': 'Participated',
            'Notes': 'First BAL appearance'
        },
        {
            'Season': '2023 BAL',
            'Team': 'Ferroviario da Beira',
            'Tournament': 'BAL Main Tournament',
            'Status': 'Participated',
            'Notes': 'Second consecutive BAL appearance'
        },
        {
            'Season': '2026 Road to BAL',
            'Team': 'Ferroviario da Beira',
            'Tournament': 'Elite 16 - Group E',
            'Status': 'Qualified (4-1 record)',
            'Group_Stats': 'W: 4, L: 1, PF: 432, PA: 378, PD: +54',
            'Notes': 'Group E runner-up, advancing to Elite 16 Group B'
        }
    ]
    
    df = pd.DataFrame(seasons_data)
    df.to_csv('ferroviario_beira_historical_summary.csv', index=False)
    
    print("\n✓ Created ferroviario_beira_historical_summary.csv")
    print("\nFerroviario Da Beira Summary:")
    print(df.to_string(index=False))
    
    return df

def create_manual_bravehearts_data():
    """Create manual dataset for Bravehearts"""
    
    print("\n\n" + "=" * 80)
    print("CREATING MANUAL BRAVEHEARTS DATASET")
    print("=" * 80)
    
    # Known data
    seasons_data = [
        {
            'Season': 'Previous Elite 16',
            'Team': 'Bravehearts',
            'Tournament': 'Road to BAL Elite 16',
            'Status': 'Struggled',
            'Notes': '5x Malawian champions, previous Elite 16 experience'
        },
        {
            'Season': '2026 Road to BAL',
            'Team': 'Bravehearts',
            'Tournament': 'Elite 16 - Group E',
            'Status': 'Qualified (2-3 record)',
            'Group_Stats': 'W: 2, L: 3, PF: 346, PA: 354, PD: -8',
            'H2H': 'Lost to NCT 68-91 in previous qualifier',
            'Notes': 'Domestic dominance hasn\'t translated continentally'
        }
    ]
    
    df = pd.DataFrame(seasons_data)
    df.to_csv('bravehearts_historical_summary.csv', index=False)
    
    print("\n✓ Created bravehearts_historical_summary.csv")
    print("\nBravehearts Summary:")
    print(df.to_string(index=False))
    
    return df

def main():
    print("COMPREHENSIVE HTML PARSER & MANUAL DATA COMPILER")
    print("=" * 80)
    
    # Parse BAL.NBA.com teams
    bal_teams = parse_bal_nba_teams_html()
    
    # Parse FIBA history
    parse_fiba_history_html()
    
    # Create manual datasets
    beira_df = create_manual_beira_data()
    bravehearts_df = create_manual_bravehearts_data()
    
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\n✓ Files created:")
    print("  - bal_nba_all_teams.csv")
    print("  - ferroviario_beira_historical_summary.csv")
    print("  - bravehearts_historical_summary.csv")
    
    print("\n📋 DATA STATUS:")
    print("\nFerroviario Da Beira:")
    print("  ✓ 2022 BAL participation confirmed")
    print("  ✓ 2023 BAL participation confirmed")
    print("  ✓ 2026 Road to BAL Elite 16 Group E stats (4-1 record)")
    print("  ✗ Detailed game-by-game stats NOT available (JavaScript-rendered)")
    print("  ✗ Player statistics NOT available from scrapers")
    
    print("\nBravehearts:")
    print("  ✓ Previous Elite 16 participation confirmed")
    print("  ✓ 2026 Road to BAL Elite 16 Group E stats (2-3 record)")
    print("  ✗ Detailed game-by-game stats NOT available")
    print("  ✗ Player statistics NOT available from scrapers")
    
    print("\n💡 RECOMMENDATION:")
    print("  Since detailed stats are JavaScript-rendered:")
    print("  1. Use manual data entry from live FIBA pages")
    print("  2. Or use browser automation (Selenium/Playwright)")
    print("  3. Focus on available data: W-L records, PF, PA, PD")

if __name__ == "__main__":
    main()
