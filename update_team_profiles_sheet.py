"""
Update only the Team Profiles worksheet in Google Sheets
"""

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# -----------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU/edit?gid=0#gid=0"

# File to update
CSV_FILE = "comprehensive_team_profiles.csv"
WORKSHEET_NAME = "Team Profiles (All 7 Teams)"

# -----------------------------------------------------------------
# UPDATE FUNCTION
# -----------------------------------------------------------------
def update_team_profiles():
    try:
        # Authenticate
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        print("="*70)
        print("UPDATING TEAM PROFILES WORKSHEET")
        print("="*70)
        print(f"\nAuthenticating with {CREDENTIALS_FILE}...")
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open spreadsheet
        print(f"Opening spreadsheet...")
        spreadsheet = client.open_by_url(SPREADSHEET_URL)
        print(f"✓ Opened: {spreadsheet.title}")
        print(f"  URL: {spreadsheet.url}\n")
        
        # Read CSV
        print(f"Loading {CSV_FILE}...")
        df = pd.read_csv(CSV_FILE)
        df = df.fillna("")
        print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Display data being uploaded
        print("\n" + "-"*70)
        print("DATA TO UPLOAD:")
        print("-"*70)
        print(df.to_string(index=False))
        
        # Get or create worksheet
        print(f"\nAccessing worksheet: {WORKSHEET_NAME}...")
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
            worksheet.clear()
            print(f"✓ Cleared existing worksheet")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=WORKSHEET_NAME, 
                rows=len(df)+50, 
                cols=len(df.columns)+5
            )
            print(f"✓ Created new worksheet")
        
        # Upload data
        print(f"Uploading data...")
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"✓ Uploaded {len(df)} rows")
        
        # Format header
        print(f"Formatting header...")
        worksheet.format('A1:ZZ1', {
            "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.8},
            "textFormat": {
                "bold": True,
                "foregroundColor": {"red": 1, "green": 1, "blue": 1}
            }
        })
        print(f"✓ Formatted header (blue background, white bold text)")
        
        # Auto-resize columns
        print(f"Auto-resizing columns...")
        worksheet.columns_auto_resize(0, len(df.columns))
        print(f"✓ Auto-resized {len(df.columns)} columns")
        
        # Summary
        print("\n" + "="*70)
        print("UPDATE COMPLETE!")
        print("="*70)
        print(f"\n✓ Worksheet: {WORKSHEET_NAME}")
        print(f"✓ Rows updated: {len(df)}")
        print(f"✓ Columns: {len(df.columns)}")
        print(f"\n✓ View updated sheet:")
        print(f"  {spreadsheet.url}")
        print("\n" + "="*70)
        
    except FileNotFoundError:
        print(f"\n❌ ERROR: File not found: {CSV_FILE}")
        print("Make sure the CSV file is in the current directory")
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials.json is in the current directory")
        print("2. Verify the spreadsheet is shared with:")
        print("   sheets-uploader@fiba-data-upload.iam.gserviceaccount.com")
        print("3. Check Google Sheets API is enabled in Google Cloud Console")

# -----------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------
if __name__ == "__main__":
    update_team_profiles()
