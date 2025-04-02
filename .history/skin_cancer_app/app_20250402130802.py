# Set page configuration must come first, before any other st commands
import streamlit as st
st.set_page_config(
    page_title="SkinScan AI - Skin Cancer Detection",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import the rest
import os
from streamlit_option_menu import option_menu
from pages import home, detection, patient_info, history, about, chatbot
from utils.db_manager import create_tables
import speech_recognition as sr
import base64

# Define a function to get the absolute path to assets
def get_asset_path(folder_type, filename):
    """
    Get the absolute path to an asset file
    
    Args:
        folder_type: The subfolder in assets (e.g., 'images', 'css')
        filename: The name of the file
    
    Returns:
        str: Absolute path to the asset file
    """
    # Get the root directory of the project based on the location of app.py
    current_file = os.path.abspath(__file__)  # Path to app.py
    project_root = os.path.dirname(current_file)  # Path to project root
    
    # Construct the path to the asset
    asset_path = os.path.join(project_root, "assets", folder_type, filename)
    
    return asset_path

# Hide default Streamlit menu and footer using a more reliable method
def hide_streamlit_elements():
    # CSS to hide the default menu, footer, and header
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        div[data-testid="stToolbar"] {visibility: hidden !important;}
        div[data-testid="stDecoration"] {visibility: hidden !important;}
        div[data-testid="stStatusWidget"] {visibility: hidden !important;}
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
        </style>
        """
    # Inject the CSS with markdown
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Alternative method to hide elements
    hide_menu_hack_js = """
    <script>
    // Wait for the DOM to load
    document.addEventListener('DOMContentLoaded', function() {
        // Create a mutation observer to watch for changes to the body
        const observer = new MutationObserver(function(mutations) {
            const mainMenu = document.querySelector('#MainMenu');
            const footer = document.querySelector('footer');
            const header = document.querySelector('header');
            
            if (mainMenu) mainMenu.style.display = 'none';
            if (footer) footer.style.display = 'none';
            if (header) header.style.display = 'none';
            
            // Hide any element with stToolbar class
            document.querySelectorAll('[data-testid="stToolbar"]').forEach(el => {
                el.style.display = 'none';
            });
        });
        
        // Start observing the document body for changes
        observer.observe(document.body, { childList: true, subtree: true });
    });
    </script>
    """
    
    # Inject JavaScript to hide menu
    st.markdown(hide_menu_hack_js, unsafe_allow_html=True)

# Custom CSS loader
def load_css():
    css_path = get_asset_path("css", "style.css")
    try:
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Please make sure assets/css/style.css exists.")

# Initialize database
def initialize_db():
    create_tables()
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = None
    
    # Initialize page state if not present
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

# Speech recognition function
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

# Voice navigation function
def navigate_with_voice(command):
    """Navigate to different pages based on voice command"""
    if any(keyword in command for keyword in ["home", "main", "start"]):
        st.session_state.page = "Home"
    elif any(keyword in command for keyword in ["skin check", "detection", "scan"]):
        st.session_state.page = "Skin Cancer Detection"
    elif any(keyword in command for keyword in ["patient", "portal", "info"]):
        st.session_state.page = "Patient Information"
    elif any(keyword in command for keyword in ["history", "records", "past"]):
        st.session_state.page = "History"
    elif any(keyword in command for keyword in ["chat", "bot", "assistant"]):
        st.session_state.page = "Chatbot"
    elif any(keyword in command for keyword in ["about", "info", "help"]):
        st.session_state.page = "About"
    else:
        st.warning("Command not recognized. Please try again.")
        return False
    return True

# Application navigation sidebar
def navigation():
    with st.sidebar:
        logo_path = get_asset_path("images", "logo.png")
        try:
            st.image(logo_path, width=200)
        except Exception as e:
            st.warning(f"Logo image not found: {str(e)}")
        
        # Get the current page from session state if set by voice or button
        default_idx = 0
        page_options = ["Home", "Skin Cancer Detection", "Patient Information", "History", "Chatbot", "About"]
        
        if st.session_state.page in page_options:
            default_idx = page_options.index(st.session_state.page)
        
        selected = option_menu(
            menu_title="Main Menu",
            options=page_options,
            icons=["house", "scan", "person", "clock-history", "chat", "info-circle"],
            menu_icon="menu-app",
            default_index=default_idx,
            styles={
                "container": {"padding": "5!important", "background-color": "#f0f2f6"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#2E86C1"},
            }
        )
        
        # Update session state with the selected page
        st.session_state.page = selected
        
        # Voice control section
        st.sidebar.markdown("---")
        st.sidebar.subheader("Voice Navigation")
        
        if "voice_control" not in st.session_state:
            st.session_state.voice_control = False
        
        col1, col2 = st.sidebar.columns([1, 3])
        with col1:
            mic_icon = "🎤" if not st.session_state.voice_control else "🔴"
            if st.button(mic_icon):
                st.session_state.voice_control = not st.session_state.voice_control
                st.rerun()
        
        with col2:
            if st.session_state.voice_control:
                st.write("Voice enabled")
                if st.button("Speak Now"):
                    command = recognize_speech()
                    if command and navigate_with_voice(command):
                        st.rerun()
            else:
                st.write("Voice disabled")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Patient ID")
        
        if st.session_state.patient_id:
            st.sidebar.success(f"Current Patient: {st.session_state.patient_id}")
            if st.sidebar.button("Clear Patient"):
                st.session_state.patient_id = None
                st.rerun()
        else:
            st.sidebar.warning("No patient selected")
            
        st.sidebar.markdown("---")
        st.sidebar.info("This application is for educational purposes only and should not replace professional medical advice.")
        st.sidebar.markdown("© 2025 SkinScan AI")
        
    return selected

# Make the asset path function available to other modules
import sys
sys.modules[__name__].get_asset_path = get_asset_path

# Main application function
def main():
    # Call this before any other Streamlit elements
    hide_streamlit_elements()
    load_css()
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