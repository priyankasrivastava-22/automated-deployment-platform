from flask import Blueprint, jsonify, render_template
import psutil
import os
from .models import Environment, Build, Deployment, SystemMetrics
from .database import db

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

# GET/Health
@main.route("/health") 
def health():
    return {"status": "OK"}

# GET/ environments
@main.route("/environments")
def get_environments():
    envs = Environment.query.all()
    return [
        {"id": e.id, "name": e.name, "status": e.status}
        for e in envs
    ]

#POST /trigger-build
@main.route("/trigger-build", methods=["POST"])
def trigger_build():
    build = Build(status="success")
    db.session.add(build)
    db.session.commit()
    return {"message": "Build triggered", "id": build.id} 

#GET /build-history
@main.route("/build-history")
def build_history():
    builds = Build.query.all()
    return [
        {"id": b.id, "status": b.status, "timestamp": b.timestamp}
        for b in builds
    ]

#GET /metrics
@main.route("/metrics")
def metrics():
    import psutil
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    metric = SystemMetrics(cpu=cpu, memory=memory)
    db.session.add(metric)
    db.session.commit()

    return {"cpu": cpu, "memory": memory}

#GET /logs
@main.route("/logs")
def logs():
    return {
        "logs": [
            "Container started",
            "Build successful",
            "Deployment completed"
        ]
    }