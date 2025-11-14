"""
Manual data collection template for live commentary
Fill in during games or from social media/news sources
"""

# NAMUWONGO BLAZERS (Uganda)
# ==========================================

NAMUWONGO_BLAZERS = {
    "team_name": "Namuwongo Blazers",
    "country": "Uganda",
    "league": "NBL Uganda",
    "domestic_achievement": "2025 NBL Uganda Champions (First title)",
    
    # KEY NARRATIVE
    "storyline": "The Kingslayers - Ended City Oilers 10-year dynasty",
    "road_to_bal_status": "First-time participant, Elite 16 Group A",
    
    # PRELIMINARY ROUND
    "prelim_group": "Group D",
    "prelim_record": "1-1",
    "prelim_games": [
        {"opponent": "Djabal Club", "result": "W", "score": "132-58", "date": "Oct 19, 2025", "notes": "Dominant blowout win"},
        {"opponent": "Dar City", "result": "L", "score": "70-83", "date": "Oct 18, 2025", "notes": "Lost to Group D winner"}
    ],
    
    # ELITE 16
    "elite16_group": "Group A",
    "elite16_status": "Not yet started",
    "elite16_opponents": ["Nairobi City Thunder (host)", "Johannesburg Giants", "TBD"],
    
    # PLAYERS (TO BE FILLED MANUALLY)
    "roster": [
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        # Add more players as identified
    ],
    
    # LIVE COMMENTARY TALKING POINTS
    "commentary_points": [
        "Historic first NBL Uganda title in franchise history",
        "Dethroned City Oilers who had won 10 consecutive championships",
        "Massive 74-point win over Djabal Club shows offensive firepower",
        "First-time Road to BAL participants",
        "Elite 16 Group A - faces host Nairobi City Thunder",
        "Uganda basketball rising - national team improvements",
        "Strong preliminary round performance despite 1-1 record"
    ],
    
    # STATS TO TRACK LIVE
    "live_stats_template": {
        "leading_scorer": "",
        "leading_rebounder": "",
        "leading_assists": "",
        "team_fg_pct": "",
        "team_3pt_pct": "",
        "team_ft_pct": "",
        "turnovers": "",
        "fast_break_points": ""
    }
}

# JOHANNESBURG GIANTS (South Africa)
# ==========================================

JOHANNESBURG_GIANTS = {
    "team_name": "Johannesburg Giants",
    "country": "South Africa",
    "league": "SA National Basketball Championship",
    "domestic_achievement": "2025 SA National Champions",
    
    # KEY NARRATIVE
    "storyline": "The Undefeated - Perfect 5-0 in Elite 16 qualifiers",
    "road_to_bal_status": "First-time participant, only undefeated team in preliminaries",
    
    # PRELIMINARY ROUND
    "prelim_group": "Group E",
    "prelim_record": "5-0 (Perfect)",
    "prelim_stats": {
        "points_for": 362,
        "points_against": 280,
        "point_diff": "+82",
        "ppg": 72.4,
        "opp_ppg": 56.0
    },
    "prelim_notable_wins": [
        "Beat Matero Magic 84-62",
        "Beat Ferroviario Da Beira 77-68 (Elite 16)"
    ],
    
    # ELITE 16
    "elite16_group": "Group A",
    "elite16_record": "1-0",
    "elite16_games": [
        {"opponent": "Ferroviario Da Beira", "result": "W", "score": "77-68", "date": "Nov 1, 2025"}
    ],
    
    # PLAYERS (TO BE FILLED MANUALLY)
    "roster": [
        {"jersey": "", "name": "", "position": "", "height": "", "notes": "Key player in undefeated run"},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        # Add more
    ],
    
    # LIVE COMMENTARY TALKING POINTS
    "commentary_points": [
        "Only undefeated team in preliminary rounds (5-0)",
        "Strong defensive team - 56.0 PPG allowed",
        "+82 point differential shows dominance",
        "South African basketball powerhouse",
        "Beat both Tier 1 teams they've faced (Beira 77-68)",
        "Consistent performance - no weak games",
        "Elite 16 Group A contender"
    ],
    
    "live_stats_template": {
        "leading_scorer": "",
        "leading_rebounder": "",
        "leading_assists": "",
        "defensive_stops": "",
        "steals": "",
        "blocks": ""
    }
}

# MATERO MAGIC (Zambia)
# ==========================================

