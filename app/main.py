from app import create_app
from flask import jsonify, render_template
import requests
import os

app = create_app()

# ==============================
# JENKINS CONFIG
# ==============================
JENKINS_URL = os.getenv("JENKINS_URL")
JOB_NAME = os.getenv("JENKINS_JOB")
USERNAME = os.getenv("JENKINS_USER")
API_TOKEN = os.getenv("JENKINS_TOKEN")

# ==============================
# ROUTES
# ==============================

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/trigger-build", methods=["POST"])
def trigger_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

    response = requests.post(
        url,
        auth=(USERNAME, API_TOKEN)
    )

    if response.status_code in [200, 201]:
        return jsonify({"status": "Build Triggered"})
    else:
        return jsonify({"status": "Failed to trigger build"}), 500

@app.route("/logs/<build_id>")
def get_logs(build_id):
    url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_id}/consoleText"

    response = requests.get(
        url,
        auth=(USERNAME, API_TOKEN)
    )

    if response.status_code == 200:
        return response.text
    else:
        return "Unable to fetch logs", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)