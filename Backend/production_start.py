#!/usr/bin/env python3
"""
Production startup script for Flatera Backend
This handles database initialization and starts the server robustly
"""
import os
import sys
import time
from app import app, db
from init_postgres import init_postgres_database

def start_production_server():
    """Start the production server with proper error handling"""
    print("🚀 Starting Flatera Backend in Production Mode...")
    print("=" * 60)
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        init_postgres_database()
        print("✅ Database initialization completed")
        
        # Test database connection
        with app.app_context():
            db.session.execute('SELECT 1')
            print("✅ Database connection verified")
        
        print("\n🌐 Starting Gunicorn server...")
        print(f"   Host: 0.0.0.0")
        print(f"   Port: {os.environ.get('PORT', 5000)}")
        print(f"   Workers: 2")
        print(f"   Timeout: 120s")
        print("=" * 60)
        
        # Start Gunicorn
        port = os.environ.get('PORT', '5000')
        os.system(f"gunicorn -b 0.0.0.0:{port} --timeout 120 --workers 2 --preload app:app")
        
    except Exception as e:
        print(f"❌ Startup error: {str(e)}")
        print("🔄 Attempting to start without database initialization...")
        
        # Fallback: start without database init
        port = os.environ.get('PORT', '5000')
        os.system(f"gunicorn -b 0.0.0.0:{port} --timeout 120 --workers 2 app:app")

if __name__ == "__main__":
    start_production_server()