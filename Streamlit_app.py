import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Set Streamlit page configuration
st.set_page_config(page_title="Grok AI Chatbot", layout="centered")
st.title("🤖 Grok AI Chatbot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare messages for Groq API
    messages = [{"role": "system", "content": "You are Grok, a witty and insightful AI assistant."}]
    messages.extend(st.session_state.chat_history)

    # Call Groq API
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Replace with your desired model
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        grok_reply = response.choices[0].message.content
    except Exception as e:
        grok_reply = f"An error occurred: {e}"

    # Append Grok's reply to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": grok_reply})

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])
