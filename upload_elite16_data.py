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
        "csv_file": "elite16_nct_fbe_bhb_stats.csv",
        "worksheet_name": "Elite 16 - 3 Teams Stats",
        "description": "Elite 16 stats for NCT, Ferroviario Da Beira, Bravehearts"
    },
    {
        "csv_file": "elite16_comprehensive_nct_fbe_bhb.csv",
        "worksheet_name": "Elite 16 Comprehensive",
        "description": "Comprehensive Road to BAL 2026 stats (Prelim + Elite 16)"
    },
    {
        "csv_file": "road_to_bal_2026_summary.csv",
        "worksheet_name": "Road to BAL Summary",
        "description": "Preliminary round summary for all 7 teams"
    }
]

for dataset in datasets:
    print(f"\n{'='*60}")
    print(f"Processing: {dataset['worksheet_name']}")
    print(f"Description: {dataset['description']}")
    print(f"{'='*60}")
    
    # Load CSV
    df = pd.read_csv(dataset["csv_file"])
    df = df.fillna('')  # Replace NaN with empty strings
    
    print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Try to find existing worksheet or create new one
    try:
        worksheet = spreadsheet.worksheet(dataset["worksheet_name"])
        print(f"✓ Found existing worksheet")
    except:
        worksheet = spreadsheet.add_worksheet(title=dataset["worksheet_name"], rows=100, cols=30)
        print(f"✓ Created new worksheet")
    
    # Clear existing data
    worksheet.clear()
    
    # Prepare data
    headers = df.columns.tolist()
    data = [headers] + df.values.tolist()
    
    # Update worksheet
    worksheet.update(data, value_input_option='USER_ENTERED')
    print(f"✓ Updated with {len(df)} rows")
    
    # Apply formatting - handle wide sheets
    if len(headers) <= 26:
        end_col = chr(65 + len(headers) - 1)
    else:
        # For columns beyond Z (AA, AB, etc.)
        end_col = 'Z' if len(headers) > 26 else chr(65 + len(headers) - 1)
    
    worksheet.format(f'A1:{end_col}1', {
        'backgroundColor': {'red': 0.0, 'green': 0.3, 'blue': 0.6},
        'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True},
        'horizontalAlignment': 'CENTER'
    })
    
    # Freeze header row
    worksheet.freeze(rows=1)
    
    # Auto-resize columns
    worksheet.columns_auto_resize(0, len(headers)-1)
    
    print(f"✓ Formatting applied")

print("\n" + "="*60)
print("✅ ALL ELITE 16 DATA UPLOADED SUCCESSFULLY!")
print("="*60)
print(f"\nUploaded {len(datasets)} worksheets:")
for dataset in datasets:
    print(f"  • {dataset['worksheet_name']}")
