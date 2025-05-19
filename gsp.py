from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone
timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/carlos/Downloads/tradingviewwebhooklogger-2143512d62a3.json', scope)

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
    timestamp = datetime.datetime.utcnow().isoformat()

    sheet.append_row([timestamp, ticker, interval, event, price])

    return 'Webhook received and data logged.', 200

if __name__ == '__main__':
    app.run(debug=True)