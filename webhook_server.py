from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Enable logging to stdout (Render will capture this)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.info("✅ Webhook endpoint was hit.")
    try:
        data = request.get_json(force=True)
        app.logger.info(f"📦 Received JSON: {data}")
    except Exception as e:
        app.logger.error(f"❌ Failed to parse JSON: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "success"})
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
