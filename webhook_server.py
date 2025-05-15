from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print("TradingView Alert Received:", data)  # This should print the JSON payload
        if data is None:
            print("Warning: Received empty JSON payload")
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
