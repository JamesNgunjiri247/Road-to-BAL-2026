"""
Open-source data scraper for teams with no FIBA history
Targets multiple sources: Wikipedia, AfroBasket, Basketball Reference, news sites
Fetches, cleans, and validates data for live commentary and stats
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from datetime import datetime

# Target teams
TEAMS = {
    "namuwongo-blazers": {
        "name": "Namuwongo Blazers",
        "country": "Uganda",
        "league": "NBL Uganda",
        "tier": "Tier 2",
        "aliases": ["Namuwongo", "Blazers", "Nam Blazers"]
    },
    "johannesburg-giants": {
        "name": "Johannesburg Giants",
        "country": "South Africa",
        "league": "SA National Championship",
        "tier": "Tier 2",
        "aliases": ["Giants", "Joburg Giants", "JHB Giants"]
    },
    "matero-magic": {
        "name": "Matero Magic",
        "country": "Zambia",
        "league": "Zambia Basketball League",
        "tier": "Tier 2",
        "aliases": ["Matero", "Magic"]
    },
    "dar-city": {
        "name": "Dar City",
        "country": "Tanzania",
        "league": "Tanzania Basketball League",
        "tier": "Tier 3",
        "aliases": ["Dar es Salaam City", "Dar City Oilers"]
    }
}

# Data sources
DATA_SOURCES = {
    "wikipedia_uganda": "https://en.wikipedia.org/wiki/National_Basketball_League_(Uganda)",
    "wikipedia_sa": "https://en.wikipedia.org/wiki/Basketball_in_South_Africa",
    "wikipedia_zambia": "https://en.wikipedia.org/wiki/Sport_in_Zambia",
    "wikipedia_tanzania": "https://en.wikipedia.org/wiki/Sport_in_Tanzania",
    "afrobasket_teams": "https://basketball.afrobasket.com/AfricanClubs.asp",
    "realgm_africa": "https://basketball.realgm.com/international/league/4/African/teams",
    "flashscore_africa": "https://www.flashscore.com/basketball/",
}

def get_page(url):
    """Fetch page with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  ❌ Error fetching {url}: {e}")
        return None

def search_google_news(team_name, country):
    """Simulate Google News search for team"""
    print(f"\n  🔍 Google News search: '{team_name} basketball {country}'")
    print(f"     Suggested queries:")
    print(f"     - {team_name} roster 2025")
    print(f"     - {team_name} players stats")
    print(f"     - {team_name} {country} basketball league")
    print(f"     - {team_name} recent games results")
    
    return {
        "search_query": f"{team_name} basketball {country}",
        "suggested_sources": [
            f"News sites covering {country} basketball",
            f"{country} Basketball Federation website",
            f"Local sports media in {country}",
            "AfroBasket.com team profiles",
            "FlashScore team pages"
        ]
    }

def scrape_wikipedia_league(team_info, url):
    """Scrape Wikipedia pages for league information"""
    print(f"\n  📖 Scraping Wikipedia: {url}")
    
    html = get_page(url)
    if not html:
        return {}
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Save HTML for manual inspection
    filename = f"wikipedia_{team_info['name'].replace(' ', '_').lower()}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"     ✓ Saved to: {filename}")
    
    data = {
        "source": url,
        "team": team_info["name"],
        "found_mentions": []
    }
    
    # Search for team mentions
    text_content = soup.get_text()
    for alias in team_info["aliases"]:
        if alias.lower() in text_content.lower():
            # Find context around mention
            pattern = re.compile(f'.{{0,100}}{re.escape(alias)}.{{0,100}}', re.IGNORECASE)
            matches = pattern.findall(text_content)
            if matches:
                data["found_mentions"].extend(matches[:3])  # First 3 mentions
    
    if data["found_mentions"]:
        print(f"     ✓ Found {len(data['found_mentions'])} mentions")
    else:
        print(f"     ⚠️ No direct mentions found")
    
    return data

