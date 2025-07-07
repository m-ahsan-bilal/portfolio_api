# Example of how to add database support for persistent storage
# This is just an example - you can add this later when you need it

import sqlite3
from datetime import datetime

def setup_database():
    """Create the database and table"""
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            topic TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT DEFAULT 'received'
        )
    ''')
    
    conn.commit()
    conn.close()

def save_submission_to_db(email, topic, message):
    """Save a submission to the database"""
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO contact_submissions (email, topic, message, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (email, topic, message, datetime.now().isoformat()))
    
    submission_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return submission_id

def get_submission_from_db(submission_id):
    """Get a submission from the database"""
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contact_submissions WHERE id = ?', (submission_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "email": result[1],
            "topic": result[2],
            "message": result[3],
            "timestamp": result[4],
            "status": result[5]
        }
    return None

# To use this in your main.py:
# 1. Call setup_database() when the app starts
# 2. Replace contact_submissions.append() with save_submission_to_db()
# 3. Replace contact_submissions[submission_id - 1] with get_submission_from_db() 
