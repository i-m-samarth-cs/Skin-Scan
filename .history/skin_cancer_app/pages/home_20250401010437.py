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
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Skin Check</h3>
            <p>Upload an image of a skin lesion for immediate analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Skin Check", key="home_skin_check"):
            st.session_state['page'] = "Skin Cancer Detection"
            st.experimental_rerun()
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Patient Portal</h3>
            <p>Register a new patient or access existing patient records</p>
        </div>
        """, unsafe_allow_html=True)