MATERO_MAGIC = {
    "team_name": "Matero Magic",
    "country": "Zambia",
    "league": "Zambia Basketball League",
    "domestic_achievement": "2024-25 Zambia League Champions",
    
    # KEY NARRATIVE
    "storyline": "The Road Warriors - Host team with home court advantage",
    "road_to_bal_status": "Elite 16 host (Lusaka), Mixed preliminary results",
    
    # PRELIMINARY ROUND
    "prelim_group": "Group E",
    "prelim_record": "3-2",
    "prelim_stats": {
        "points_for": 383,
        "points_against": 280,
        "point_diff": "+103",
        "ppg": 76.6,
        "opp_ppg": 56.0
    },
    
    # ELITE 16
    "elite16_group": "Group B",
    "elite16_record": "2-0",
    "elite16_games": [
        {"opponent": "Dolphins", "result": "W", "score": "68-59", "date": "Oct 28, 2025"},
        {"opponent": "Bravehearts", "result": "W", "score": "74-59", "date": "Nov 1, 2025"}
    ],
    
    # PLAYERS (TO BE FILLED MANUALLY)
    "roster": [
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        # Fill during games
    ],
    
    # LIVE COMMENTARY TALKING POINTS
    "commentary_points": [
        "Host team advantage playing in Lusaka",
        "Good point differential (+103) shows offensive capability",
        "Struggles against elite teams - lost to Giants by 22, Beira by 11",
        "Beat weaker opponents convincingly",
        "Need to close 11-22 point gap vs top tier",
        "Zambian basketball growth",
        "2-0 in Elite 16 so far"
    ],
    
    "matchup_notes": {
        "vs_tier1": "Struggles - need improved execution",
        "vs_tier2": "Competitive",
        "vs_tier3": "Dominant"
    }
}

# DAR CITY (Tanzania)
# ==========================================

DAR_CITY = {
    "team_name": "Dar City",
    "country": "Tanzania",
    "league": "Tanzania Basketball League",
    "domestic_achievement": "Tanzania domestic qualification",
    
    # KEY NARRATIVE
    "storyline": "Star-Powered Unknown - Elite individual talent",
    "road_to_bal_status": "Group D winner (2-0 perfect), Elite 16 Group B",
    
    # KEY PLAYERS
    "star_players": [
        {
            "name": "Solo Diabate",
            "notes": "Former BAL champion with AS Salé (Morocco)",
            "significance": "Championship experience and leadership"
        },
        {
            "name": "Raphiael Putney",
            "notes": "High-scoring guard/forward",
            "significance": "Primary offensive weapon"
        }
    ],
    
    # PRELIMINARY ROUND
    "prelim_group": "Group D",
    "prelim_record": "2-0 (Perfect)",
    "prelim_stats": {
        "points_for": 185,
        "points_against": 120,
        "point_diff": "+65",
        "ppg": 92.5,
        "opp_ppg": 60.0
    },
    "prelim_games": [
        {"opponent": "Djabal Club", "result": "W", "score": "102-50", "date": "Oct 17, 2025", "notes": "Dominant win"},
        {"opponent": "Namuwongo Blazers", "result": "W", "score": "83-70", "date": "Oct 18, 2025", "notes": "Beat eventual qualifier"}
    ],
    
    # ELITE 16
    "elite16_group": "Group B",
    "elite16_status": "2-0 in Group D, advancing to Elite 16",
    
    # PLAYERS (TO BE FILLED MANUALLY)
    "roster": [
        {"jersey": "", "name": "Solo Diabate", "position": "F/C", "height": "", "notes": "Former BAL champion"},
        {"jersey": "", "name": "Raphiael Putney", "position": "G/F", "height": "", "notes": "Leading scorer"},
        {"jersey": "", "name": "", "position": "", "height": "", "notes": ""},
        # Fill during games
    ],
    
    # LIVE COMMENTARY TALKING POINTS
    "commentary_points": [
        "Dark horse team with championship-level talent",
        "Solo Diabate brings BAL experience (AS Salé champion)",
        "Highest PPG in Group D (92.5)",
        "Perfect 2-0 preliminary record",
        "Star power vs team system - interesting storyline",
        "Tanzania basketball emerging",
        "Unknown quantity but dangerous opponent",
        "Beat strong Namuwongo Blazers team 83-70"
    ],
    
    "x_factor": "Solo Diabate's leadership and championship experience could be decisive",
    
    "live_stats_template": {
        "diabate_points": "",
        "diabate_rebounds": "",
        "putney_points": "",
        "team_chemistry": "Monitor how stars integrate with team"
    }
}

# SAVE TO DICTIONARY
ALL_TEAMS = {
    "namuwongo_blazers": NAMUWONGO_BLAZERS,
    "johannesburg_giants": JOHANNESBURG_GIANTS,
    "matero_magic": MATERO_MAGIC,
    "dar_city": DAR_CITY
}

# EXPORT INSTRUCTIONS
"""
HOW TO USE THIS TEMPLATE:

1. BEFORE GAMES:
   - Fill in roster information from social media/news
   - Update any new domestic league achievements
   - Note recent form and injuries

2. DURING GAMES:
   - Track live_stats_template fields
   - Note standout performances
   - Record key plays and momentum shifts
   - Update roster with jersey numbers

3. FOR COMMENTARY:
   - Use commentary_points as talking points
   - Reference storylines for narrative context
   - Compare stats to preliminary performance
   - Highlight star players and matchups

4. POST-GAME:
   - Update with final stats
   - Note MVP performances
   - Record for future reference
"""
