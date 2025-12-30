#!/usr/bin/env python3
"""
Startup script for the Flask application
This script will:
1. Initialize the PostgreSQL database
2. Start the Flask development server
"""

import os
import sys
from app import app, db
from init_postgres import init_postgres_database

def start_application():
    """Initialize database and start the application"""
    print("🚀 Starting Flatera Backend Application...")
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        init_postgres_database()
        
        print("✅ Database initialized successfully!")
        print("\n" + "="*50)
        print("🏠 FLATERA APARTMENT RENTAL SYSTEM")
        print("="*50)
        print("🌐 Server running at: http://localhost:5000")
        print("👑 Admin Login: admin@flatera.com / admin123")
        print("📋 API Documentation:")
        print("   - Auth: /auth/login, /auth/register")
        print("   - Public: /public/towers, /public/flats, /public/amenities")
        print("   - Admin: /admin/* (requires admin token)")
        print("="*50)
        
        # Start the Flask development server
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_application()