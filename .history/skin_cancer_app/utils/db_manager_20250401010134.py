import sqlite3
import os
import streamlit as st
from datetime import datetime

# Database connection
def get_connection():
    conn = sqlite3.connect('data/patient_records.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables
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
    return histor