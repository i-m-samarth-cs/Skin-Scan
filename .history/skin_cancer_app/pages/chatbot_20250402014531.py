# chatbot.py
import streamlit as st
import time
import random
import openai
import json
import os
from utils.chatbot_utils import get_chatbot_response, get_faq_data

def show():
    """Display the chatbot interface without translation functionality"""
    # Page header with animation
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>SkinScan Assistant</h1>", unsafe_allow_html=True)
    
    # Chatbot configuration
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = os.environ.get('OPENAI_API_KEY', '')
    
    # Toggle between local FAQ and GPT model
    if 'use_gpt' not in st.session_state:
        st.session_state.use_gpt = False
    
    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm the SkinScan Assistant. I can answer your questions about skin cancer, help you navigate the app, or provide general skin health information. How can I help you today?"}
        ]
    
    # Chat UI container with custom styling
    chat_container = st.container()
    
    with chat_container:
        # Custom styling for chat messages
        st.markdown("""
        <style>
        .user-message {
            background-color: #DCF8C6;
            border-radius: 15px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
            align-self: flex-end;
            margin-left: auto;
        }
        .assistant-message {
            background-color: #E3F2FD;
            border-radius: 15px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
        }
        div.stChatMessage {
            padding: 5px;
            border-radius: 15px;
        }
        div.stChatMessage [data-testid="chatAvatarIcon-assistant"] {
            background-color: #2E86C1;
        }
        div.stChatMessage [data-testid="chatAvatarIcon-user"] {
            background-color: #27AE60;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display chat messages with improved styling
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Set up sidebar with options and FAQs
    with st.sidebar:
        st.markdown("## Chat Options")
        
        # API key input for GPT integration
        if st.session_state.use_gpt:
            api_key = st.text_input(
                "OpenAI API Key", 
                value=st.session_state.openai_api_key,
                type="password", 
                help="Enter your OpenAI API key to use GPT for more intelligent responses"
            )
            if api_key != st.session_state.openai_api_key:
                st.session_state.openai_api_key = api_key
        
        # Toggle between built-in FAQ system and GPT
        st.session_state.use_gpt = st.toggle(
            "Use AI-powered responses", 
            value=st.session_state.use_gpt,
            help="Switch between built-in FAQ system and OpenAI GPT for more advanced responses"
        )
        
        # Frequently asked questions section
        st.markdown("## Frequently Asked Questions")
        
        # Get FAQ data
        faq_data = get_faq_data()
        faq_questions = [q["question"] for q in faq_data["faqs"]]
        
        # Display FAQ buttons
        for i, question in enumerate(faq_questions):
            if st.button(question, key=f"faq_{i}"):
                # Add FAQ question to chat history
                st.session_state.chat_history.append({"role": "user", "content": question})
                
                # Get response
                if st.session_state.use_gpt and st.session_state.openai_api_key:
                    # Use GPT for response
                    response = chat_with_gpt(question)
                else:
                    # Use built-in FAQ system
                    response = get_chatbot_response(question)
                
                # Add response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Rerun to display the new messages
                st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I'm the SkinScan Assistant. I can answer your questions about skin cancer, help you navigate the app, or provide general skin health information. How can I help you today?"}
            ]
            st.rerun()
        
        # Disclaimer
        st.markdown("---")
        st.markdown("""
        **Disclaimer:** This chatbot provides general information only and should not be used for diagnosis or as a replacement for professional medical advice.
        """)
    
    # Chat input at the bottom
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Store original input for processing
        original_input = user_input
        
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": original_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(original_input)
        
        # Get chatbot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                if st.session_state.use_gpt and st.session_state.openai_api_key:
                    # Use GPT for response
                    response = chat_with_gpt(original_input)
                else:
                    # Use built-in FAQ system
                    response = get_chatbot_response(original_input)
                
                # Simulate typing effect
                full_response = ""
                # Split by words but preserve punctuation
                words = []
                current_word = ""
                for char in response:
                    if char.isalnum() or char in "'-":
                        current_word += char
                    else:
                        if current_word:
                            words.append(current_word)
                            current_word = ""
                        words.append(char)
                if current_word:
                    words.append(current_word)
                
                for word in words:
                    full_response += word
                    time.sleep(0.02)  # Faster typing speed
                    message_placeholder.write(full_response)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                message_placeholder.write(error_message)
                st.session_state.chat_history.append({"role": "assistant", "content": error_message})

def chat_with_gpt(prompt):
    """Generate a response using OpenAI's GPT API"""
    try:
        # Check if API key is available
        if not st.session_state.openai_api_key:
            return "Please enter an OpenAI API key in the sidebar to use AI-powered responses."
        
        # Set up the OpenAI API
        openai.api_key = st.session_state.openai_api_key
        
        # Create a system message for context
        system_message = """
        You are the SkinScan Assistant, a specialized AI designed to provide information about skin cancer, 
        help users navigate the SkinScan app, and provide general skin health information.
        
        Important guidelines:
        1. Only provide medically accurate information about skin cancer and skin health.
        2. Always emphasize that users should consult healthcare professionals for medical concerns.
        3. Do not diagnose conditions or provide specific medical advice.
        4. Be empathetic, clear, and concise in your responses.
        5. Explain features of the SkinScan app when asked.
        """
        
        # Create message history from recent conversation (last 4 exchanges)
        messages = [{"role": "system", "content": system_message}]
        recent_history = st.session_state.chat_history[-8:] if len(st.session_state.chat_history) > 8 else st.session_state.chat_history
        for message in recent_history:
            messages.append({"role": message["role"], "content": message["content"]})
        
        # Add the current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"I'm having trouble connecting to the AI service. Error: {str(e)}"

if __name__ == "__main__":
    show()