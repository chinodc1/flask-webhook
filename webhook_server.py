from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Try parsing JSON first
        data = request.get_json(silent=True)
        if data:
            print("TradingView JSON Alert Received:", data)
        else:
            # If no JSON, print raw data as text
            raw_data = request.data.decode('utf-8')
            print("Received non-JSON payload:", raw_data)

        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("Error processing webhook:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
