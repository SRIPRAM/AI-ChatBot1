import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
API_URL="https://api.groq.com/openai/v1/chat/completions"
def chat_with_groq(messages,model="meta-llama/llama-4-scout-17b-16e-instruct",temperature=0.7):
    headers={
        'Authorization':f'Bearer {GROQ_API_KEY}',
        'Content-Type':'application/json'
    }
    payload={
        "model":model,
        "messages":messages,
        "temperature":temperature
    }
    response=requests.post(API_URL,headers=headers,json=payload)
    if response.status_code==200:
        result=response.json()
        reply=result['choices'][0]['message']['content']
        return reply
    else:
        return f"Error{response.status_code}:{response.text}"
st.set_page_config(page_title="AI ChatBot",layout="centered",initial_sidebar_state="collapsed")
st.title("AI Chatbot Powered by Groq LLM")
st.caption("Built with LLaMA 4 Scout via Groq API")
if "messages" not in st.session_state:
    st.session_state.messages=[{"role":"system","content":"Hi! How can I help you today?"}]
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"],avatar="🧑‍💻" if msg["role"]=="user" else "🤖"):
        st.write(msg["content"])
if prompt:=st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user",avatar="🧑‍💻"):
        st.write(prompt)
    with st.chat_message("assistant",avatar="🤖"):
        response=chat_with_groq(st.session_state.messages)
        st.write(response)
    st.session_state.messages.append({"role":"assistant","content":response})
