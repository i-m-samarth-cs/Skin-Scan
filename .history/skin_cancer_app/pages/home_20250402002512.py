import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import speech_recognition as sr
from PIL import Image

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
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Skin Check</h3>
            <p>Upload an image of a skin lesion for immediate analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("skin_check_form", clear_on_submit=True):
            submitted = st.form_submit_button("Start Skin Check")
            if submitted:
                st.session_state['page'] = "detection"
                st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Patient Portal</h3>
            <p>Register a new patient or access existing patient records</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("patient_form", clear_on_submit=True):
            patient_submitted = st.form_submit_button("Manage Patients")
            if patient_submitted:
                st.session_state['page'] = "patient_info"
                st.rerun()
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>AI Chatbot</h3>
            <p>Have questions about skin cancer? Ask our intelligent assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            chat_submitted = st.form_submit_button("Chat Now")
            if chat_submitted:
                st.session_state['page'] = "chatbot"
                st.rerun()
    
    # Navigation menu
    st.markdown("<h3>Navigation Menu</h3>", unsafe_allow_html=True)
    menu_cols = st.columns(3)
    
    with menu_cols[0]:
        if st.button("Go to Skin Check"):
            st.session_state['page'] = "detection"
            st.rerun()
    
    with menu_cols[1]:
        if st.button("Go to Patient Portal"):
            st.session_state['page'] = "patient_info"
            st.rerun()
    
    with menu_cols[2]:
        if st.button("Go to Chatbot"):
            st.session_state['page'] = "chatbot"
            st.rerun()
    
    # Voice Control Section with proper implementation
    st.markdown("<h3>Voice Navigation</h3>", unsafe_allow_html=True)
    
    if "voice_control" not in st.session_state:
        st.session_state["voice_control"] = False
    
    voice_cols = st.columns([1, 5])
    
    with voice_cols[0]:
        mic_icon = "🎤" if not st.session_state["voice_control"] else "🔴"
        if st.button(mic_icon):
            st.session_state["voice_control"] = not st.session_state["voice_control"]
            st.rerun()
    
    with voice_cols[1]:
        if st.session_state["voice_control"]:
            st.write("Voice control is enabled. Click 'Speak Now' to navigate with voice commands.")
            if st.button("Speak Now"):
                command = recognize_speech()
                if command:
                    navigate_with_voice(command)
        else:
            st.write("Voice control is disabled. Click the microphone icon to enable.")

def recognize_speech():
    """Recognize speech using the microphone"""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        command = recognizer.recognize_google(audio).lower()
        st.success(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the command.")
    except sr.RequestError:
        st.error("Error connecting to the speech recognition service.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    return None

def navigate_with_voice(command):
    """Navigate to different pages based on voice command"""
    if "skin check" in command or "detection" in command or "scan" in command:
        st.session_state['page'] = "detection"
        st.rerun()
    elif "patient" in command or "portal" in command or "info" in command:
        st.session_state['page'] = "patient_info"
        st.rerun()
    elif "chat" in command or "bot" in command or "assistant" in command:
        st.session_state['page'] = "chatbot"
        st.rerun()
    else:
        st.warning("Command not recognized. Please try again with 'skin check', 'patient portal', or 'chatbot'.")