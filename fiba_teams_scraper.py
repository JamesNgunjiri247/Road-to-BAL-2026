import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# -----------------------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------------------
URL = "https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026/teams"
OUTPUT_FILE = "teams_roster_links.csv"
BASE_URL = "https://www.fiba.basketball"

# -----------------------------------------------------------------
# 2. SCRAPING LOGIC
# -----------------------------------------------------------------
def scrape_fiba_teams(url):
    print(f"Starting scrape from {url}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        
        teams_data = []

        # TARGET: We found 'data-testid="team-card"' in your source code.
        # This is the most robust way to find the team containers.
        team_cards = soup.find_all("a", attrs={"data-testid": "team-card"})

        if not team_cards:
            print("--- WARNING: No team cards found. ---")
            return

        print(f"SUCCESS: Found {len(team_cards)} teams. Extracting details...")

        for card in team_cards:
            try:
                # 1. Extract Link (It's in the 'href' of the <a> tag)
                partial_link = card.get('href')
                full_link = BASE_URL + partial_link if partial_link else "N/A"
                
                # 2. Extract Team Name (Inside the <h2> tag)
                name_tag = card.find("h2")
                team_name = name_tag.get_text(strip=True) if name_tag else "N/A"
                
                # 3. Extract Team Code (The abbreviation like 'AHL')
                # In your source, the code is in a <span> that follows the <h2>
                # Structure: <h2>Name</h2> <span class="r79..."> <div>CODE</div> </span>
                code = "N/A"
                if name_tag:
                    # Find the next sibling span that contains the code
                    code_container = name_tag.find_next_sibling("span")
                    if code_container:
                        code = code_container.get_text(strip=True)

                # Append to our list
                teams_data.append({
                    "team_name": team_name,
                    "team_code": code,
                    "profile_url": full_link,
                    "team_slug": partial_link.split('/')[-1] if partial_link else "N/A"
                })

            except Exception as e:
                print(f"Error extracting a card: {e}")
                continue

        return teams_data

    except requests.exceptions.RequestException as e:
        print(f"Error during network request: {e}")
        return []

# -----------------------------------------------------------------
# 3. EXECUTION
# -----------------------------------------------------------------
if __name__ == "__main__":
    data = scrape_fiba_teams(URL)

    if data:
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        df.to_csv(OUTPUT_FILE, index=False)
        
        print("-" * 50)
        print(f"SUCCESS: Data saved to {OUTPUT_FILE}")
        print(f"Total Teams: {len(df)}")
        print("-" * 50)
        print(df.head())
    else:
        print("Scrape failed or found no data.")