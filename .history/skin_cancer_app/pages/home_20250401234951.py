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
import pyaudio
import wave
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson API Credentials
API_KEY = "f8zDkspU2Jkv8SBQWHvuflJlZAjsiatHYJ-Bmc4aL57P"
SERVICE_URL = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/7dbc66c3-6543-4a70-a380-263b8af09854"
AUDIO_FILE_PATH = "user_audio.wav"

# Function to Record Audio
def record_audio(output_file, record_seconds=5, sample_rate=16000, chunk_size=1024):
    audio_format = pyaudio.paInt16
    channels = 1

    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk_size)

    st.write("🎙 Recording... Speak Now.")
    frames = []
    for _ in range(0, int(sample_rate / chunk_size * record_seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_file, 'wb') as wave_file:
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(audio.get_sample_size(audio_format))
        wave_file.setframerate(sample_rate)
        wave_file.writeframes(b''.join(frames))

# Function to Convert Speech to Text
def speech_to_text(audio_file_path):
    try:
        authenticator = IAMAuthenticator(API_KEY)
        speech_to_text = SpeechToTextV1(authenticator=authenticator)
        speech_to_text.set_service_url(SERVICE_URL)

        with open(audio_file_path, 'rb') as audio_file:
            result = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model='en-US_BroadbandModel'
            ).get_result()

        if result and 'results' in result:
            return result['results'][0]['alternatives'][0]['transcript'].lower()
        else:
            return None
    except Exception as e:
        st.write(f"❌ Error: {e}")
        return None

# Function to Navigate Using Voice Commands
def navigate_with_voice():
    record_audio(AUDIO_FILE_PATH, record_seconds=5)
    command = speech_to_text(AUDIO_FILE_PATH)

    if command:
        st.write(f"🔊 You said: **{command}**")

        if "home" in command:
            st.session_state["home"] = "Home"
        elif "skin check" in command:
            st.session_state["skin"] = "Skin Cancer Detection"
        elif "patient portal" in command:
            st.session_state["page"] = "Patient Information"
        elif "chatbot" in command:
            st.session_state["page"] = "Chatbot"
        else:
            st.write("❌ Command not recognized!")

        st.rerun()

# 🌟 Streamlit UI
st.title("🎤 Voice Navigation")

if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Display Current Page
st.subheader(f"📌 Current Page: {st.session_state['page']}")

if st.button("🎤 Use Voice Command"):
    navigate_with_voice()