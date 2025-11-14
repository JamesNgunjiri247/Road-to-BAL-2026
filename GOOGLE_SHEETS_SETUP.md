# Google Sheets Upload Setup Guide

## Quick Start

Follow these steps to upload your FIBA teams data to Google Sheets:

### Step 1: Install Required Package
```bash
.\.venv\Scripts\python.exe -m pip install gspread google-auth
```

### Step 2: Set Up Google Cloud Credentials

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create or Select a Project**
   - Click "Select a Project" → "New Project"
   - Name it (e.g., "FIBA Data Upload")
   - Click "Create"

3. **Enable Google Sheets API**
   - In the search bar, type "Google Sheets API"
   - Click on it and click "Enable"
   - Also enable "Google Drive API" (recommended)

4. **Create Service Account**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name it (e.g., "sheets-uploader")
   - Click "Create and Continue"
   - Skip optional steps, click "Done"

5. **Download Credentials JSON**
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create New Key"
   - Choose "JSON" format
   - Click "Create" (file downloads automatically)
   - Rename the downloaded file to `credentials.json`
   - Move it to: `C:\Users\Bo$$\OneDrive\Documents\ROAD TO BAL\`

6. **Note the Service Account Email**
   - In the service account details, copy the email (looks like: `your-service@project.iam.gserviceaccount.com`)
   - You'll need this to share your spreadsheet

### Step 3: Create or Prepare Google Sheet

**Option A: Let the script create it**
- The script will automatically create a new spreadsheet called "FIBA Teams Road to BAL 2026"
- After running the script once, open the spreadsheet and share it with your service account email

**Option B: Use existing spreadsheet**
1. Create a new Google Sheet or open an existing one
2. Click "Share" button
3. Paste the service account email
4. Give it "Editor" access
5. Update the `SPREADSHEET_NAME` in `upload_to_sheets.py`

### Step 4: Run the Upload Script
```bash
.\.venv\Scripts\python.exe upload_to_sheets.py
```

## Alternative: Simple Method Using Personal Account

If you want to use your personal Google account instead of a service account:

1. Install gspread with OAuth:
```bash
.\.venv\Scripts\python.exe -m pip install gspread gspread-oauth
```

2. Use this simpler script (I can create this for you if needed)

## Troubleshooting

**Error: "Credentials file not found"**
- Make sure `credentials.json` is in the same folder as the script

**Error: "Spreadsheet not found"**
- Make sure you've shared the spreadsheet with the service account email

**Error: "Permission denied"**
- Ensure the service account has "Editor" access to the spreadsheet

**Error: "API not enabled"**
- Go back to Google Cloud Console and enable Google Sheets API

## What the Script Does

1. Reads `teams_roster_links.csv`
2. Authenticates with Google using `credentials.json`
3. Creates or opens the specified Google Sheet
4. Uploads all team data with formatted headers
5. Provides you with the direct URL to view the sheet

---

Need help? Let me know which step you're stuck on!
