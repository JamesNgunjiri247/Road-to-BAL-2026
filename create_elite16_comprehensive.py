"""
Create comprehensive Elite 16 performance summary for NCT, Ferroviario Da Beira, and Bravehearts
Combines preliminary group stats with Elite 16 stats
"""

import pandas as pd

print("\n" + "="*70)
print("ELITE 16 COMPREHENSIVE STATS - 3 TEAMS")
print("="*70)

# Load existing data
prelim_df = pd.read_csv("road_to_bal_2026_summary.csv")
games_df = pd.read_csv("elite16_case_study_games_completed.csv")

# Filter for our 3 target teams
target_teams = ["Nairobi City Thunder", "Ferroviario da Beira", "Bravehearts"]

# Create comprehensive stats
comprehensive_stats = []

for team in target_teams:
    # Get preliminary stats
    prelim_stats = prelim_df[prelim_df["Team"] == team].iloc[0] if team in prelim_df["Team"].values else None
    
    # Get Elite 16 games
    team_games = games_df[
        (games_df["Team_A"] == team) | (games_df["Team_B"] == team)
    ]
    
    # Calculate Elite 16 stats
    elite16_wins = 0
    elite16_losses = 0
    elite16_pf = 0
    elite16_pa = 0
    elite16_games_list = []
    
    for _, game in team_games.iterrows():
        if game["Team_A"] == team:
            score_for = game["Score_A"]
            score_against = game["Score_B"]
            opponent = game["Team_B"]
            if game["Winner"] == game["Team_A_Code"]:
                elite16_wins += 1
                result = "W"
            else:
                elite16_losses += 1
                result = "L"
        else:
            score_for = game["Score_B"]
            score_against = game["Score_A"]
            opponent = game["Team_A"]
            if game["Winner"] == game["Team_B_Code"]:
                elite16_wins += 1
                result = "W"
            else:
                elite16_losses += 1
                result = "L"
        
        elite16_pf += score_for
        elite16_pa += score_against
        elite16_games_list.append(f"{result} {score_for}-{score_against} vs {opponent} ({game['Date']})")
    
    # Build comprehensive record
    stats = {
        "Team": team,
        "Tier": prelim_stats["Tier"] if prelim_stats is not None else "N/A",
        "Country": prelim_stats["Country"] if prelim_stats is not None else "N/A",
        
        # Preliminary Round
        "Prelim_Group": prelim_stats["Preliminary_Group"] if prelim_stats is not None else "N/A",
        "Prelim_GP": int(prelim_stats["Games_Played"]) if prelim_stats is not None else 0,
        "Prelim_Wins": int(prelim_stats["Wins"]) if prelim_stats is not None else 0,
        "Prelim_Losses": int(prelim_stats["Losses"]) if prelim_stats is not None else 0,
        "Prelim_PF": int(prelim_stats["Points_For"]) if prelim_stats is not None else 0,
        "Prelim_PA": int(prelim_stats["Points_Against"]) if prelim_stats is not None else 0,
        "Prelim_PD": int(prelim_stats["Point_Diff"]) if prelim_stats is not None else 0,
        "Prelim_PPG": float(prelim_stats["PPG"]) if prelim_stats is not None else 0.0,
        
        # Elite 16
        "Elite16_GP": len(team_games),
        "Elite16_Wins": elite16_wins,
        "Elite16_Losses": elite16_losses,
        "Elite16_PF": elite16_pf,
        "Elite16_PA": elite16_pa,
        "Elite16_PD": elite16_pf - elite16_pa,
        "Elite16_PPG": round(elite16_pf / len(team_games), 1) if len(team_games) > 0 else 0.0,
        "Elite16_OppPPG": round(elite16_pa / len(team_games), 1) if len(team_games) > 0 else 0.0,
        
        # Combined Total
        "Total_GP": (int(prelim_stats["Games_Played"]) if prelim_stats is not None else 0) + len(team_games),
        "Total_Wins": (int(prelim_stats["Wins"]) if prelim_stats is not None else 0) + elite16_wins,
        "Total_Losses": (int(prelim_stats["Losses"]) if prelim_stats is not None else 0) + elite16_losses,
        "Total_PF": (int(prelim_stats["Points_For"]) if prelim_stats is not None else 0) + elite16_pf,
        "Total_PA": (int(prelim_stats["Points_Against"]) if prelim_stats is not None else 0) + elite16_pa,
        
        "Elite16_Games": " | ".join(elite16_games_list) if elite16_games_list else "No games yet"
    }
    
    # Calculate totals
    if stats["Total_GP"] > 0:
        stats["Total_PD"] = stats["Total_PF"] - stats["Total_PA"]
        stats["Total_PPG"] = round(stats["Total_PF"] / stats["Total_GP"], 1)
        stats["Total_Win_Pct"] = round(stats["Total_Wins"] / stats["Total_GP"], 3)
    else:
        stats["Total_PD"] = 0
        stats["Total_PPG"] = 0.0
        stats["Total_Win_Pct"] = 0.000
    
    comprehensive_stats.append(stats)

# Create DataFrame
df = pd.DataFrame(comprehensive_stats)

# Save to CSV
df.to_csv("elite16_comprehensive_nct_fbe_bhb.csv", index=False)

print(f"\n✓ Created comprehensive stats for {len(df)} teams\n")
print(df[["Team", "Tier", "Prelim_GP", "Prelim_Wins", "Elite16_GP", "Elite16_Wins", "Total_GP", "Total_Wins", "Total_PPG"]].to_string(index=False))

print("\n" + "="*70)
print("DETAILED BREAKDOWN")
print("="*70)

for _, row in df.iterrows():
    print(f"\n{row['Team']} ({row['Tier']}) - {row['Country']}")
    print("-" * 60)
    print(f"PRELIMINARY ROUND ({row['Prelim_Group']}):")
    print(f"  Record: {row['Prelim_Wins']}-{row['Prelim_Losses']} in {row['Prelim_GP']} games")
    print(f"  Scoring: {row['Prelim_PPG']} PPG | {row['Prelim_PD']:+d} PD")
    
    print(f"\nELITE 16:")
    print(f"  Record: {row['Elite16_Wins']}-{row['Elite16_Losses']} in {row['Elite16_GP']} games")
    if row['Elite16_GP'] > 0:
        print(f"  Scoring: {row['Elite16_PPG']} PPG | {row['Elite16_PD']:+d} PD")
        print(f"  Games: {row['Elite16_Games']}")
    else:
        print(f"  Status: Games not yet started")
    
    print(f"\nTOTAL ROAD TO BAL 2026:")
    print(f"  Overall Record: {row['Total_Wins']}-{row['Total_Losses']} ({row['Total_Win_Pct']:.1%})")
    print(f"  Total Games: {row['Total_GP']}")
    print(f"  Average: {row['Total_PPG']} PPG | {row['Total_PD']:+d} PD")

print("\n" + "="*70)
print("✅ COMPREHENSIVE STATS SAVED: elite16_comprehensive_nct_fbe_bhb.csv")
print("="*70)
