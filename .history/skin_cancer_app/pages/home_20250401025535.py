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
        
        with st.form("home_form"):
    st.write("Start your skin check")
            st.session_state['page'] = "Skin Cancer Detection"
            st.rerun()

    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>Patient Portal</h3>
            <p>Register a new patient or access existing patient records</p>
        </div>
        """, unsafe_allow_html=True)
        if st.form_submit_button("Manage Patients", key="home_patient"):
            st.session_state['page'] = "Patient Information"
            st.rerun()

    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>AI Chatbot</h3>
            <p>Have questions about skin cancer? Ask our intelligent assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.form_submit_button("Chat Now", key="home_chat"):
            st.session_state['page'] = "Chatbot"
            st.rerun()

    
    # Statistics section
    st.markdown("<h2 style='text-align: center;'>Skin Cancer Statistics</h2>", unsafe_allow_html=True)
    
    # Generate sample statistics for visualization
    def create_stats_chart():
        cancer_types = ['Melanoma', 'Basal Cell', 'Squamous Cell', 'Other']
        survival_rates = [92, 100, 95, 85]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(cancer_types, survival_rates, color=['#E74C3C', '#3498DB', '#2ECC71', '#F39C12'])
        
        # Add data labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height}%', ha='center', va='bottom')
        
        ax.set_ylim(0, 105)
        ax.set_ylabel('5-Year Survival Rate (%)')
        ax.set_title('Skin Cancer 5-Year Survival Rates with Early Detection')
        
        # Convert plot to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        
        # Encode to base64 for Streamlit
        data = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{data}"
    
    chart_data = create_stats_chart()
    st.markdown(f'<img src="{chart_data}" width="100%"/>', unsafe_allow_html=True)
    
    # Information cards
    st.markdown("<h2 style='text-align: center;'>Types of Skin Cancer</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Melanoma</h3>
            <p>The most dangerous form of skin cancer. Develops from pigment-producing cells (melanocytes). 
            Early detection is critical as it can spread to other parts of the body.</p>
            <h4>Warning Signs:</h4>
            <p>Follow the ABCDE rule: Asymmetry, Border irregularity, Color changes, Diameter growth, Evolution.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>Basal Cell Carcinoma</h3>
            <p>The most common form of skin cancer. Rarely spreads but can cause significant local damage if untreated.</p>
            <h4>Warning Signs:</h4>
            <p>Pearly or waxy bumps, flat flesh-colored or brown lesions, or bleeding/scabbing sores that heal and return.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Squamous Cell Carcinoma</h3>
            <p>The second most common form of skin cancer. Can spread to other parts of the body if left untreated.</p>
            <h4>Warning Signs:</h4>
            <p>Firm red nodules or flat lesions with scaly, crusted surfaces.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>Precancerous Conditions</h3>
            <p>Actinic Keratoses and others can develop into skin cancer if left untreated.</p>
            <h4>Warning Signs:</h4>
            <p>Rough, scaly patches that may be red, brown or skin-colored.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
        <p>SkinScan AI is designed for educational and assistive purposes only.</p>
        <p>Always consult a healthcare professional for medical advice and diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)
