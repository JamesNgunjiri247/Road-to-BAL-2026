import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_ID = '1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU'

# Authenticate
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open spreadsheet
spreadsheet = client.open_by_key(SPREADSHEET_ID)
print(f"✓ Opened: {spreadsheet.title}")

# Load qualification data
df = pd.read_csv('bal_2026_qualification_data.csv')

# Replace NaN values with empty strings for Google Sheets compatibility
df = df.fillna('')

print(f"✓ Loaded {len(df)} qualification records")
print(df.head())

# Try to find existing worksheet or create new one
worksheet_title = "BAL 2026 Qualification Data"
try:
    worksheet = spreadsheet.worksheet(worksheet_title)
    print(f"✓ Found existing worksheet: {worksheet_title}")
except:
    worksheet = spreadsheet.add_worksheet(title=worksheet_title, rows=100, cols=20)
    print(f"✓ Created new worksheet: {worksheet_title}")

# Clear existing data
worksheet.clear()

# Prepare data
headers = df.columns.tolist()
data = [headers] + df.values.tolist()

# Update worksheet
worksheet.update(data, value_input_option='USER_ENTERED')
print(f"✓ Updated {worksheet_title}")
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(headers)}")

# Apply formatting
# Header row - Blue background, white text, bold
worksheet.format('A1:O1', {
    'backgroundColor': {'red': 0.0, 'green': 0.3, 'blue': 0.6},
    'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True},
    'horizontalAlignment': 'CENTER'
})

# Freeze header row
worksheet.freeze(rows=1)

# Auto-resize columns
worksheet.columns_auto_resize(0, len(headers)-1)

print("✓ Formatting applied")
print(f"✅ BAL 2026 QUALIFICATION DATA UPDATED SUCCESSFULLY!")
