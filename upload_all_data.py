"""
Upload BAL 2026 qualification data to Google Sheets
"""

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# -----------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1__XNzNwQ2Ib9ULzQ1NaHt6Jfw5EefkA4-_QojbrLLlU/edit?gid=0#gid=0"

# Files to upload
FILES_TO_UPLOAD = [
    {
        "csv_file": "comprehensive_team_profiles.csv",
        "worksheet_name": "Team Profiles (All 7 Teams)",
        "description": "Comprehensive profiles for all case study teams"
    },
    {
        "csv_file": "head_to_head_results.csv",
        "worksheet_name": "Head-to-Head Results",
        "description": "H2H matchup data and results"
    },
    {
        "csv_file": "case_study_teams_comprehensive_data.csv",
        "worksheet_name": "Scraped Data (All Sources)",
        "description": "All scraped data from specified sites"
    },
    {
        "csv_file": "scraping_summary_by_team.csv",
        "worksheet_name": "Scraping Summary",
        "description": "Summary of data collected per team/source"
    },
    {
        "csv_file": "bal_2026_qualification_data.csv",
        "worksheet_name": "BAL 2026 Qualification Data",
        "description": "Historical qualification data from Wikipedia"
    },
    {
        "csv_file": "teams_roster_links.csv",
        "worksheet_name": "All Teams Roster Links",
        "description": "Complete list of all 23 teams"
    },
    {
        "csv_file": "nct_2025_summary_clean.csv",
        "worksheet_name": "NCT 2025 Summary",
        "description": "NCT key metrics and season overview"
    },
    {
        "csv_file": "nct_2025_team_stats_clean.csv",
        "worksheet_name": "NCT 2025 Team Stats",
        "description": "NCT team statistics (shooting, rebounds, etc.)"
    },
    {
        "csv_file": "nct_2025_player_stats_clean.csv",
        "worksheet_name": "NCT 2025 Player Stats",
        "description": "NCT individual player statistics"
    },
    {
        "csv_file": "nct_2025_game_record_clean.csv",
        "worksheet_name": "NCT 2025 Game Record",
        "description": "NCT home/away win-loss record"
    }
]

# -----------------------------------------------------------------
# UPLOAD FUNCTION
# -----------------------------------------------------------------
def upload_multiple_files():
    try:
        # Authenticate
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        print("="*70)
        print("GOOGLE SHEETS UPLOADER - MULTIPLE FILES")
        print("="*70)
        print(f"\nAuthenticating with {CREDENTIALS_FILE}...")
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open spreadsheet
        print(f"Opening spreadsheet...")
        spreadsheet = client.open_by_url(SPREADSHEET_URL)
        print(f"✓ Opened: {spreadsheet.title}")
        print(f"  URL: {spreadsheet.url}\n")
        
        # Upload each file
        for file_info in FILES_TO_UPLOAD:
            csv_file = file_info["csv_file"]
            worksheet_name = file_info["worksheet_name"]
            description = file_info["description"]
            
            print("-"*70)
            print(f"Uploading: {csv_file}")
            print(f"  → Worksheet: {worksheet_name}")
            print(f"  → {description}")
            
            try:
                # Read CSV
                df = pd.read_csv(csv_file)
                # Replace NaN with empty strings for Google Sheets compatibility
                df = df.fillna("")
                print(f"  ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
                
                # Get or create worksheet
                try:
                    worksheet = spreadsheet.worksheet(worksheet_name)
                    worksheet.clear()
                    print(f"  ✓ Cleared existing worksheet")
                except gspread.WorksheetNotFound:
                    worksheet = spreadsheet.add_worksheet(
                        title=worksheet_name, 
                        rows=len(df)+50, 
                        cols=len(df.columns)+5
                    )
                    print(f"  ✓ Created new worksheet")
                
                # Upload data
                worksheet.update([df.columns.values.tolist()] + df.values.tolist())
                print(f"  ✓ Uploaded data")
                
                # Format header
                worksheet.format('A1:ZZ1', {
                    "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.8},
                    "textFormat": {
                        "bold": True,
                        "foregroundColor": {"red": 1, "green": 1, "blue": 1}
                    }
                })
                print(f"  ✓ Formatted header")
                
                # Auto-resize columns
                worksheet.columns_auto_resize(0, len(df.columns))
                print(f"  ✓ Auto-resized columns")
                
            except FileNotFoundError:
                print(f"  ⚠ File not found: {csv_file} (skipping)")
                continue
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        # Summary
        print("\n" + "="*70)
        print("UPLOAD COMPLETE!")
        print("="*70)
        print(f"\n✓ Spreadsheet URL: {spreadsheet.url}")
        print(f"✓ Files processed: {len(FILES_TO_UPLOAD)}")
        print("\nWorksheets created:")
        for ws in spreadsheet.worksheets():
            print(f"  - {ws.title}")
        print("\n" + "="*70)
        
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
    upload_multiple_files()
