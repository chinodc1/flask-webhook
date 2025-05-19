import os
import json
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Enable logging to stdout for Render logs
logging.basicConfig(level=logging.INFO)

# Google Sheets credentials from environment variable 'ggl'
creds_json_str = os.environ.get('ggl')
if not creds_json_str:
    raise Exception("Environment variable 'ggl' with Google credentials JSON not found.")

creds_json = json.loads(creds_json_str)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

sheet = client.open("Webhook Alerts").sheet1  # Make sure this matches your sheet name

@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.info("✅ Webhook endpoint was hit.")
    try:
        data = request.get_json(force=True)
        app.logger.info(f"📦 Received JSON: {data}")

        ticker = data.get('ticker', '')
        interval = data.get('interval', '')
        time = data.get('time', '')
        price = data.get('price', '')

        timestamp = datetime.now(timezone.utc).isoformat()

        sheet.append_row([timestamp, ticker, interval, event, price])
        app.logger.info("📈 Data appended to Google Sheets.")

    except Exception as e:
        app.logger.error(f"❌ Failed processing webhook data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "success", "message": "Data logged to Google Sheets."}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
