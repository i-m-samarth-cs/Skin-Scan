import sqlite3
import os
import streamlit as st
from datetime import datetime

# Database connection
def get_connection():
    conn = sqlite3.connect('data/patient_records.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database by creating necessary tables
def init_db():
    create_tables()

# Create tables if they do not exist
def create_tables():
    os.makedirs('data', exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        contact TEXT,
        address TEXT,
        medical_history TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create detection results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detection_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        image_path TEXT,
        diagnosis TEXT,
        confidence REAL,
        lesion_location TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Add a detection record
def add_detection_record(patient_id, image_path, diagnosis, confidence, lesion_location, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO detection_results 
           (patient_id, image_path, diagnosis, confidence, lesion_location, notes) 
           VALUES (?, ?, ?, ?, ?, ?)''',
        (patient_id, image_path, diagnosis, confidence, lesion_location, notes)
    )
    conn.commit()
    conn.close()

# Patient management functions
def add_patient(name, age, gender, contact, address, medical_history):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO patients (name, age, gender, contact, address, medical_history) VALUES (?, ?, ?, ?, ?, ?)',
        (name, age, gender, contact, address, medical_history)
    )
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id

def get_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    return patient

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients ORDER BY created_at DESC')
    patients = cursor.fetchall()
    conn.close()
    return patients

def save_detection_result(patient_id, image_path, diagnosis, confidence, lesion_location, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO detection_results (patient_id, image_path, diagnosis, confidence, lesion_location, notes) VALUES (?, ?, ?, ?, ?, ?)',
        (patient_id, image_path, diagnosis, confidence, lesion_location, notes)
    )
    result_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return result_id

def get_patient_detection_history(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM detection_results WHERE patient_id = ? ORDER BY created_at DESC',
        (patient_id,)
    )
    history = cursor.fetchall()
    conn.close()
    return history

def get_all_detection_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT dr.*, p.name as patient_name 
        FROM detection_results dr
        LEFT JOIN patients p ON dr.patient_id = p.id
        ORDER BY dr.created_at DESC
    ''')
    history = cursor.fetchall()
    conn.close()
    return history

# Update patient information
def update_patient(patient_id, name=None, age=None, gender=None, contact=None, address=None, medical_history=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Prepare the fields to update
    fields = []
    values = []
    
    if name:
        fields.append('name = ?')
        values.append(name)
    if age:
        fields.append('age = ?')
        values.append(age)
    if gender:
        fields.append('gender = ?')
        values.append(gender)
    if contact:
        fields.append('contact = ?')
        values.append(contact)
    if address:
        fields.append('address = ?')
        values.append(address)
    if medical_history:
        fields.append('medical_history = ?')
        values.append(medical_history)
    
    # If no fields to update, return None
    if not fields:
        return None
    
    # Create the SQL query to update the patient
    query = f'UPDATE patients SET {", ".join(fields)} WHERE id = ?'
    values.append(patient_id)
    
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
