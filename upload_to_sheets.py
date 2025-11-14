"""
Upload teams_roster_links.csv to Google Sheets

Setup Instructions:
1. Install required package: pip install gspread
2. Set up Google Cloud Console credentials:
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing one
   - Enable Google Sheets API
   - Create Service Account credentials
   - Download JSON key file and save as 'credentials.json' in this folder
3. Share your Google Sheet with the service account email from credentials.json
4. Update SPREADSHEET_NAME or SPREADSHEET_URL below
"""

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# -----------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------
CSV_FILE = "teams_roster_links.csv"
CREDENTIALS_FILE = "credentials.json"

# Option 1: Use spreadsheet name (if you know the exact name)
# SPREADSHEET_NAME = "FIBA Teams Road to BAL 2026"

# Option 2: Or use spreadsheet URL/ID (more reliable)
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU/edit?gid=0#gid=0"  # Paste your Google Sheet URL here

WORKSHEET_NAME = "Teams Data"  # Name of the sheet/tab

# -----------------------------------------------------------------
# UPLOAD FUNCTION
# -----------------------------------------------------------------
def upload_to_google_sheets():
    try:
        # Define the scope
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Authenticate using service account
        print(f"Authenticating with {CREDENTIALS_FILE}...")
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Read CSV data
        print(f"Reading data from {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE)
        print(f"Loaded {len(df)} rows")
        
        # Open or create spreadsheet
        print(f"Opening spreadsheet...")
        if SPREADSHEET_URL:
            spreadsheet = client.open_by_url(SPREADSHEET_URL)
            print(f"Opened spreadsheet: {spreadsheet.url}")
        else:
            print("ERROR: Please provide SPREADSHEET_URL in the configuration")
            return
        
        # Get or create worksheet
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
            worksheet.clear()  # Clear existing data
            print(f"Cleared existing worksheet '{WORKSHEET_NAME}'")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=100, cols=20)
            print(f"Created new worksheet '{WORKSHEET_NAME}'")
        
        # Upload data (includes headers)
        print("Uploading data...")
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        # Format header row
        worksheet.format('A1:Z1', {
            "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.8},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        })
        
        print("-" * 60)
        print(f"✓ SUCCESS: Data uploaded to Google Sheets!")
        print(f"✓ Spreadsheet URL: {spreadsheet.url}")
        print(f"✓ Worksheet: {WORKSHEET_NAME}")
        print(f"✓ Rows uploaded: {len(df)}")
        print("-" * 60)
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
        print("\nMake sure you have:")
        print(f"1. '{CSV_FILE}' in the current directory")
        print(f"2. '{CREDENTIALS_FILE}' (Google service account key)")
        print("\nTo get credentials:")
        print("- Visit: https://console.cloud.google.com/")
        print("- Create a service account with Google Sheets API access")
        print("- Download the JSON key as 'credentials.json'")
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Google Sheets API is enabled in your Google Cloud project")
        print("2. Share your spreadsheet with the service account email")
        print("   Email: sheets-uploader@fiba-data-upload.iam.gserviceaccount.com")
        print("3. Check that credentials.json has the correct permissions")

# -----------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------
if __name__ == "__main__":
    upload_to_google_sheets()
