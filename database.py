import sqlite3
import pandas as pd

DB = "csf_v2.db"

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            date_of_birth TEXT,
            phone TEXT,
            cin TEXT,
            health_center TEXT,
            blood_group TEXT,
            allergies TEXT,
            medical_history TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            record_date TEXT,
            reason TEXT,
            diagnosis TEXT,
            treatment TEXT,
            professional TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            appointment_date TEXT,
            purpose TEXT,
            status TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            title TEXT,
            document_type TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            screening_date TEXT,
            screening_type TEXT,
            result TEXT,
            notes TEXT,
            professional TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        """)

def add_patient(last, first, dob, phone, cin, center, blood, allergies, history):
    with connect() as c:
        c.execute("""INSERT INTO patients
        (last_name, first_name, date_of_birth, phone, cin, health_center,
         blood_group, allergies, medical_history)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (last, first, dob, phone, cin, center, blood, allergies, history))

def get_patients():
    with connect() as c:
        return pd.read_sql_query(
            "SELECT id, last_name, first_name, date_of_birth, phone, cin, health_center, blood_group, allergies, medical_history, created_at FROM patients ORDER BY last_name, first_name", c)

def get_patient(patient_id):
    with connect() as c:
        row = c.execute("SELECT * FROM patients WHERE id=?", (int(patient_id),)).fetchone()
        return dict(row) if row else None

def add_record(patient_id, category, record_date, reason, diagnosis, treatment, professional):
    with connect() as c:
        c.execute("""INSERT INTO medical_records
        (patient_id, category, record_date, reason, diagnosis, treatment, professional)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (int(patient_id), category, record_date, reason, diagnosis, treatment, professional))

def get_records(patient_id, category=None):
    with connect() as c:
        if category:
            q = "SELECT category, record_date, reason, diagnosis, treatment, professional FROM medical_records WHERE patient_id=? AND category=? ORDER BY record_date DESC"
            return pd.read_sql_query(q, c, params=(int(patient_id), category))
        q = "SELECT category, record_date, reason, diagnosis, treatment, professional FROM medical_records WHERE patient_id=? ORDER BY record_date DESC"
        return pd.read_sql_query(q, c, params=(int(patient_id),))

def add_appointment(patient_id, d, purpose, status):
    with connect() as c:
        c.execute("INSERT INTO appointments (patient_id, appointment_date, purpose, status) VALUES (?, ?, ?, ?)",
                  (int(patient_id), d, purpose, status))

def get_appointments(patient_id):
    with connect() as c:
        return pd.read_sql_query("SELECT appointment_date, purpose, status FROM appointments WHERE patient_id=? ORDER BY appointment_date DESC",
                                 c, params=(int(patient_id),))

def add_document(patient_id, title, doc_type, description):
    with connect() as c:
        c.execute("INSERT INTO documents (patient_id, title, document_type, description) VALUES (?, ?, ?, ?)",
                  (int(patient_id), title, doc_type, description))

def get_documents(patient_id):
    with connect() as c:
        return pd.read_sql_query("SELECT title, document_type, description, created_at FROM documents WHERE patient_id=? ORDER BY created_at DESC",
                                 c, params=(int(patient_id),))

def add_screening(patient_id, d, kind, result, notes, professional):
    with connect() as c:
        c.execute("""INSERT INTO screenings
        (patient_id, screening_date, screening_type, result, notes, professional)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (int(patient_id), d, kind, result, notes, professional))

def get_screenings(patient_id):
    with connect() as c:
        return pd.read_sql_query("SELECT screening_date, screening_type, result, notes, professional FROM screenings WHERE patient_id=? ORDER BY screening_date DESC",
                                 c, params=(int(patient_id),))
