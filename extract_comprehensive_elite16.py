import json
import re
import pandas as pd
from datetime import datetime

def extract_games_from_json(file_path='standings_script_105.js'):
    """Extract all game data from the JavaScript file"""
    
    print("Reading JavaScript file...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the games array - it's embedded in the JSON structure
    # Pattern: "games":[{game objects}]
    games_match = re.search(r'"games":\[(.*?)\],"children"', content, re.DOTALL)
    
    if not games_match:
        print("Could not find games array")
        return None
    
    games_json_str = '[' + games_match.group(1) + ']'
    
    # Fix escaped quotes and parse
    try:
        games_json_str = games_json_str.replace('\\"', '"').replace('\\\\', '\\')
        
        # Manual parsing since it's complex nested structure
        # Extract individual game objects
        game_pattern = r'\{\"gameId\":(\d+),.*?\"teamA\":\{.*?\"code\":\"([A-Z]+)\",\"officialName\":\"([^\"]+)\".*?\},\"teamB\":\{.*?\"code\":\"([A-Z]+)\",\"officialName\":\"([^\"]+)\".*?\},\"teamAScore\":(\d+),\"teamBScore\":(\d+).*?\"groupPairingCode\":\"([A-Z]?)\".*?\"gameDateTime\":\"([^\"]+)\"'
        
        games = re.findall(game_pattern, content)
        
        print(f"\n✓ Found {len(games)} games")
        
        all_games = []
        for game in games:
            game_id, teamA_code, teamA_name, teamB_code, teamB_name, scoreA, scoreB, group, date = game
            
            all_games.append({
                'Game_ID': game_id,
                'Group': group if group else 'N/A',
                'Date': date[:10] if date != '0001-01-01T00:00:00' else 'TBD',
                'Team_A_Code': teamA_code,
                'Team_A': teamA_name,
                'Score_A': int(scoreA),
                'Team_B_Code': teamB_code,
                'Team_B': teamB_name,
                'Score_B': int(scoreB),
                'Winner': teamA_code if int(scoreA) > int(scoreB) else teamB_code if int(scoreB) > int(scoreA) else 'Draw'
            })
        
        return pd.DataFrame(all_games)
        
    except Exception as e:
        print(f"Error parsing: {e}")
        return None

def calculate_standings(games_df, case_study_teams):
    """Calculate standings from games data"""
    
    # Filter only completed games (not 0-0)
    completed = games_df[(games_df['Score_A'] > 0) | (games_df['Score_B'] > 0)].copy()
    
    standings = {}
    
    # Initialize all teams
    all_teams = set(completed['Team_A_Code'].unique()) | set(completed['Team_B_Code'].unique())
    
    for team in all_teams:
        # Find team's group
        team_games = completed[(completed['Team_A_Code'] == team) | (completed['Team_B_Code'] == team)]
        if not team_games.empty:
            group = team_games.iloc[0]['Group']
            
            standings[team] = {
                'Group': group,
                'GP': 0,
                'W': 0,
                'L': 0,
                'PF': 0,
                'PA': 0,
                'PD': 0,
                'PTS': 0
            }
    
    # Calculate stats from games
    for _, game in completed.iterrows():
        teamA = game['Team_A_Code']
        teamB = game['Team_B_Code']
        scoreA = game['Score_A']
        scoreB = game['Score_B']
        
        if teamA in standings:
            standings[teamA]['GP'] += 1
            standings[teamA]['PF'] += scoreA
            standings[teamA]['PA'] += scoreB
            if scoreA > scoreB:
                standings[teamA]['W'] += 1
                standings[teamA]['PTS'] += 2
            else:
                standings[teamA]['L'] += 1
                standings[teamA]['PTS'] += 1
        
        if teamB in standings:
            standings[teamB]['GP'] += 1
            standings[teamB]['PF'] += scoreB
            standings[teamB]['PA'] += scoreA
            if scoreB > scoreA:
                standings[teamB]['W'] += 1
                standings[teamB]['PTS'] += 2
            else:
                standings[teamB]['L'] += 1
                standings[teamB]['PTS'] += 1
    
    # Calculate point differential
    for team in standings:
        standings[team]['PD'] = standings[team]['PF'] - standings[team]['PA']
    
    # Convert to DataFrame
    standings_df = pd.DataFrame.from_dict(standings, orient='index')
    standings_df['Team_Code'] = standings_df.index
    standings_df = standings_df.reset_index(drop=True)
    
    # Sort by Group, PTS, PD
    standings_df = standings_df.sort_values(['Group', 'PTS', 'PD'], ascending=[True, False, False])
    
    # Add rank within group
    standings_df['Rank'] = standings_df.groupby('Group').cumcount() + 1
    
    # Reorder columns
    standings_df = standings_df[['Group', 'Rank', 'Team_Code', 'GP', 'W', 'L', 'PF', 'PA', 'PD', 'PTS']]
    
    # Filter case study teams
    case_study_df = standings_df[standings_df['Team_Code'].isin(case_study_teams)].copy()
    
    # Add full names
    team_names = {
        'NCT': 'Nairobi City Thunder',
        'NAM': 'Namuwongo Blazers',
        'JOH': 'Johannesburg Giants',
        'FBE': 'Ferroviario da Beira',
        'MMA': 'Matero Magic',
        'DAR': 'Dar City',
        'BHB': 'Bravehearts'
    }
    
    case_study_df['Team_Name'] = case_study_df['Team_Code'].map(team_names)
    
    return standings_df, case_study_df

def extract_case_study_games(games_df, case_study_teams):
    """Extract all games involving case study teams"""
    
    case_study_games = games_df[
        (games_df['Team_A_Code'].isin(case_study_teams)) |
        (games_df['Team_B_Code'].isin(case_study_teams))
    ].copy()
    
    # Add match type
    def classify_match(row):
        teamA_in = row['Team_A_Code'] in case_study_teams
        teamB_in = row['Team_B_Code'] in case_study_teams
        
        if teamA_in and teamB_in:
            return 'Head-to-Head'
        else:
            return 'vs Other'
    
    case_study_games['Match_Type'] = case_study_games.apply(classify_match, axis=1)
    
    # Filter only completed games
    completed_games = case_study_games[(case_study_games['Score_A'] > 0) | (case_study_games['Score_B'] > 0)]
    
    return completed_games

def main():
    print("=" * 80)
    print("COMPREHENSIVE ELITE 16 DATA EXTRACTION")
    print("=" * 80)
    
    # Case study teams
    case_study_teams = ['NCT', 'NAM', 'JOH', 'FBE', 'MMA', 'DAR', 'BHB']
    
    # Extract all games
    games_df = extract_games_from_json()
    
    if games_df is None:
        print("Failed to extract games data")
        return
    
    print(f"\n✓ Total games extracted: {len(games_df)}")
    
    # Save all games
    games_df.to_csv('elite16_all_games.csv', index=False)
    print(f"✓ Saved to elite16_all_games.csv")
    
    # Calculate standings
    print("\n\nCalculating standings...")
    all_standings, case_study_standings = calculate_standings(games_df, case_study_teams)
    
    print("\n" + "=" * 80)
    print("ALL STANDINGS (FROM COMPLETED GAMES)")
    print("=" * 80)
    print(all_standings.to_string(index=False))
    
    all_standings.to_csv('elite16_calculated_standings.csv', index=False)
    print(f"\n✓ Saved to elite16_calculated_standings.csv")
    
    print("\n" + "=" * 80)
    print("CASE STUDY TEAMS STANDINGS")
    print("=" * 80)
    print(case_study_standings.to_string(index=False))
    
    case_study_standings.to_csv('elite16_case_study_standings.csv', index=False)
    print(f"\n✓ Saved to elite16_case_study_standings.csv")
    
    # Extract case study games
    print("\n\nExtracting case study team games...")
    case_study_games = extract_case_study_games(games_df, case_study_teams)
    
    print("\n" + "=" * 80)
    print("CASE STUDY TEAM GAMES (COMPLETED)")
    print("=" * 80)
    print(case_study_games[['Date', 'Group', 'Team_A_Code', 'Score_A', 'Team_B_Code', 'Score_B', 'Match_Type']].to_string(index=False))
    
    case_study_games.to_csv('elite16_case_study_games.csv', index=False)
    print(f"\n✓ Saved to elite16_case_study_games.csv")
    
    # Summary stats
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    for team in case_study_teams:
        team_data = case_study_standings[case_study_standings['Team_Code'] == team]
        if not team_data.empty:
            row = team_data.iloc[0]
            print(f"\n{team} ({row['Team_Name']}):")
            print(f"  Group {row['Group']} - Rank #{int(row['Rank'])}")
            print(f"  Record: {int(row['W'])}-{int(row['L'])} ({int(row['GP'])} games)")
            print(f"  Scoring: {int(row['PF'])} PF, {int(row['PA'])} PA, {int(row['PD']):+d} PD")
            print(f"  Points: {int(row['PTS'])}")
    
    print("\n" + "=" * 80)
    print("✓ EXTRACTION COMPLETE")
    print("=" * 80)
    print("\nFiles created:")
    print("1. elite16_all_games.csv - All games from all groups")
    print("2. elite16_calculated_standings.csv - Standings for all teams")
    print("3. elite16_case_study_standings.csv - Standings for 7 case study teams")
    print("4. elite16_case_study_games.csv - All games involving case study teams")

if __name__ == "__main__":
    main()
