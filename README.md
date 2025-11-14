# Road to BAL 2026 - Data Scraping & Analysis Project

## Project Overview
Comprehensive data collection and analysis for 7 teams competing in the Basketball Africa League (BAL) Road to BAL 2026 Elite 16 tournament.

---

## Case Study Teams

### Group A (The "Group of Death")
1. **Nairobi City Thunder (NCT)** - Tier 1 (BAL Vet)
   - The Hosts - 2025 BAL debutants
   - Baseline team for case study

2. **Namuwongo Blazers** - Tier 2 (New Guard)
   - The Kingslayers - First Ugandan NBL title
   - Dethroned 10x defending champions

3. **Johannesburg Giants** - Tier 2 (New Guard)
   - The Undefeated - Perfect 5-0 in qualifiers
   - Group E winners

### Group B (The Juggernaut vs. The Challengers)
4. **Ferroviario Da Beira** - Tier 1 (BAL Vet)
   - The Juggernaut - 2x BAL main tournament participant (2022, 2023)
   - Clear favorites

5. **Matero Magic** - Tier 2
   - The Road Warriors - Zambian champions
   - Need to close gap vs. elite teams

6. **Dar City** - Tier 3 (Dark Horse)
   - Star-Powered Unknown
   - Features former BAL champion Solo Diabate

7. **Bravehearts** - Tier 3
   - The Underdogs - 5x Malawian champions
   - Previous Elite 16 struggles

---

## ✅ COMPLETED TASKS

### 1. Environment Setup
- ✅ Python virtual environment configured (Python 3.13.7)
- ✅ Dependencies installed: requests, beautifulsoup4, pandas, gspread, google-auth
- ✅ Google Cloud credentials configured
- ✅ Google Sheets API access established

### 2. Data Collection Scripts Created
- ✅ `fiba_teams_scraper.py` - Scrapes all 23 Road to BAL teams
- ✅ `scrape_wikipedia_bal.py` - Extracts qualification data from Wikipedia
- ✅ `scrape_from_specified_sites.py` - Comprehensive scraper for 5 data sources
- ✅ `clean_nct_stats.py` - Parses and cleans NCT 2025 BAL stats
- ✅ `create_team_profiles.py` - Generates comprehensive team profiles
- ✅ `upload_all_data.py` - Uploads all data to Google Sheets

### 3. Data Successfully Scraped

#### A. All Teams Data
- ✅ **teams_roster_links.csv** (23 teams)
  - Team names, codes, profile URLs, team slugs

#### B. Case Study Teams
- ✅ **comprehensive_team_profiles.csv** (7 teams)
  - Tier classifications
  - BAL history
  - Narratives and storylines
  - Strengths/weaknesses
  - Key players
  - H2H notes

#### C. Qualification Data
- ✅ **bal_2026_qualification_data.csv** (16 records)
  - W-L records from preliminary groups
  - Points For (PF), Points Against (PA), Point Differential (PD)
  - Qualification methods
  - Advancement status

#### D. Head-to-Head Results
- ✅ **head_to_head_results.csv** (3 matchups)
  - Giants vs Matero Magic (84-62, +22)
  - Beira vs Matero Magic (94-83, +11)
  - NCT vs Bravehearts (91-68, +23)

#### E. Nairobi City Thunder Complete Stats
- ✅ **nct_2025_summary_clean.csv**
  - Key metrics: 79.0 PPG, 89.8 Opp PPG, Net Rating -13.3
  - Record: 1-5 (6 games)
  
- ✅ **nct_2025_team_stats_clean.csv**
  - Shooting: 46.6% 2FG, 28.2% 3FG, 58.2% FT
  - Rebounds: 39.7 RPG (13.8 ORB, 25.8 DRB)
  - Assists: 18.7 APG
  - Defense: 7.8 SPG, 3.2 BPG
  - Turnovers: 14.2 TOV
  
- ✅ **nct_2025_player_stats_clean.csv** (12 players)
  - Top scorers: Iroegbu (14.0 PPG), Odero (14.0 PPG), Ongwae (11.5 PPG)
  - Full stats: G, MIN, FG%, 3P%, FT%, REB, AST, STL, BLK, TO, PTS
  
- ✅ **nct_2025_game_record_clean.csv**
  - Home: 0-3, Away: 1-2

#### F. Multi-Source Scraped Data
- ✅ **case_study_teams_comprehensive_data.csv**
  - Data from Road to BAL 2025
  - Data from FIBA History
  - Limited data from BAL.NBA.com (most teams not in BAL yet)
  - Note: Only NCT has significant data (8 records)

- ✅ **scraping_summary_by_team.csv**
  - Tracking of data collected per source per team

### 4. Google Sheets Integration
- ✅ Spreadsheet: "FIBA Teams Road to BAL 2026"
- ✅ URL: https://docs.google.com/spreadsheets/d/1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU
- ✅ Service account: sheets-uploader@fiba-data-upload.iam.gserviceaccount.com

