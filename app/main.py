# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello Priyanka, DevOps CI/CD Project Running!"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


# from flask import Flask, jsonify, render_template
# import psutil
# import os

# app = Flask(__name__)

# VERSION = "1.0.0"

# @app.route("/")
# def dashboard():
#     return render_template("dashboard.html")

# @app.route("/api/status")
# def status():
#     return jsonify({
#         "environment": os.getenv("ENV", "production"),
#         "status": "running",
#         "version": VERSION
#     })

# @app.route("/api/system")
# def system():
#     return jsonify({
#         "cpu": psutil.cpu_percent(),
#         "memory": psutil.virtual_memory().percent
#     })

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import psutil
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

VERSION = "1.0.0"

# Example Model
class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/status")
def status():
    return jsonify({
        "environment": os.getenv("ENV", "production"),
        "status": "running",
        "version": VERSION
    })

@app.route("/api/system")
def system():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    })

@app.route("/api/deployments")
def get_deployments():
    deployments = Deployment.query.all()
    return jsonify([
        {
            "id": d.id,
            "project_name": d.project_name,
            "status": d.status
        }
        for d in deployments
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)