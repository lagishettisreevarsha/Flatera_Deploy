
#!/usr/bin/env python3

import os
import sys

from sqlalchemy import text
from app import app, db
from init_postgres import init_postgres_database


def start_production_server():
    print("Starting Flatera Backend in Production Mode...")

    try:
        # Initialize database
        print("Initializing PostgreSQL database...")

        with app.app_context():
            init_postgres_database()

            # Verify database connection
            db.session.execute(text("SELECT 1"))
            db.session.commit()

        print("Database initialized successfully!")

        # Get Render port
        port = os.environ.get("PORT", "10000")

        print(f"Starting Gunicorn on port {port}...")

        # Start Gunicorn as the main process
        os.execvp(
            "gunicorn",
            [
                "gunicorn",
                "--bind", f"0.0.0.0:{port}",
                "--timeout", "120",
                "--workers", "2",
                "app:app"
            ]
        )

    except Exception as e:
        print(f"Production startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_production_server()
