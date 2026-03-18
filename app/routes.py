from flask import Blueprint, jsonify, render_template, request
import psutil
import time
import os
from .models import Environment, Build, Deployment, SystemMetrics
from .database import db
import requests
from sqlalchemy import text
import logging
import subprocess
from .deployment_service import deploy_container

logger = logging.getLogger(__name__)

JENKINS_URL = os.getenv("JENKINS_URL")
JOB_NAME = os.getenv("JENKINS_JOB")
USERNAME = os.getenv("JENKINS_USER")
API_TOKEN = os.getenv("JENKINS_TOKEN")

main = Blueprint("main", __name__)

VERSION = "1.0.0"

# ---------------- DASHBOARD ----------------

@main.route("/")
def dashboard():
    return render_template("dashboard.html")


# ---------------- STATUS ----------------

@main.route("/api/status")
def status():
    return jsonify({
        "environment": os.getenv("ENV", "production"),
        "status": "running",
        "version": VERSION
    })


# ---------------- SYSTEM INFO ----------------

@main.route("/api/system")
def system():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    })


# ---------------- DEPLOYMENTS ----------------

@main.route("/api/deployments")
def get_deployments():
    deployments = Deployment.query.all()

    result = []

    for d in deployments:
        result.append({
            "id": d.id,
            "environment": d.environment,
            "version": d.version,
            "status": d.status,
            "timestamp": d.timestamp.isoformat() if d.timestamp else None
        })

    return jsonify(result), 200


# ---------------- HEALTH CHECK ----------------

@main.route("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        db_status = "UP"
    except Exception:
        db_status = "DOWN"

    return jsonify({
        "status": "UP",
        "service": "Automated Deployment Platform",
        "version": VERSION,
        "environment": os.getenv("ENV", "production"),
        "database": db_status
    }), 200


# ---------------- ENVIRONMENTS ----------------

@main.route("/api/environments")
def get_environments():
    envs = Environment.query.all()

    result = [
        {"id": e.id, "name": e.name, "status": e.status}
        for e in envs
    ]

    return jsonify(result), 200


# ---------------- TRIGGER BUILD ----------------

@main.route("/trigger-build", methods=["POST"])
def trigger_build():

    if not JENKINS_URL:
        return jsonify({"error": "Jenkins not configured"}), 500

    url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

    response = requests.post(
        url,
        auth=(USERNAME, API_TOKEN)
    )

    if response.status_code in [200, 201]:
        build = Build(status="Triggered")
        db.session.add(build)
        db.session.commit()

        return jsonify({"status": "Build Triggered"})

    return jsonify({"status": "Failed"}), 500


# ---------------- BUILD HISTORY ----------------

@main.route("/api/build-history")
def build_history():

    if not all([JENKINS_URL, JOB_NAME, USERNAME, API_TOKEN]):
        return jsonify({"error": "Jenkins configuration missing"}), 500

    try:

        url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"

        response = requests.get(url, auth=(USERNAME, API_TOKEN))

        if response.status_code == 200:

            data = response.json()

            return jsonify({
                "build_number": data.get("number"),
                "status": data.get("result"),
                "timestamp": data.get("timestamp")
            }), 200

        return jsonify({"error": "Failed to fetch build status"}), 500

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# ---------------- METRICS ----------------

@main.route("/api/metrics")
def metrics():

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    metric = SystemMetrics(cpu=cpu, memory=memory)

    db.session.add(metric)
    db.session.commit()

    return jsonify({
        "cpu": cpu,
        "memory": memory
    }), 200


# ---------------- LOGS ----------------

@main.route("/api/logs")
def logs():

    try:

        container_name = os.getenv("CONTAINER_NAME", "automated-app-dev")

        result = subprocess.getoutput(
            f"docker logs {container_name} --tail 20"
        )

        return jsonify({
            "logs": result.split("\n")
        }), 200

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# ---------------- PAGE ROUTES ----------------

@main.route("/environments")
def environments():
    return render_template("environments.html")


@main.route("/builds")
def builds():
    return render_template("builds.html")


@main.route("/deployments")
def deployments():
    return render_template("deployments.html")


@main.route("/monitoring")
def monitoring():
    return render_template("monitoring.html")


@main.route("/logs-page")
def logs_page():
    return render_template("logs.html")


@main.route("/settings")
def settings():
    return render_template("settings.html")


# ---------------- SYSTEM METRICS ----------------

start_time = time.time()

@main.route("/api/system-metrics")
def system_metrics():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    uptime_seconds = int(time.time() - start_time)
    uptime = str(uptime_seconds) + " seconds"

    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "uptime": uptime
    })


# ---------------- DEPLOY APPLICATION ----------------

@main.route("/deploy", methods=["POST"])
def deploy():

    #Get request data from Jenkins/API
    data = request.json

    environment = data.get("environment")
    version = data.get("version")

    #Validate input
    if not environment or not version:
        return jsonify({"error": "Missing environment or version"}), 400

    logger.info(f"Starting deployment for {environment} with version {version}")

    try:
        #Call deployment logic (THIS is where actual Docker commands run)
        success = deploy_container(version, environment)

        if success:
            #Save deployment record in DB
            deployment = Deployment(
                environment=environment,
                version=version,
                status="Successful"
            )

            db.session.add(deployment)
            db.session.commit()

            logger.info("Deployment successful")

            return jsonify({"status": "Deployment Successful"}), 200

        else:
            logger.error("Deployment failed inside deploy_container")

            return jsonify({"status": "Deployment Failed"}), 500

    except Exception as e:
        logger.error(f"Deployment exception: {str(e)}")

        return jsonify({"error": str(e)}), 500


# ---------------- DEPLOYMENT HISTORY ----------------

@main.route("/api/deployment-history")
def deployment_history():

    deployments = Deployment.query.order_by(
        Deployment.timestamp.desc()
    ).all()

    result = []

    for d in deployments:

        result.append({
            "environment": d.environment,
            "version": d.version,
            "status": d.status,
            "timestamp": d.timestamp.isoformat()
        })

    return jsonify(result)