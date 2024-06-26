from huggingface_hub import InferenceClient
import streamlit as st
from utils import generate_response,print_history

messages=[]

if 'key' not in st.session_state:
    st.session_state['key']=''

if st.session_state['key']!='':
    client = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1",token=st.session_state['key'])
@st.experimental_dialog("API key")
def key():
    st.write("Enter API key")
    token = st.text_input("Enter here...")
    if st.button("Submit"):
        st.session_state['key']=token
        st.rerun()

def main():
    st.set_page_config(page_title="Chatbot")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history']=[]
    if st.session_state['key']=='':
        key()
    else:
        st.markdown(
        """
        <style>
        h1 {
            text-align:center;
        }
        h3 {
            text-align:center;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        
        st.title("Rulebook Chatbot")
        
        placeholder=st.empty()
        with placeholder:
            st.subheader("How can i help you?")
        prompt = st.chat_input("Say something")
        
        if prompt:
            placeholder.empty()
            st.session_state['chat_history'] = generate_response(st.session_state['chat_history'],prompt,client)
if __name__ == '__main__':
    main()
