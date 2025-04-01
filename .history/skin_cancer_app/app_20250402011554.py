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
from google.cloud import translate_v2 as translate

# Translation utilities
# Available languages
LANGUAGES = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "zh": "中文",
    "hi": "हिन्दी",
    "ar": "العربية"
}

# Initialize Google Translate client
@st.cache_resource
def get_translate_client():
    return translate.Client()

def translate_text(text, target_language='en'):
    """Translates text to the target language using Google Translate API"""
    if target_language == 'en' or not text:
        return text  # No need to translate if already in English or empty
        
    try:
        client = get_translate_client()
        result = client.translate(
            text,
            target_language=target_language,
            source_language='en'  # Assuming all original content is in English
        )
        return result['translatedText']
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text  # Return original text if translation fails

# Shorthand for translate_text
def t(text):
    """Translate text to the current language"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'  # Default language
        
    if st.session_state.language == 'en':
        return text  # No translation needed for English
    return translate_text(text, st.session_state.language)

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
    css_path = os.path.join("assets", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(t("CSS file not found. Please make sure assets/css/style.css exists."))

# Initialize database
def initialize_db():
    create_tables()
    if 'patient_id' not in st.session_state:
        st.session_state.patient_id = None
    
    # Initialize page state if not present
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    
    # Initialize language if not present
    if 'language' not in st.session_state:
        st.session_state.language = 'en'

# Speech recognition function
def recognize_speech():
    """Recognize speech using the microphone"""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info(t("Listening... Speak now!"))
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        # Use the user's selected language for speech recognition
        command = recognizer.recognize_google(audio, language=st.session_state.language).lower()
        st.success(t("You said:") + f" {command}")
        return command
    except sr.UnknownValueError:
        st.error(t("Sorry, could not understand the command."))
    except sr.RequestError:
        st.error(t("Error connecting to the speech recognition service."))
    except Exception as e:
        st.error(t("Error:") + f" {str(e)}")
    
    return None

# Voice navigation function
def navigate_with_voice(command):
    """Navigate to different pages based on voice command"""
    # Translate common navigation terms to English for processing
    # This allows navigation in any language
    try:
        if st.session_state.language != 'en':
            client = get_translate_client()
            result = client.translate(
                command,
                target_language='en',
                source_language=st.session_state.language
            )
            command = result['translatedText'].lower()
    except Exception:
        # If translation fails, continue with original command
        pass
        
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
        st.warning(t("Command not recognized. Please try again."))
        return False
    return True

# Language selector function
def add_language_selector():
    """Add a language selector to the sidebar"""
    selected_lang = st.selectbox(
        t("Select Language"),
        list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(st.session_state.language) if st.session_state.language in LANGUAGES else 0
    )
    
    # If language changed, update it
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

# Application navigation sidebar
def navigation():
    with st.sidebar:
        logo_path = os.path.join("assets", "images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)
        else:
            st.warning(t("Logo image not found."))
        
        # Add language selector
        add_language_selector()
        
        # Get the current page from session state if set by voice or button
        default_idx = 0
        page_options = ["Home", "Skin Cancer Detection", "Patient Information", "History", "Chatbot", "About"]
        # Translate page options
        translated_options = [t(option) for option in page_options]
        
        if st.session_state.page in page_options:
            default_idx = page_options.index(st.session_state.page)
        
        selected = option_menu(
            menu_title=t("Main Menu"),
            options=translated_options,
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
        
        # Map the translated selection back to the original page name
        selected_index = translated_options.index(selected)
        st.session_state.page = page_options[selected_index]
        
        # Voice control section
        st.sidebar.markdown("---")
        st.sidebar.subheader(t("Voice Navigation"))
        
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
                st.write(t("Voice enabled"))
                if st.button(t("Speak Now")):
                    command = recognize_speech()
                    if command and navigate_with_voice(command):
                        st.rerun()
            else:
                st.write(t("Voice disabled"))
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(t("### Patient ID"))
        
        if st.session_state.patient_id:
            st.sidebar.success(t("Current Patient:") + f" {st.session_state.patient_id}")
            if st.sidebar.button(t("Clear Patient")):
                st.session_state.patient_id = None
                st.rerun()
        else:
            st.sidebar.warning(t("No patient selected"))
            
        st.sidebar.markdown("---")
        st.sidebar.info(t("This application is for educational purposes only and should not replace professional medical advice."))
        st.sidebar.markdown("© 2025 SkinScan AI")
        
    return st.session_state.page

# Main application function
def main():
    # Call this before any other Streamlit elements
    hide_streamlit_elements()
    load_css()
    initialize_db()
    selected = navigation()
    
    # Pass t function to each page component so they can use translation
    translation_context = {
        "t": t,
        "translate_text": translate_text
    }
    
    # Render the selected page
    if selected == "Home":
        home.show(translation_context)
    elif selected == "Skin Cancer Detection":
        detection.show(translation_context)
    elif selected == "Patient Information":
        patient_info.show(translation_context)
    elif selected == "History":
        history.show(translation_context)
    elif selected == "Chatbot":
        chatbot.show(translation_context)
    elif selected == "About":
        about.show(translation_context)

if __name__ == "__main__":
    main()