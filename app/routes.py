from flask import Blueprint, jsonify, render_template
import psutil
import os
from .models import Deployment

main = Blueprint("main", __name__)

VERSION = "1.0.0"

@main.route("/")
def dashboard():
    return render_template("dashboard.html")

@main.route("/api/status")
def status():
    return jsonify({
        "environment": os.getenv("ENV", "production"),
        "status": "running",
        "version": VERSION
    })

@main.route("/api/system")
def system():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    })

@main.route("/api/deployments")
def get_deployments():
    deployments = Deployment.query.all()
    return jsonify([
        {
            "id": d.id,
            "project_name": d.project_name,
            "status": d.status,
            "timestamp": d.timestamp
        }
        for d in deployments
    ])