from app import create_app
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
app = create_app()

if __name__ == "__main__":
    port = 5001 if os.getenv("ENV") == "dev" else 5000
    app.run(host="0.0.0.0", port=port, debug=True)