#### Worksheets Created:
1. ✅ Team Profiles (All 7 Teams)
2. ✅ Head-to-Head Results
3. ✅ Scraped Data (All Sources)
4. ✅ Scraping Summary
5. ✅ BAL 2026 Qualification Data
6. ✅ All Teams Roster Links
7. ✅ NCT 2025 Summary
8. ✅ NCT 2025 Team Stats
9. ✅ NCT 2025 Player Stats
10. ✅ NCT 2025 Game Record

---

## ⚠️ INCOMPLETE / MISSING DATA

### 1. Limited Historical BAL Data for Other Teams

**Ferroviario Da Beira (Tier 1 - Critical)**
- ❌ 2022 BAL season statistics
- ❌ 2023 BAL season statistics
- ❌ Player stats (Will Perry, Jermel Kennedy, Ayad Munguambe)
- ❌ Team averages (PPG, RPG, APG, ORtg, DRtg)
- 📍 Known sources:
  - https://www.fiba.basketball/en/history/109-basketball-africa-league/208481/teams/ferroviario-da-beira
  - Basketball24.com for historical data

**Other 5 Teams (Tier 2-3)**
- ❌ No detailed player statistics
- ❌ No team shooting percentages
- ❌ No individual game stats
- 📍 Why: These teams have not participated in main BAL tournament yet

### 2. Road to BAL 2026 Current Data (Elite 16)

**Missing for ALL 7 Teams:**
- ❌ Elite 16 games schedule (Group A & B)
- ❌ Live game results and box scores
- ❌ Updated standings
- ❌ Player leaderboards (PPG, RPG, APG leaders)
- ❌ Team statistics from Elite 16 rounds

**Known Issues:**
- FIBA website uses JavaScript/React - data loads dynamically
- Static HTML scrapers cannot access this data
- Would need browser automation (Selenium/Playwright) or API access

### 3. Detailed Qualifier Data

**Group D (Namuwongo Blazers, Dar City)**
- ❌ Game-by-game results
- ❌ Player statistics
- ❌ Team shooting percentages

**Group E (Giants, Beira, Matero, Bravehearts)**
- ✅ Have: W-L records, PF, PA, PD
- ❌ Missing: Individual game box scores
- ❌ Missing: Player leaders
- ❌ Missing: Advanced metrics

### 4. Player Comparison Data

**Across All 7 Teams:**
- ❌ Top scorers ranking
- ❌ Top rebounders ranking
- ❌ Top assist leaders
- ❌ Shooting efficiency comparison
- ❌ Defensive stats comparison

### 5. Advanced Analytics

**For All Teams Except NCT:**
- ❌ Offensive Rating (ORtg)
- ❌ Defensive Rating (DRtg)
- ❌ Net Rating
- ❌ Pace
- ❌ Four Factors (eFG%, TOV%, ORB%, FT Rate)
- ❌ Usage rates
- ❌ Plus/Minus data

---

## 📋 TO-DO LIST (Priority Order)

### HIGH PRIORITY

1. **⭐ Ferroviario Da Beira Historical Data**
   - Target: 2023 BAL season (most recent)
   - Data needed: Team stats, top 3 players, W-L record
   - Importance: Only other Tier 1 team (NCT baseline comparison)
   - Manual option: Review Basketball24.com BAL 2023 archives

2. **⭐ Road to BAL 2026 Elite 16 Live Data**
   - Option A: Manual data entry from FIBA live stats
   - Option B: Browser automation (Selenium)
   - Option C: Wait for post-tournament static data
   - Critical for: Current tournament analysis

3. **⭐ Create Comparison Matrix**
   - NCT vs. Beira (Tier 1 comparison)
   - Group A competitive landscape
   - Group B competitive landscape
   - Manual data aggregation from existing sources

### MEDIUM PRIORITY

4. **Group E Detailed Stats**
   - Giants (5-0), Beira (4-1), Matero (3-2), Bravehearts (2-3)
   - Game-by-game breakdowns
   - Key player identification

5. **Player Profiles for Star Players**
   - Solo Diabate (Dar City) - former BAL champion
   - Raphiael Putney (Dar City) - high scorer
   - Top performers from Giants' 5-0 run
   - Namuwongo Blazers' key players

6. **Head-to-Head Analysis**
   - Expand beyond 3 documented games
   - Historical matchups from previous qualifiers
   - Identify trends and patterns

### LOW PRIORITY

7. **Additional Teams Context**
   - Domestic league statistics
   - International tournament history
   - Roster changes from previous seasons

8. **Visual Data Prep**
   - Format data for graphics package
   - Create stat cards templates
   - Prepare pre-game comparison sheets

---

## 🛠️ TECHNICAL NOTES

### Data Source Status

**✅ Working Sources:**
- Wikipedia (static HTML) - Excellent for standings/records
- Afrobasket.com - Good for BAL historical data (when team ID known)
- FIBA team profile pages (static content)

**⚠️ Partially Working:**
- FIBA History pages - Limited data availability
- BAL.NBA.com - Only teams with BAL history
- Basketball24.com - Archive data available but requires manual extraction

**❌ Not Working:**
- FIBA live stats/games pages (JavaScript-based)
- Road to BAL 2026 current games (dynamic loading)
- Real-time leaderboards (API required)

