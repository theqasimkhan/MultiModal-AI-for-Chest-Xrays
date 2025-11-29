import sqlite3
import json
from datetime import datetime

DB_NAME = "medical_reports.db"

def init_db():
    """Initialize the database with the reports table"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            exam_date TEXT,
            upload_date TEXT,
            image_path TEXT,
            clinical_indication TEXT,
            findings TEXT,
            report_text TEXT,
            structured_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_report(patient_name, exam_date, image_path, clinical_indication, findings, report_text, structured_data):
    """Save a new report to the database"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure structured_data is a string
    if isinstance(structured_data, dict):
        structured_data = json.dumps(structured_data)
        
    c.execute('''
        INSERT INTO reports (patient_name, exam_date, upload_date, image_path, clinical_indication, findings, report_text, structured_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (patient_name, exam_date, upload_date, image_path, clinical_indication, findings, report_text, structured_data))
    
    conn.commit()
    report_id = c.lastrowid
    conn.close()
    return report_id

def get_reports(query=None):
    """
    Retrieve reports from the database.
    If query is provided, search by patient name or date.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if query:
        search_term = f"%{query}%"
        c.execute('''
            SELECT * FROM reports 
            WHERE patient_name LIKE ? OR exam_date LIKE ? 
            ORDER BY upload_date DESC
        ''', (search_term, search_term))
    else:
        c.execute('SELECT * FROM reports ORDER BY upload_date DESC')
        
    rows = c.fetchall()
    reports = []
    for row in rows:
        reports.append(dict(row))
        
    conn.close()
    return reports

def get_report_by_id(report_id):
    """Retrieve a specific report by ID"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
    row = c.fetchone()
    
    conn.close()
    if row:
        return dict(row)
    return None

# Initialize DB on module import
init_db()
