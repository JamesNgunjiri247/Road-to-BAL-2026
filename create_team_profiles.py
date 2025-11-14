"""
Create comprehensive team profiles using existing Wikipedia data 
plus targeted scraping for teams with confirmed BAL history
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Read existing qualification data
print("="*70)
print("CREATING COMPREHENSIVE TEAM PROFILES")
print("="*70)

# Load the qualification data we already have
qual_data = pd.read_csv("bal_2026_qualification_data.csv")

print(f"\n✓ Loaded {len(qual_data)} qualification records")

# Define comprehensive team profiles
TEAM_PROFILES = {
    "Nairobi City Thunder": {
        "tier": "Tier 1 (BAL Vet)",
        "group": "Group A",
        "narrative": "The Hosts - 2025 BAL debutants",
        "country": "Kenya",
        "bal_history": "2025 BAL (1-5 record, 79.0 PPG, 89.8 Opp PPG)",
        "qualifier_2026": "Elite 16 - Group A",
        "key_stats": "ORtg: 97.0, DRtg: 110.3, Net: -13.3",
        "top_players": "Iroegbu (14.0 PPG), Odero (14.0 PPG), Ongwae (11.5 PPG)",
        "strengths": "Rebounding (39.7 RPG), Assists (18.7 APG)",
        "weaknesses": "3PT% (28.2%), FT% (58.2%), Defense (89.8 Opp PPG)",
        "storyline": "Baseline team for case study - first BAL appearance"
    },
    
    "Namuwongo Blazers": {
        "tier": "Tier 2 (New Guard)",
        "group": "Group A",
        "narrative": "The Kingslayers - First Ugandan NBL title",
        "country": "Uganda",
        "bal_history": "None - Road to BAL debut",
        "qualifier_2026": "Elite 16 - Group A (advanced from Group D)",
        "domestic_success": "2025 NBL Uganda champions (dethroned 10x champ City Oilers)",
        "h2h_notes": "Group D qualifier: 1-1 record",
        "storyline": "Biggest upset story - beat decade-long dynasty"
    },
    
    "Johannesburg Giants": {
        "tier": "Tier 2 (New Guard)",
        "group": "Group A",
        "narrative": "The Undefeated - Perfect 5-0 in qualifiers",
        "country": "South Africa",
        "bal_history": "None - Road to BAL debut",
        "qualifier_2026": "Elite 16 - Group A (5-0 in Group E)",
        "group_e_stats": "W: 5, L: 0, PF: 362, PA: 280, PD: +82",
        "h2h_results": "Beat Matero Magic 84-62 (Nov 1)",
        "strengths": "Perfect record, strong point differential (+82)",
        "storyline": "Dominant qualifiers - only undefeated team"
    },
    
    "Ferroviario Da Beira": {
        "tier": "Tier 1 (BAL Vet)",
        "group": "Group B",
        "narrative": "The Juggernaut - 2x BAL main tournament participant",
        "country": "Mozambique",
        "bal_history": "2022 BAL, 2023 BAL (2x participant)",
        "qualifier_2026": "Elite 16 - Group B (4-1 in Group E)",
        "group_e_stats": "W: 4, L: 1, PF: 432, PA: 378, PD: +54",
        "h2h_results": "Beat Matero Magic 94-83",
        "2023_players": "Will Perry, Jermel Kennedy, Ayad Munguambe (leaders)",
        "strengths": "BAL experience, high scoring (432 PF)",
        "storyline": "Clear favorite - proven BAL pedigree"
    },
    
    "Matero Magic": {
        "tier": "Tier 2",
        "group": "Group B",
        "narrative": "The Road Warriors - Zambian champions",
        "country": "Zambia",
        "bal_history": "None - Road to BAL experience",
        "qualifier_2026": "Elite 16 - Group B (3-2 in Group E)",
        "group_e_stats": "W: 3, L: 2, PF: 383, PA: 280, PD: +103",
        "h2h_results": "Lost to Giants 62-84 (-22), Lost to Beira 83-94 (-11)",
        "strengths": "Good point differential (+103), solid scoring",
        "weaknesses": "H2H losses to top teams",
        "storyline": "Strong team but gap vs. elite (needs to close 11-22 pt margins)"
    },
    
    "Dar City": {
        "tier": "Tier 3 (Dark Horse)",
        "group": "Group B",
        "narrative": "Star-Powered Unknown with elite talent",
        "country": "Tanzania",
        "bal_history": "None - Road to BAL debut",
        "qualifier_2026": "Elite 16 - Group B (won Group D)",
        "key_players": "Solo Diabate (former BAL champion), Raphiael Putney (high scorer)",
        "strengths": "Elite individual talent, dominated preliminaries",
        "x_factor": "Star power vs. team system test",
        "storyline": "Unknown quantity with championship-level players"
    },
    
    "Bravehearts": {
        "tier": "Tier 3",
        "group": "Group B",
        "narrative": "The Underdogs - 5x Malawian champions",
        "country": "Malawi",
        "bal_history": "Previous Elite 16 experience (struggled)",
        "qualifier_2026": "Elite 16 - Group B (2-3 in Group E)",
        "group_e_stats": "W: 2, L: 3, PF: 346, PA: 354, PD: -8",
        "h2h_history": "Lost to NCT 68-91 in previous qualifier",
        "domestic_success": "5x Malawian champions",
        "weaknesses": "Negative point differential (-8), Elite 16 struggles",
        "storyline": "Domestic dominance hasn't translated to continental success"
    }
}

# Create comprehensive DataFrame
teams_list = []
for team_name, profile in TEAM_PROFILES.items():
    teams_list.append({
        "Team": team_name,
        "Tier": profile["tier"],
        "Group": profile["group"],
        "Country": profile["country"],
        "Narrative": profile["narrative"],
        "BAL History": profile["bal_history"],
        "2026 Qualifier Status": profile["qualifier_2026"],
        "Key Stats": profile.get("group_e_stats", profile.get("key_stats", "N/A")),
        "Top Players": profile.get("top_players", profile.get("2023_players", profile.get("key_players", "N/A"))),
        "Strengths": profile.get("strengths", "N/A"),
        "Weaknesses": profile.get("weaknesses", "N/A"),
        "H2H Notes": profile.get("h2h_results", profile.get("h2h_history", profile.get("h2h_notes", "N/A"))),
        "X-Factor": profile.get("x_factor", "N/A"),
        "Storyline": profile["storyline"]
    })

df_profiles = pd.DataFrame(teams_list)

# Save comprehensive profiles
df_profiles.to_csv("comprehensive_team_profiles.csv", index=False)

print("\n" + "="*70)
print("COMPREHENSIVE TEAM PROFILES CREATED")
print("="*70)
print(f"\n✓ comprehensive_team_profiles.csv")
print(f"  {len(df_profiles)} teams with full profiles\n")

# Display summary
print("TEAM BREAKDOWN:")
print("-"*70)
for _, row in df_profiles.iterrows():
    print(f"\n{row['Team']} ({row['Tier']})")
    print(f"  Group: {row['Group']}")
    print(f"  BAL History: {row['BAL History']}")
    print(f"  Storyline: {row['Storyline']}")

# Create comparison matrix
print("\n" + "="*70)
print("HEAD-TO-HEAD & COMPARISON DATA")
print("="*70)

h2h_data = [
    {"Team A": "Johannesburg Giants", "Team B": "Matero Magic", "Result": "Giants 84-62", "Margin": "+22", "Date": "Nov 1", "Significance": "Giants dominance"},
    {"Team A": "Ferroviario Da Beira", "Team B": "Matero Magic", "Result": "Beira 94-83", "Margin": "+11", "Significance": "Beira experience edge"},
    {"Team A": "Nairobi City Thunder", "Team B": "Bravehearts", "Result": "NCT 91-68", "Margin": "+23", "Date": "Previous qualifier", "Significance": "Historical matchup"},
]

df_h2h = pd.DataFrame(h2h_data)
df_h2h.to_csv("head_to_head_results.csv", index=False)
print("\n✓ head_to_head_results.csv")
print(f"  {len(df_h2h)} documented H2H results\n")

# Create tier rankings
print("="*70)
print("TIER ANALYSIS")
print("="*70)

tier_analysis = df_profiles.groupby('Tier').agg({
    'Team': lambda x: ', '.join(x),
    'Group': lambda x: list(x)
}).reset_index()

print("\nTier 1 (BAL Veterans):")
tier1 = df_profiles[df_profiles['Tier'].str.contains('Tier 1')]
for _, team in tier1.iterrows():
    print(f"  • {team['Team']}: {team['BAL History']}")

print("\nTier 2 (New Guard/Strong Contenders):")
tier2 = df_profiles[df_profiles['Tier'].str.contains('Tier 2')]
for _, team in tier2.iterrows():
    print(f"  • {team['Team']}: {team['Storyline'][:50]}...")

print("\nTier 3 (Underdogs/Dark Horses):")
tier3 = df_profiles[df_profiles['Tier'].str.contains('Tier 3')]
for _, team in tier3.iterrows():
    print(f"  • {team['Team']}: {team['Storyline'][:50]}...")

print("\n" + "="*70)
print("ALL FILES READY FOR UPLOAD!")
print("="*70)
print("\nCreated files:")
print("  1. comprehensive_team_profiles.csv - Full team profiles")
print("  2. head_to_head_results.csv - H2H matchup data")
print("\nCombine with existing:")
print("  • bal_2026_qualification_data.csv")
print("  • nct_2025_summary_clean.csv")
print("  • nct_2025_player_stats_clean.csv")
print("\nReady to upload all to Google Sheets!")
