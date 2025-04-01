import streamlit as st
import time
import random
from utils.chatbot_utils import get_chatbot_response

def show():
    """Display the chatbot interface page"""
    st.markdown("<h1 style='text-align: center;'>SkinScan Assistant</h1>", unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm the SkinScan Assistant. How can I help you today?"}
        ]

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_input := st.chat_input("Type your question here..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            response = get_chatbot_response(user_input)
            message_placeholder = st.empty()
            full_response = ""

            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.write(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": response})

    if st.sidebar.button("Clear Chat History"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! How can I assist you?"}
        ]
        st.experimental_rerun()

if __name__ == "__main__":
    show()
