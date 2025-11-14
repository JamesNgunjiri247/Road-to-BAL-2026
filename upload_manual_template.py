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

# Load manual template
df = pd.read_csv("open_source_teams_manual_template.csv")
df = df.fillna('')

print(f"\n✓ Loaded {len(df)} teams")
print(df[["Team", "Country", "Data_Source", "Manual_Entry_Required"]].to_string(index=False))

# Create or update worksheet
worksheet_name = "Open Source Teams - Manual Data"

try:
    worksheet = spreadsheet.worksheet(worksheet_name)
    print(f"\n✓ Found existing worksheet")
except:
    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=100, cols=15)
    print(f"\n✓ Created new worksheet")

# Clear and update
worksheet.clear()

headers = df.columns.tolist()
data = [headers] + df.values.tolist()

worksheet.update(data, value_input_option='USER_ENTERED')
print(f"✓ Updated with {len(df)} teams")

# Format header
worksheet.format('A1:J1', {
    'backgroundColor': {'red': 0.9, 'green': 0.5, 'blue': 0.1},  # Orange for manual entry
    'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True},
    'horizontalAlignment': 'CENTER'
})

# Freeze header
worksheet.freeze(rows=1)

# Auto-resize
worksheet.columns_auto_resize(0, len(headers)-1)

print("✓ Formatting applied")

print("\n" + "="*60)
print("✅ MANUAL DATA TEMPLATE UPLOADED TO GOOGLE SHEETS")
print("="*60)
print(f"\nWorksheet: {worksheet_name}")
print("\nNEXT STEPS:")
print("  1. Fill in roster information during Elite 16 games")
print("  2. Check team social media for player names")
print("  3. Use commentary notes during live broadcasts")
print("  4. Track stats manually during games")
