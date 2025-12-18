#!/usr/bin/env python3
"""
Migration script to remove image column from flats table
"""
import sqlite3
import sys
import os

def remove_image_column():
    """Remove image column from flats table"""
    
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'apartment.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if image column exists
        cursor.execute("PRAGMA table_info(flats)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'image' not in columns:
            print("Image column does not exist in flats table")
            return True
        
        # Create backup table without image column
        cursor.execute("""
            CREATE TABLE flats_backup (
                id INTEGER PRIMARY KEY,
                flat_no VARCHAR(10) UNIQUE NOT NULL,
                bedrooms INTEGER NOT NULL,
                sqft INTEGER NOT NULL,
                rent REAL NOT NULL,
                is_available BOOLEAN DEFAULT 1,
                description TEXT,
                features TEXT,
                floor INTEGER,
                tower_id INTEGER NOT NULL,
                FOREIGN KEY (tower_id) REFERENCES towers (id)
            )
        """)
        
        # Copy data from original table to backup
        cursor.execute("""
            INSERT INTO flats_backup (
                id, flat_no, bedrooms, sqft, rent, is_available, 
                description, features, floor, tower_id
            )
            SELECT 
                id, flat_no, bedrooms, sqft, rent, is_available,
                description, features, floor, tower_id
            FROM flats
        """)
        
        # Drop original table
        cursor.execute("DROP TABLE flats")
        
        # Rename backup table to original name
        cursor.execute("ALTER TABLE flats_backup RENAME TO flats")
        
        conn.commit()
        print("Successfully removed image column from flats table")
        return True
        
    except Exception as e:
        print(f"Error removing image column: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = remove_image_column()
    sys.exit(0 if success else 1)
