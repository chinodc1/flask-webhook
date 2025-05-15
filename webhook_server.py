from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True, silent=True)
        if data:
            print("TradingView JSON Alert Received:", data)
        else:
            raw = request.data.decode('utf-8')
            print("TradingView Raw Data Received (non-JSON):", raw)
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("Error parsing request:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
