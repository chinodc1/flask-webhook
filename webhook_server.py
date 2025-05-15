import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("TradingView Alert Received:", data)  # Logs the full JSON payload
        if data is None:
            print("Warning: Received empty JSON payload")
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port or default to 10000
    app.run(host='0.0.0.0', port=port)
