from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# Get verification token and endpoint from environment for safety/flexibility
VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN")  # Set this in Render settings!
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")              # Set this in Render settings!

@app.route("/ebay-challenge", methods=["GET"])
def ebay_challenge():
    challenge_code = request.args.get("challenge_code")
    if not challenge_code or not VERIFICATION_TOKEN or not ENDPOINT_URL:
        return jsonify({"error": "Missing required info"}), 400

    m = hashlib.sha256()
    m.update(challenge_code.encode("utf-8"))
    m.update(VERIFICATION_TOKEN.encode("utf-8"))
    m.update(ENDPOINT_URL.encode("utf-8"))
    challenge_response = m.hexdigest()
    return jsonify({"challengeResponse": challenge_response}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
