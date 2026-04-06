from app import create_app
from app.database import db
from app.models import Environment

app = create_app()

with app.app_context():

    envs = [
        Environment(name="dev", status="active"),
        Environment(name="staging", status="active"),
        Environment(name="production", status="inactive")
    ]

    db.session.add_all(envs)
    db.session.commit()

    print("Environments inserted successfully")
