# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello Priyanka, DevOps CI/CD Project Running!"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, jsonify, render_template
import psutil
import os

app = Flask(__name__)

VERSION = "1.0.0"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)