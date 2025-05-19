from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone
import json
import os

# Get credentials JSON string from environment variable 'ggl'
creds_json_str = os.environ.get('ggl')
if not creds_json_str:
    raise Exception("Environment variable 'ggl' with Google credentials JSON not found.")

# Parse the JSON string to dict
creds_json = json.loads(creds_json_str)

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from dict
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("Webhook Alerts").sheet1

# === Flask App ===
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    ticker = data.get('ticker')
    interval = data.get('interval')
    event = data.get('event')
    price = data.get('price')

    # Use timezone-aware UTC ISO format
    timestamp = datetime.now(timezone.utc).isoformat()

    sheet.append_row([timestamp, ticker, interval, event, price])

    return 'Webhook received and data logged.', 200

if __name__ == '__main__':
    app.run(debug=True)
