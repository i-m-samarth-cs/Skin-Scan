import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import os

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
        # Use the st.file_path special function to find the absolute path
        # This avoids circular imports and path calculation issues
        try:
            # Get the absolute path of where the Streamlit app is running
            import pathlib
            # Get the directory where this file is located
            current_file = pathlib.Path(__file__).resolve()
            # Go up to the project root (parent of pages directory)
            project_root = current_file.parent.parent
            # Build the path to the image
            image_path = project_root / "assets" / "images" / "skin_scan_hero.jpg"
            
            # Check if the file exists
            if image_path.exists():
                st.image(str(image_path), caption="Early detection is crucial")
            else:
                st.warning(f"Image not found at: {image_path}")
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
    
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
        
        if st.button("Start Skin Check", key="skin_check_btn"):
            st.session_state.page = "Skin Cancer Detection"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Patient Portal</h3>
            <p>Register a new patient or access existing patient records</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Manage Patients", key="patient_btn"):
            st.session_state.page = "Patient Information"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>AI Chatbot</h3>
            <p>Have questions about skin cancer? Ask our intelligent assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chat Now", key="chat_btn"):
            st.session_state.page = "Chatbot"
            st.rerun()
    
    # Statistics section
    st.markdown("<h2 style='text-align: center;'>Skin Cancer Statistics</h2>", unsafe_allow_html=True)
    
    stats_cols = st.columns(4)
    
    with stats_cols[0]:
        st.metric(label="New Cases Annually", value="5.4M", delta="↑ 2.3%")
    
    with stats_cols[1]:
        st.metric(label="Early Detection Survival", value="99%", delta="↑ 5%")
    
    with stats_cols[2]:
        st.metric(label="Late Detection Survival", value="25%", delta="↓ 3%")
    
    with stats_cols[3]:
        st.metric(label="Average Diagnosis Age", value="63", delta="↓ 1.2")
    
    # Info section
    st.markdown("""
    <div class="card">
        <h3>How It Works</h3>
        <p>SkinScan AI uses a convolutional neural network trained on over 150,000 images of skin lesions to identify potential skin cancers with high accuracy. Our AI can detect:</p>
        <ul>
            <li>Melanoma</li>
            <li>Basal Cell Carcinoma</li>
            <li>Squamous Cell Carcinoma</li>
            <li>Actinic Keratosis</li>
            <li>Benign Keratosis</li>
            <li>Dermatofibroma</li>
            <li>Vascular Lesions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)