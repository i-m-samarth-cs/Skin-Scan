import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        st.write(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        st.write("Sorry, could not understand the command.")
    except sr.RequestError:
        st.write("Error with the speech recognition service.")
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

def show():
    """Display the home page"""
    
    st.markdown("""

SkinScan AI: Advanced Skin Cancer Detection

""", unsafe_allow_html=True)
    
    # Hero section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
         Early Detection Saves Lives

         SkinScan AI uses cutting-edge deep learning technology to help identify potential skin cancer from images. 
            Our system can detect 7 different types of skin conditions with high accuracy.

         Remember: This tool is meant to assist, not replace, professional medical advice.
         """, unsafe_allow_html=True)
        
        st.markdown("""
         Did you know?
         Skin cancer is the most common cancer worldwide
         Early detection increases survival rate to over 95%
         Regular skin checks can help catch cancer in its earliest stages
         """, unsafe_allow_html=True)
    
    with col2:
        st.image("assets/images/skin_scan_hero.jpg", caption="Early detection is crucial")
    
    # Quick access section
    st.markdown("""
Quick Access
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # **Fix: Each button inside its own form**
    with col1:
        st.markdown("""
         Skin Check
         Upload an image of a skin lesion for immediate analysis
        """, unsafe_allow_html=True)
        
        with st.form("home_form"):
            submitted = st.form_submit_button("Start Skin Check")  # Button inside the form
            if submitted:
                st.session_state['page'] = "Skin Cancer Detection"
                st.rerun()
    
    with col2:
        st.markdown("""
         Patient Portal
         Register a new patient or access existing patient records
        """, unsafe_allow_html=True)

        with st.form("patient_form"):  # **Fixed: Wrapping in a form**
            patient_submitted = st.form_submit_button("Manage Patients")
            if patient_submitted:
                st.session_state['page'] = "Patient Information"
                st.rerun()
    
    with col3:
        st.markdown("""
         AI Chatbot
         Have questions about skin cancer? Ask our intelligent assistant
        """, unsafe_allow_html=True)
        
        with st.form("chat_form"):  # **Fixed: Wrapping in a form**
            chat_submitted = st.form_submit_button("Chat Now")
            if chat_submitted:
                st.session_state['page'] = "Chatbot"
                st.rerun()
    
   