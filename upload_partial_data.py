import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU'

# Authenticate
credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key(SPREADSHEET_ID)
print(f"✓ Opened: {spreadsheet.title}")

# Datasets to upload
datasets = [
    {
        "csv_file": "partial_rosters.csv",
        "worksheet_name": "Partial Rosters",
        "description": "Identified players for 4 teams"
    },
    {
        "csv_file": "partial_stats.csv",
        "worksheet_name": "Partial Stats",
        "description": "Detailed statistics from preliminary games"
    },
    {
        "csv_file": "live_commentary_cards.csv",
        "worksheet_name": "Live Commentary Cards",
        "description": "Quick reference cards for live broadcasts"
    }
]

for dataset in datasets:
    print(f"\n{'='*60}")
    print(f"Processing: {dataset['worksheet_name']}")
    print(f"{'='*60}")
    
    # Load CSV
    df = pd.read_csv(dataset["csv_file"])
    df = df.fillna('')
    
    print(f"✓ Loaded {len(df)} rows")
    
    # Try to find or create worksheet
    try:
        worksheet = spreadsheet.worksheet(dataset["worksheet_name"])
        print(f"✓ Found existing worksheet")
    except:
        worksheet = spreadsheet.add_worksheet(title=dataset["worksheet_name"], rows=100, cols=20)
        print(f"✓ Created new worksheet")
    
    # Clear and update
    worksheet.clear()
    
    headers = df.columns.tolist()
    data = [headers] + df.values.tolist()
    
    worksheet.update(data, value_input_option='USER_ENTERED')
    print(f"✓ Updated with {len(df)} rows, {len(headers)} columns")
    
    # Format header
    if len(headers) <= 26:
        end_col = chr(64 + len(headers))
    else:
        end_col = 'Z'
    
    # Color code based on worksheet
    if "Roster" in dataset["worksheet_name"]:
        # Green for rosters
        bg_color = {'red': 0.2, 'green': 0.6, 'blue': 0.3}
    elif "Stats" in dataset["worksheet_name"]:
        # Blue for stats
        bg_color = {'red': 0.0, 'green': 0.3, 'blue': 0.6}
    else:
        # Purple for commentary
        bg_color = {'red': 0.5, 'green': 0.2, 'blue': 0.6}
    
    worksheet.format(f'A1:{end_col}1', {
        'backgroundColor': bg_color,
        'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True},
        'horizontalAlignment': 'CENTER'
    })
    
    # Freeze header
    worksheet.freeze(rows=1)
    
    # Auto-resize columns
    worksheet.columns_auto_resize(0, min(len(headers)-1, 25))
    
    print(f"✓ Formatting applied")

print("\n" + "="*60)
print("✅ ALL PARTIAL DATA UPLOADED TO GOOGLE SHEETS")
print("="*60)

print("\nWorksheets Created:")
print("  1. Partial Rosters (Green) - Player information")
print("  2. Partial Stats (Blue) - Detailed statistics")
print("  3. Live Commentary Cards (Purple) - Quick reference")

print("\n" + "="*60)
print("DATA SUMMARY")
print("="*60)

# Load and display summary
rosters = pd.read_csv("partial_rosters.csv")
stats = pd.read_csv("partial_stats.csv")
cards = pd.read_csv("live_commentary_cards.csv")

print(f"\nRosters: {len(rosters)} players across {len(rosters['Team'].unique())} teams")
for team in rosters['Team'].unique():
    confirmed = len(rosters[(rosters['Team'] == team) & (~rosters['Player_Name'].str.contains('Unknown'))])
    total = len(rosters[rosters['Team'] == team])
    print(f"  • {team}: {confirmed} confirmed / {total} total")

print(f"\nStats: {len(stats)} data points across {len(stats['Team'].unique())} teams")
for team in stats['Team'].unique():
    count = len(stats[stats['Team'] == team])
    print(f"  • {team}: {count} stats")

print(f"\nCommentary Cards: {len(cards)} teams ready for broadcast")

print("\n" + "="*60)
print("READY FOR LIVE COMMENTARY!")
print("="*60)
