import streamlit as st
import os
from streamlit_option_menu import option_menu
from pages import home, detection, patient_info, history, about, chatbot
from utils.db_manager import create_tables

st.set_page_config(
    page_title="Skin Cancer Detection",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set page configuration
st.set_page_config(
    page_title="SkinScan AI - Skin Cancer Detection",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open(os.path.join("assets", "css", "style.css"), "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize database
def initialize_db():
    create_tables()
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = None

# Application navigation
def navigation():
    with st.sidebar:
        st.image(os.path.join("assets", "images", "logo.png"), width=200)
        
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Skin Cancer Detection", "Patient Information", "History", "Chatbot", "About"],
            icons=["house", "scan", "person", "clock-history", "chat", "info-circle"],
            menu_icon="menu-app",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#f0f2f6"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#2E86C1"},
            }
        )
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Patient ID")
        
        if st.session_state.patient_id:
            st.sidebar.success(f"Current Patient: {st.session_state.patient_id}")
            if st.sidebar.button("Clear Patient"):
                st.session_state.patient_id = None
                st.experimental_rerun()
        else:
            st.sidebar.warning("No patient selected")
            
        st.sidebar.markdown("---")
        st.sidebar.info("This application is for educational purposes only and should not replace professional medical advice.")
        st.sidebar.markdown("© 2025 SkinScan AI")
        
    return selected

# Main application
def main():
    try:
        load_css()
    except:
        st.warning("CSS file not found. Please make sure assets/css/style.css exists.")
    
    initialize_db()
    selected = navigation()
    
    # Render the selected page
    if selected == "Home":
        home.show()
    elif selected == "Skin Cancer Detection":
        detection.show()
    elif selected == "Patient Information":
        patient_info.show()
    elif selected == "History":
        history.show()
    elif selected == "Chatbot":
        chatbot.show()
    elif selected == "About":
        about.show()

if __name__ == "__main__":
    main()