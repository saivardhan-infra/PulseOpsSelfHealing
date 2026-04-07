from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    print("🚨 Alert received:", data)

    # Example auto-healing action
    os.system("docker restart flask-app")

    return "OK", 200

app.run(host='0.0.0.0', port=5001)