def scrape_afrobasket(team_info):
    """Scrape AfroBasket for team information"""
    print(f"\n  🏀 Searching AfroBasket.com for {team_info['name']}")
    
    base_url = "https://basketball.afrobasket.com"
    search_url = f"{base_url}/Search.asp?search={team_info['name'].replace(' ', '+')}"
    
    html = get_page(search_url)
    if not html:
        return {}
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Save HTML
    filename = f"afrobasket_{team_info['name'].replace(' ', '_').lower()}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"     ✓ Saved search results to: {filename}")
    
    # Look for team links
    team_links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if any(alias.lower() in link.get_text().lower() for alias in team_info["aliases"]):
            full_url = href if href.startswith('http') else base_url + href
            team_links.append({
                "text": link.get_text(strip=True),
                "url": full_url
            })
    
    if team_links:
        print(f"     ✓ Found {len(team_links)} potential team pages")
        for idx, link in enumerate(team_links[:5]):
            print(f"       {idx+1}. {link['text']}: {link['url']}")
    else:
        print(f"     ⚠️ No team pages found")
    
    return {
        "source": "AfroBasket.com",
        "team": team_info["name"],
        "team_links": team_links
    }

def scrape_team_social_media(team_info):
    """Generate social media search queries"""
    print(f"\n  📱 Social Media Sources:")
    
    queries = {
        "twitter": f"{team_info['name']} basketball {team_info['country']}",
        "facebook": f"{team_info['name']} official page",
        "instagram": f"@{team_info['name'].replace(' ', '').lower()}",
        "youtube": f"{team_info['name']} highlights"
    }
    
    for platform, query in queries.items():
        print(f"     {platform.capitalize()}: {query}")
    
    return queries

