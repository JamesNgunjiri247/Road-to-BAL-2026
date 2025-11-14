"""
Clean and parse NCT 2025 BAL stats from messy scraped data
"""

import pandas as pd
import re

# Read the messy data
df = pd.read_csv('nct_2025_bal_stats.csv')

# Extract team summary stats (the clean ones)
team_stats_data = []
for _, row in df.iterrows():
    data = row['data']
    if isinstance(data, str):
        # Team summary stats
        if 'Points per game |' in data:
            team_stats_data.append({'Metric': 'Points per game', 'Value': data.split('|')[1].strip()})
        elif '2FGP% |' in data:
            team_stats_data.append({'Metric': '2FG%', 'Value': data.split('|')[1].strip()})
        elif '3FGP% |' in data:
            team_stats_data.append({'Metric': '3FG%', 'Value': data.split('|')[1].strip()})
        elif 'FT% |' in data:
            team_stats_data.append({'Metric': 'FT%', 'Value': data.split('|')[1].strip()})
        elif 'Off rebounds |' in data:
            team_stats_data.append({'Metric': 'Offensive Rebounds', 'Value': data.split('|')[1].strip()})
        elif 'Def rebounds |' in data:
            team_stats_data.append({'Metric': 'Defensive Rebounds', 'Value': data.split('|')[1].strip()})
        elif 'Total rebounds |' in data:
            team_stats_data.append({'Metric': 'Total Rebounds', 'Value': data.split('|')[1].strip()})
        elif 'Assists per game |' in data:
            team_stats_data.append({'Metric': 'Assists per game', 'Value': data.split('|')[1].strip()})
        elif 'Turnovers per game |' in data:
            team_stats_data.append({'Metric': 'Turnovers per game', 'Value': data.split('|')[1].strip()})
        elif 'Steals per game |' in data:
            team_stats_data.append({'Metric': 'Steals per game', 'Value': data.split('|')[1].strip()})
        elif 'Blocks per game |' in data:
            team_stats_data.append({'Metric': 'Blocks per game', 'Value': data.split('|')[1].strip()})
        elif 'Points per game of opponent |' in data:
            team_stats_data.append({'Metric': 'Opponent Points per game', 'Value': data.split('|')[1].strip()})
        elif 'Opponent 2FGP% |' in data:
            team_stats_data.append({'Metric': 'Opponent 2FG%', 'Value': data.split('|')[1].strip()})
        elif 'Opponent 3FGP% |' in data:
            team_stats_data.append({'Metric': 'Opponent 3FG%', 'Value': data.split('|')[1].strip()})

# Extract player stats (the pipe-separated ones)
player_stats = []
for _, row in df.iterrows():
    data = row['data']
    if isinstance(data, str) and ' | ' in data:
        parts = data.split(' | ')
        # Look for player stat rows (they have jersey number at start)
        if len(parts) >= 18:
            try:
                # Check if first element is a number (jersey number)
                jersey_num = parts[0].strip()
                if jersey_num.isdigit():
                    player_stats.append({
                        'Jersey': jersey_num,
                        'Name': parts[1].strip(),
                        'Games': parts[2].strip(),
                        'MIN': parts[3].strip(),
                        'FGM-A': parts[4].strip(),
                        'FG%': parts[5].strip(),
                        '3PM-A': parts[6].strip(),
                        '3P%': parts[7].strip(),
                        'FTM-A': parts[8].strip(),
                        'FT%': parts[9].strip(),
                        'ORB': parts[10].strip(),
                        'DRB': parts[11].strip(),
                        'REB': parts[12].strip(),
                        'AST': parts[13].strip(),
                        'PF': parts[14].strip(),
                        'STL': parts[15].strip(),
                        'BLK': parts[16].strip(),
                        'TO': parts[17].strip(),
                        'PTS': parts[18].strip(),
                        'RNK': parts[19].strip() if len(parts) > 19 else ''
                    })
            except:
                pass

