import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_elite16_standings():
    """
    Scrape Road to BAL 2026 Elite 16 standings from FIBA website
    Focus on case study teams in Groups A and B
    """
    
    url = "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/standings"
    
    print(f"Fetching data from: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Case study teams mapping
        case_study_teams = {
            'NCT': 'Nairobi City Thunder',
            'NAM': 'Namuwongo Blazers',
            'JOH': 'Johannesburg Giants',
            'FBE': 'Ferroviario Da Beira',
            'MMA': 'Matero Magic',
            'DAR': 'Dar City',
            'BHB': 'Bravehearts'
        }
        
        all_standings = []
        
        # Look for group standings sections
        # Try multiple possible HTML structures
        
        # Method 1: Find tables
        tables = soup.find_all('table')
        if tables:
            print(f"Found {len(tables)} tables")
            for idx, table in enumerate(tables):
                print(f"\nProcessing table {idx + 1}")
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 4:
                        row_data = [cell.get_text(strip=True) for cell in cells]
                        print(f"  Row: {row_data}")
        
        # Method 2: Find divs with group data
        group_sections = soup.find_all(['div', 'section'], class_=lambda x: x and ('group' in x.lower() or 'standing' in x.lower()))
        if group_sections:
            print(f"\nFound {len(group_sections)} group sections")
            for section in group_sections:
                print(f"Section: {section.get('class', 'No class')}")
        
        # Method 3: Search for specific team codes
        print("\n\nSearching for case study team codes in page...")
        page_text = soup.get_text()
        for code, full_name in case_study_teams.items():
            if code in page_text:
                print(f"✓ Found: {code} ({full_name})")
            else:
                print(f"✗ Not found: {code} ({full_name})")
        
        # Method 4: Extract all text content and look for patterns
        print("\n\nExtracting structured data...")
        
        # Find all elements that might contain standings
        potential_standings = soup.find_all(['li', 'div', 'tr'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['team', 'standing', 'rank', 'row']
        ))
        
        if potential_standings:
            print(f"Found {len(potential_standings)} potential standing elements")
            for elem in potential_standings[:20]:  # Show first 20
                text = elem.get_text(strip=True)
                if any(code in text for code in case_study_teams.keys()):
                    print(f"  Relevant: {text[:100]}")
        
        # Method 5: Save raw HTML for analysis
        print("\n\nSaving raw HTML for manual inspection...")
        with open('standings_raw.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("✓ Saved to standings_raw.html")
        
        # Method 6: Try to find JavaScript data
        scripts = soup.find_all('script')
        print(f"\n\nFound {len(scripts)} script tags")
        for idx, script in enumerate(scripts):
            script_content = script.string
            if script_content and any(code in script_content for code in case_study_teams.keys()):
                print(f"\nScript {idx} contains team data:")
                # Save relevant scripts
                with open(f'standings_script_{idx}.js', 'w', encoding='utf-8') as f:
                    f.write(script_content)
                print(f"  ✓ Saved to standings_script_{idx}.js")
        
        # Try to extract standings data from visible elements
        print("\n\n" + "="*80)
        print("ATTEMPTING DATA EXTRACTION")
        print("="*80)
        
        # Look for group headers
        groups = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']
        
        for group_name in groups:
            print(f"\n\nSearching for {group_name}...")
            
            # Find group header
            group_header = soup.find(string=lambda text: text and group_name in text)
            if group_header:
                print(f"✓ Found {group_name} header")
                parent = group_header.find_parent()
                
                # Try to find standings table near this header
                if parent:
                    # Look for siblings or children with team data
                    siblings = parent.find_next_siblings(limit=10)
                    for sibling in siblings:
                        text = sibling.get_text(strip=True)
                        if any(code in text for code in case_study_teams.keys()):
                            print(f"  Team data found: {text[:150]}")
                            
                            # Try to parse this element
                            team_elements = sibling.find_all(['div', 'li', 'tr'])
                            for team_elem in team_elements:
                                team_text = team_elem.get_text(strip=True)
                                # Look for pattern: TEAM_CODE W/L PTS
                                for code, full_name in case_study_teams.items():
                                    if code in team_text:
                                        print(f"    Parsing: {code} - {team_text}")
                                        all_standings.append({
                                            'Group': group_name,
                                            'Team_Code': code,
                                            'Team_Name': full_name,
                                            'Raw_Data': team_text
                                        })
        
        # Create DataFrame
        if all_standings:
            df = pd.DataFrame(all_standings)
            print(f"\n\n✓ Extracted {len(df)} records")
            print(df)
            
            # Save to CSV
            output_file = 'elite16_standings_raw.csv'
            df.to_csv(output_file, index=False)
            print(f"\n✓ Saved to {output_file}")
            return df
        else:
            print("\n\n⚠ No structured data extracted")
            print("The page likely uses JavaScript to load standings dynamically")
            print("\nRECOMMENDATION:")
            print("1. Check standings_raw.html for page structure")
            print("2. Check standings_script_*.js files for data")
            print("3. Consider using Selenium for JavaScript-rendered content")
            print("4. Or manually extract data from the page")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching page: {e}")
        return None

if __name__ == "__main__":
    print("Road to BAL 2026 Elite 16 Standings Scraper")
    print("=" * 80)
    scrape_elite16_standings()