### Scraping Limitations
- JavaScript-rendered content not accessible with BeautifulSoup
- Rate limiting required (2-3 second delays)
- Team name variations cause matching issues
- Some teams have no prior BAL data (debut teams)

### Alternatives
1. **Manual Data Entry** - For critical Beira 2023 BAL data
2. **Browser Automation** - For current Elite 16 live data
3. **Official APIs** - If FIBA provides access
4. **Post-Tournament Data** - Wait for static archives

---

## 📊 DATA QUALITY ASSESSMENT

### Excellent (100% Complete)
- ✅ Nairobi City Thunder (Baseline team)
- ✅ Team profiles and narratives
- ✅ Qualification standings
- ✅ H2H documented games

### Good (50-75% Complete)
- ⚠️ Johannesburg Giants (group record, missing player data)
- ⚠️ Matero Magic (group record, missing player data)
- ⚠️ Bravehearts (group record, missing player data)

### Fair (25-50% Complete)
- ⚠️ Ferroviario Da Beira (BAL history known, stats missing)
- ⚠️ Namuwongo Blazers (profile complete, stats missing)

### Poor (<25% Complete)
- ⚠️ Dar City (profile only, no stats)

---

## 🎯 IMMEDIATE NEXT STEPS

1. **Review uploaded Google Sheets data**
   - Verify all worksheets loaded correctly
   - Check data formatting
   - Identify any upload errors

2. **Manual Beira data collection**
   - Search Basketball24.com for 2023 BAL
   - Extract key stats for comparison with NCT
   - Create beira_2023_bal_stats.csv

3. **Monitor Elite 16 tournament**
   - Track live results manually
   - Record game scores
   - Note standout performances

4. **Prepare analysis framework**
   - Define key comparison metrics
   - Create baseline benchmarks (NCT = reference)
   - Design tier-based analysis approach

---

## 📁 FILE STRUCTURE

```
ROAD TO BAL/
├── credentials.json (Google API)
├── .venv/ (Python virtual environment)
│
├── SCRAPERS:
│   ├── fiba_teams_scraper.py
│   ├── scrape_wikipedia_bal.py
│   ├── scrape_from_specified_sites.py
│   ├── clean_nct_stats.py
│   └── create_team_profiles.py
│
├── DATA (CSV):
│   ├── teams_roster_links.csv (23 teams)
│   ├── comprehensive_team_profiles.csv (7 teams)
│   ├── bal_2026_qualification_data.csv
│   ├── head_to_head_results.csv
│   ├── nct_2025_summary_clean.csv
│   ├── nct_2025_team_stats_clean.csv
│   ├── nct_2025_player_stats_clean.csv
│   ├── nct_2025_game_record_clean.csv
│   ├── case_study_teams_comprehensive_data.csv
│   └── scraping_summary_by_team.csv
│
├── UTILITIES:
│   ├── upload_all_data.py
│   └── upload_to_sheets.py
│
└── DOCUMENTATION:
    ├── README.md (this file)
    └── GOOGLE_SHEETS_SETUP.md
```

---

## 🔗 KEY LINKS

### Google Sheets
- Main Spreadsheet: https://docs.google.com/spreadsheets/d/1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU

### Data Sources
- Road to BAL 2025: https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2025
- Road to BAL 2026: https://www.fiba.basketball/en/events/fiba-africa-champions-clubs-road-to-bal-2026
- FIBA History: https://www.fiba.basketball/en/history/104-africa-champions-clubs-road-to-bal/208719
- BAL Teams: https://bal.nba.com/teams
- BAL Stats: https://bal.nba.com/statistics
- Basketball24: https://www.basketball24.com/africa/bal-2022/
- NCT 2025 BAL Stats: https://basketball.afrobasket.com/team/Nairobi-City-Thunder/17638/Stats
- Beira History: https://www.fiba.basketball/en/history/109-basketball-africa-league/208481/teams/ferroviario-da-beira
- Wikipedia Qualification: https://en.wikipedia.org/wiki/2026_BAL_qualification

---

## 📝 NOTES

### Key Insights from Data
1. **NCT Baseline**: 79.0 PPG, -10.8 net rating establishes benchmark
2. **Giants Dominance**: Perfect 5-0 with +82 point differential
3. **Beira Experience**: 2x BAL participant = clear Group B favorite
4. **Matero Challenge**: Good stats (+103 PD) but loses to top teams by 11-22 pts
5. **Tier System**: Clear separation between BAL vets, strong challengers, and underdogs

### Technical Achievements
- Successfully scraped and cleaned messy HTML data
- Automated Google Sheets upload with formatting
- Created reusable scraping framework
- Handled NaN values and data inconsistencies
- Built comprehensive team profile system

### Lessons Learned
- Dynamic JavaScript sites require different approach
- Wikipedia excellent for structured tournament data
- Team name variations complicate matching
- Historical BAL data limited for most African teams
- Manual data collection necessary for some sources

---

**Last Updated:** November 14, 2025  
**Project Status:** Data Collection Phase - 60% Complete  
**Next Milestone:** Ferroviario Da Beira historical data collection