def extract_player_data(html, team_info):
    """Extract player names and stats from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    
    players = []
    
    # Look for tables with player data
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_text = [cell.get_text(strip=True) for cell in cells]
            
            # Check if row contains team name
            row_str = ' '.join(row_text)
            if any(alias.lower() in row_str.lower() for alias in team_info["aliases"]):
                # Try to identify player names (usually in first column)
                if len(row_text) >= 2:
                    potential_name = row_text[0]
                    # Basic validation: name should have 2+ parts
                    if len(potential_name.split()) >= 2 and not potential_name.isdigit():
                        players.append({
                            "name": potential_name,
                            "data": row_text
                        })
    
    return players

def validate_team_data(data):
    """Validate and clean scraped data"""
    validated = {
        "team": data.get("team", "Unknown"),
        "country": data.get("country", "Unknown"),
        "league": data.get("league", "Unknown"),
        "data_quality": "Unknown",
        "sources_checked": 0,
        "sources_with_data": 0,
        "players_found": 0,
        "stats_available": False,
        "recommendations": []
    }
    
    # Count sources
    if "wikipedia_mentions" in data:
        validated["sources_checked"] += 1
        if data["wikipedia_mentions"]:
            validated["sources_with_data"] += 1
    
    if "afrobasket_links" in data:
        validated["sources_checked"] += 1
        if data["afrobasket_links"]:
            validated["sources_with_data"] += 1
    
    if "players" in data:
        validated["players_found"] = len(data["players"])
        if validated["players_found"] > 0:
            validated["stats_available"] = True
    
    # Determine data quality
    if validated["sources_with_data"] >= 2 and validated["players_found"] >= 5:
        validated["data_quality"] = "Good"
    elif validated["sources_with_data"] >= 1 or validated["players_found"] >= 3:
        validated["data_quality"] = "Fair"
    else:
        validated["data_quality"] = "Poor"
    
    # Generate recommendations
    if validated["data_quality"] == "Poor":
        validated["recommendations"].append("Manual data entry required")
        validated["recommendations"].append(f"Contact {data.get('country')} Basketball Federation")
        validated["recommendations"].append("Check local news sites and sports media")
    
    if validated["players_found"] == 0:
        validated["recommendations"].append("Search for team roster on social media")
        validated["recommendations"].append("Check recent game lineups")
    
    if not validated["stats_available"]:
        validated["recommendations"].append("Manual stat tracking during live games")
        validated["recommendations"].append("Use Elite 16 official stats when available")
    
    return validated

def scrape_team_comprehensive(slug, team_info):
    """Comprehensive scraping for a single team"""
    print(f"\n{'='*70}")
    print(f"SCRAPING: {team_info['name']} ({team_info['country']})")
    print(f"{'='*70}")
    
    all_data = {
        "team": team_info["name"],
        "country": team_info["country"],
        "league": team_info["league"],
        "tier": team_info["tier"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 1. Wikipedia
    wiki_urls = {
        "Namuwongo Blazers": DATA_SOURCES["wikipedia_uganda"],
        "Johannesburg Giants": DATA_SOURCES["wikipedia_sa"],
        "Matero Magic": DATA_SOURCES["wikipedia_zambia"],
        "Dar City": DATA_SOURCES["wikipedia_tanzania"]
    }
    
    if team_info["name"] in wiki_urls:
        wiki_data = scrape_wikipedia_league(team_info, wiki_urls[team_info["name"]])
        all_data["wikipedia_mentions"] = wiki_data.get("found_mentions", [])
        time.sleep(2)
    
    # 2. AfroBasket
    afrobasket_data = scrape_afrobasket(team_info)
    all_data["afrobasket_links"] = afrobasket_data.get("team_links", [])
    time.sleep(2)
    
    # 3. Google News suggestions
    news_search = search_google_news(team_info["name"], team_info["country"])
    all_data["news_search"] = news_search
    
    # 4. Social media sources
    social_queries = scrape_team_social_media(team_info)
    all_data["social_media_queries"] = social_queries
    
    # 5. Validate data
    validation = validate_team_data(all_data)
    all_data["validation"] = validation
    
    return all_data

def main():
    print("\n" + "="*70)
    print("OPEN-SOURCE DATA SCRAPER FOR FIRST-TIME TEAMS")
    print("="*70)
    print("\nTarget Teams:")
    for slug, info in TEAMS.items():
        print(f"  • {info['name']} ({info['country']}) - {info['tier']}")
    
    print("\n" + "="*70)
    print("STARTING COMPREHENSIVE SCRAPING")
    print("="*70)
    
    all_teams_data = []
    
    for slug, team_info in TEAMS.items():
        team_data = scrape_team_comprehensive(slug, team_info)
        all_teams_data.append(team_data)
        
        print(f"\n{'='*70}")
        print(f"VALIDATION RESULTS: {team_info['name']}")
        print(f"{'='*70}")
        validation = team_data["validation"]
        print(f"  Data Quality: {validation['data_quality']}")
        print(f"  Sources Checked: {validation['sources_checked']}")
        print(f"  Sources with Data: {validation['sources_with_data']}")
        print(f"  Players Found: {validation['players_found']}")
        print(f"  Stats Available: {validation['stats_available']}")
        
        if validation["recommendations"]:
            print(f"\n  Recommendations:")
            for rec in validation["recommendations"]:
                print(f"    - {rec}")
        
        time.sleep(3)
    
    # Save summary
    summary_data = []
    for team_data in all_teams_data:
        summary_data.append({
            "Team": team_data["team"],
            "Country": team_data["country"],
            "League": team_data["league"],
            "Tier": team_data["tier"],
            "Data_Quality": team_data["validation"]["data_quality"],
            "Sources_Checked": team_data["validation"]["sources_checked"],
            "Sources_With_Data": team_data["validation"]["sources_with_data"],
            "Players_Found": team_data["validation"]["players_found"],
            "Stats_Available": team_data["validation"]["stats_available"],
            "Wikipedia_Mentions": len(team_data.get("wikipedia_mentions", [])),
            "AfroBasket_Links": len(team_data.get("afrobasket_links", [])),
            "Timestamp": team_data["timestamp"]
        })
    
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv("open_source_teams_data_summary.csv", index=False)
    
    print("\n" + "="*70)
    print("SCRAPING COMPLETE")
    print("="*70)
    print(f"\n✓ Processed {len(all_teams_data)} teams")
    print(f"✓ Summary saved to: open_source_teams_data_summary.csv")
    
    print("\n" + "="*70)
    print("DATA QUALITY SUMMARY")
    print("="*70)
    print(df_summary.to_string(index=False))
    
    print("\n" + "="*70)
    print("NEXT STEPS FOR LIVE COMMENTARY")
    print("="*70)
    print("""
1. MANUAL DATA COLLECTION:
   - Visit team social media pages (Facebook, Twitter, Instagram)
   - Check recent game photos for player names and numbers
   - Search local news sites for roster announcements
   
2. FEDERATION CONTACTS:
   - Uganda Basketball Federation: https://ubf.co.ug
   - Basketball South Africa: https://basketball.org.za
   - Zambia Basketball Federation: Contact via AfroBasket
   - Tanzania Basketball Federation: Contact via AfroBasket
   
3. LIVE GAME TRACKING:
   - Create manual stat sheets for each team
   - Track players during Elite 16 games
   - Note jersey numbers, positions, scoring patterns
   
4. COMMENTARY PREPARATION:
   - Focus on team achievements (domestic titles)
   - Highlight Road to BAL journey
   - Use Elite 16 preliminary stats
   - Reference country basketball context
   
5. LIVE STATS SOURCES:
   - FIBA official live stats (when available)
   - Manual scorekeeping during broadcasts
   - Post-game box scores from FIBA
    """)

if __name__ == "__main__":
    main()
