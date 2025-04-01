import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def show():
    """Display the home page"""
    
    st.markdown("<h1 style='text-align: center;'>SkinScan AI: Advanced Skin Cancer Detection</h1>", unsafe_allow_html=True)
    
    # Hero section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2>Early Detection Saves Lives</h2>
            <p>SkinScan AI uses cutting-edge deep learning technology to help identify potential skin cancer from images. 
            Our system can detect 7 different types of skin conditions with high accuracy.</p>
            <p>Remember: This tool is meant to assist, not replace, professional medical advice.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-panel">
            <h3>Did you know?</h3>
            <ul>
                <li>Skin cancer is the most common cancer worldwide</li>
                <li>Early detection increases survival rate to over 95%</li>
                <li>Regular skin checks can help catch cancer in its earliest stages</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("assets/images/skin_scan_hero.jpg", caption="Early detection is crucial")
    
    # Quick access section
    st.markdown("<h2 style='text-align: center;'>Quick Access</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # **Fix: Each button inside its own form**
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Skin Check</h3>
            <p>Upload an image of a skin lesion for immediate analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("home_form"):
            submitted = st.form_submit_button("Start Skin Check")  # Button inside the form
            if submitted:
                st.session_state['page'] = "Skin Cancer Detection"
                st.rerun()

    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Patient Portal</h3>
            <p>Register a new patient or access existing patient records</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("patient_form"):  # **Fixed: Wrapping in a form**
            patient_submitted = st.form_submit_button("Manage Patients")
            if patient_submitted:
                st.session_state['page'] = "Patient Information"
                st.rerun()

    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>AI Chatbot</h3>
            <p>Have questions about skin cancer? Ask our intelligent assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("chat_form"):  # **Fixed: Wrapping in a form**
            chat_submitted = st.form_submit_button("Chat Now")
            if chat_submitted:
                st.session_state['page'] = "Chatbot"
                st.rerun()

import streamlit as st
import speech_recognition as sr
from PIL import Image

# Ensure PyAudio is installed: pip install pyaudio speechrecognition

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source, timeout=5)  # Timeout to prevent hanging
    
    try:
        command = recognizer.recognize_google(audio).lower()
        st.write(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the command.")
    except sr.RequestError:
        st.error("Error connecting to the speech recognition service.")
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
    
    return None

def navigate_with_voice():
    command = recognize_speech()
    if command:
        if "skin check" in command:
            st.session_state['page'] = "Skin Cancer Detection"
        elif "patient portal" in command:
            st.session_state['page'] = "Patient Information"
        elif "chatbot" in command:
            st.session_state['page'] = "Chatbot"
        st.rerun()

# ✅ Voice Control Section with Microphone Icon
st.subheader("Voice Control")

if "voice_control" not in st.session_state:
    st.session_state["voice_control"] = False

col1, col2 = st.columns([1, 5])

with col1:
    mic_icon = "🎤" if not st.session_state["voice_control"] else "🔴"
    if st.button(mic_icon):
        st.session_state["voice_control"] = not st.session_state["voice_control"]
        st.rerun()

with col2:
    if st.session_state["voice_control"]:
        st.write("Voice control is enabled.")
        if st.button("Use Voice Command"):
            navigate_with_voice()
    else:
        st.write("Voice control is disabled.")
