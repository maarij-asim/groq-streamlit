import streamlit as st
import os
from streamlit_chat import message
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(layout="wide")

# Initialize Groq API key here 
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_streaming_response(response):
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def generate_content(model_name:str,prompt:str,system_message:str="You are a helpful assistant.",max_tokens:int=1024,temperature:int=0.5):
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        stop=None,
        stream=True
    ) 

    return stream

st.title("Smart Bot 🤖")

with st.sidebar:
    st.write("This is a LLM based bot built using **Streamlit💻** and **Groq🖥**")
    model_name = st.selectbox("Models",["llama3-8b-8192","mixtral-8x7b-32768","llama3-70b-8192","gemma-7b-it"])
    system_message = st.text_input("System Message",placeholder="Default : You are a helpful assistant.")
    temperature = st.slider("Temperature",0.0,1.0,0.5,0.2)
    max_tokens = st.selectbox("Max New Tokens",[1024,2048,4096,8196])

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display chat messages from history on app rerun
for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"],):
        st.markdown(message["content"])

# Main reponse generation logic
if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state["chat_history"].append(
        {"role": "user", "content": prompt},
    )
    with st.chat_message("user"):
        st.write(prompt)

    response = generate_content(model_name,prompt,system_message,max_tokens,temperature)
    with st.chat_message("assistant"):
        stream_generator = get_streaming_response(response)
        streamed_reponse = st.write_stream(stream_generator)

    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": streamed_reponse,
        },
    )
