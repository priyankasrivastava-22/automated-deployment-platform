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

# GET/Health
@main.route("/health") 
def health():
    return {"status": "OK"}

# GET/ environments
@main.route("/api/environments")
def get_environments():
    envs = Environment.query.all()

    result = [
        {"id": e.id, "name": e.name, "status": e.status}
        for e in envs
    ]

    return jsonify(result), 200

#POST /trigger-build
@main.route("/trigger-build", methods=["POST"])
def trigger_build():
    build = Build(status="success")
    db.session.add(build)
    db.session.commit()
    return {"message": "Build triggered", "id": build.id} 

#GET /build-history
@main.route("/api/build-history")
def build_history():
    builds = Build.query.all()

    result = [
        {
            "id": b.id,
            "status": b.status,
            "timestamp": b.timestamp.isoformat() if b.timestamp else None
        }
        for b in builds
    ]

    return jsonify(result), 200

#GET /metrics
@main.route("/api/metrics")
def metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent

    metric = SystemMetrics(cpu=cpu, memory=memory)
    db.session.add(metric)
    db.session.commit()

    return jsonify({"cpu": cpu, "memory": memory}), 200

#GET /logs
@main.route("/api/logs")
def logs():
    return jsonify({
        "logs": [
            "Container started",
            "Build successful",
            "Deployment completed"
        ]
    }), 200