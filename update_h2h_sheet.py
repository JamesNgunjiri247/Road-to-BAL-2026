import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Setup credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(credentials)

# Open spreadsheet
SPREADSHEET_ID = '1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU'
spreadsheet = client.open_by_key(SPREADSHEET_ID)

print(f"✓ Opened: {spreadsheet.title}")

# Read the updated CSV
df = pd.read_csv('head_to_head_results.csv')
df = df.fillna('')

print(f"\n✓ Loaded {len(df)} head-to-head results")
print(df)

# Find or create the worksheet
worksheet_title = "Head-to-Head Results"
try:
    worksheet = spreadsheet.worksheet(worksheet_title)
    print(f"\n✓ Found existing worksheet: {worksheet_title}")
except:
    worksheet = spreadsheet.add_worksheet(title=worksheet_title, rows=100, cols=10)
    print(f"\n✓ Created new worksheet: {worksheet_title}")

# Clear existing content
worksheet.clear()

# Update with new data
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print(f"\n✓ Updated {worksheet_title}")
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(df.columns)}")

# Format header row
worksheet.format('A1:F1', {
    'backgroundColor': {'red': 0.0, 'green': 0.3, 'blue': 0.6},
    'textFormat': {'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}, 'bold': True}
})

# Auto-resize columns
worksheet.columns_auto_resize(0, len(df.columns))

print(f"\n✓ Formatting applied")
print("\n✅ HEAD-TO-HEAD RESULTS UPDATED SUCCESSFULLY!")
