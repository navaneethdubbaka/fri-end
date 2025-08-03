from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Home page serving HTML UI
@app.route("/")
def home():
    return render_template("index.html")

# Analyze endpoint: receives drama, forwards to n8n, returns response
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    n8n_webhook_url = 'https://n8n-sgdfdpon.us-east-1.clawcloudrun.com/webhook/f6661e4e-e7b5-4772-830a-7838c0df3234'   # Set this to your public or local n8n webhook

    try:
        n8n_response = requests.post(n8n_webhook_url, json={'text': text}, timeout=10)
        if n8n_response.status_code == 200:
            json_data = n8n_response.json()
            print(json_data)
            return jsonify(json_data)
        else:
            return jsonify({'error': 'n8n returned an error'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to connect to n8n: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

