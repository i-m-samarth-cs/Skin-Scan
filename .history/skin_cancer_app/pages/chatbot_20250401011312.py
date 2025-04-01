import streamlit as st
import time
import random
from utils.chatbot_utils import get_chatbot_response

def show():
    """Display the chatbot interface page"""
    st.markdown("<h1 style='text-align: center;'>SkinScan Assistant</h1>", unsafe_allow_html=True)
    
    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm the SkinScan Assistant. I can answer your questions about skin cancer, help you navigate the app, or provide general skin health information. How can I help you today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Type your question here..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get chatbot response with a simulated typing effect
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = get_chatbot_response(user_input)
            
            # Simulate typing
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)  # Adjust typing speed as needed
                message_placeholder.write(full_response)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Sidebar with frequently asked questions
    st.sidebar.markdown("## Frequently Asked Questions")
    
    faq_questions = [
        "What are the warning signs of melanoma?",
        "How often should I check my skin?",
        "What SPF sunscreen should I use?",
        "How does the SkinScan app work?",
        "Can SkinScan diagnose my condition?"
    ]
    
    for question in faq_questions:
        if st.sidebar.button(question):
            # Add FAQ question to chat history
            st.session_state.chat_history.append({"role": "user", "content": question})
            
            # Get response
            response = get_chatbot_response(question)
            
            # Add response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Rerun to display the new messages
            st.experimental_rerun()
    
    # Clear chat button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm the SkinScan Assistant. I can answer your questions about skin cancer, help you navigate the app, or provide general skin health information. How can I help you today?"}
        ]
        st.experimental_rerun()
    
    # Disclaimer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Disclaimer:** This chatbot provides general information only and should not be used for diagnosis or as a replacement for professional medical advice.
    """)

if __name__ == "__main__":
    show()