# Extract game record
game_record = {}
for _, row in df.iterrows():
    data = row['data']
    if isinstance(data, str) and 'Basketball Africa League | 6 |' in data:
        parts = data.split(' | ')
        if len(parts) >= 6:
            game_record = {
                'Competition': parts[0].strip(),
                'Total Games': parts[1].strip(),
                'Home Won': parts[2].strip(),
                'Home Lost': parts[3].strip(),
                'Away Won': parts[4].strip(),
                'Away Lost': parts[5].strip()
            }

# Create clean DataFrames
print("="*70)
print("NCT 2025 BAL SEASON - CLEANED DATA")
print("="*70)

# 1. Team Summary Stats
if team_stats_data:
    df_team = pd.DataFrame(team_stats_data)
    df_team.to_csv('nct_2025_team_stats_clean.csv', index=False)
    print("\n1. TEAM SUMMARY STATS")
    print("-"*70)
    print(df_team.to_string(index=False))
    print(f"\n✓ Saved: nct_2025_team_stats_clean.csv")

# 2. Game Record
if game_record:
    df_record = pd.DataFrame([game_record])
    df_record.to_csv('nct_2025_game_record_clean.csv', index=False)
    print("\n2. GAME RECORD (2025 BAL)")
    print("-"*70)
    print(df_record.to_string(index=False))
    print(f"\n✓ Saved: nct_2025_game_record_clean.csv")

# 3. Player Stats
if player_stats:
    df_players = pd.DataFrame(player_stats)
    df_players.to_csv('nct_2025_player_stats_clean.csv', index=False)
    print("\n3. PLAYER STATS")
    print("-"*70)
    print(df_players.to_string(index=False))
    print(f"\n✓ Saved: nct_2025_player_stats_clean.csv")

# 4. Create a comprehensive summary sheet
print("\n" + "="*70)
print("CREATING COMPREHENSIVE SUMMARY")
print("="*70)

# Key metrics for comparison
key_metrics = {
    'Team': 'Nairobi City Thunder',
    'Season': '2025 BAL',
    'Games Played': '6',
    'Record': '1-5',
    'PPG': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Points per game'), 'N/A'),
    'Opp PPG': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Opponent Points per game'), 'N/A'),
    'FG%': next((item['Value'] for item in team_stats_data if item['Metric'] == '2FG%'), 'N/A'),
    '3P%': next((item['Value'] for item in team_stats_data if item['Metric'] == '3FG%'), 'N/A'),
    'FT%': next((item['Value'] for item in team_stats_data if item['Metric'] == 'FT%'), 'N/A'),
    'RPG': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Total Rebounds'), 'N/A'),
    'APG': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Assists per game'), 'N/A'),
    'SPG': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Steals per game'), 'N/A'),
    'BPG': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Blocks per game'), 'N/A'),
    'TOV': next((item['Value'] for item in team_stats_data if item['Metric'] == 'Turnovers per game'), 'N/A'),
}

df_summary = pd.DataFrame([key_metrics])
df_summary.to_csv('nct_2025_summary_clean.csv', index=False)
print("\n✓ Saved: nct_2025_summary_clean.csv")
print("\nKEY METRICS:")
for key, value in key_metrics.items():
    print(f"  {key}: {value}")

# Top 3 scorers
if player_stats:
    print("\nTOP 3 SCORERS:")
    top_scorers = sorted(player_stats, key=lambda x: float(x['PTS']), reverse=True)[:3]
    for i, player in enumerate(top_scorers, 1):
        print(f"  {i}. {player['Name']}: {player['PTS']} PPG")

print("\n" + "="*70)
print("DATA CLEANING COMPLETE!")
print("="*70)
print("\nFiles created:")
print("  1. nct_2025_team_stats_clean.csv")
print("  2. nct_2025_game_record_clean.csv")
print("  3. nct_2025_player_stats_clean.csv")
print("  4. nct_2025_summary_clean.csv")
print("\nReady to upload to Google Sheets!")
