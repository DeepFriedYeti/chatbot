from huggingface_hub import InferenceClient
import streamlit as st
from utils import generate_response

messages=[]

if 'key' not in st.session_state:
    st.session_state['key']=''

if st.session_state['key']=='':
    client = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1")
else:
    client = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1",token=st.session_state['key'])
@st.experimental_dialog("Name")
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
    st.markdown(
    """
    <style>
    h1 {
        text-align:center;
    }
    button.st-emotion-cache-8ijwm3 {
        height: 100px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    
    st.title("Conversational Chatbot")
    
    placeholder=st.empty()
    with placeholder:
        c1=st.container()
        suggestion_msg = {"role":"user","content":"Give three random suggestions for prompts to an ai assistant, your answer should be separated by ';' as a single string, don't add anything like 'Suggestion 1' to the final answer"}
        response=client.chat_completion([suggestion_msg],max_tokens=512,temperature=1)
        response_text = response.choices[0].message.content
        suggestions=response_text.split(";")
        suggestions[0]=suggestions[0].replace('"','')
        suggestions[1]=suggestions[1].replace('"','')
        suggestions[2]=suggestions[2].replace('"','')
        col1,col2,col3=st.columns(3)
        with col1:
            but1= col1.button(suggestions[0],use_container_width=True)
        with col2:
            but2 = col2.button(suggestions[1],use_container_width=True)
        with col3:
            but3 = col3.button(suggestions[2],use_container_width=True)
    prompt = st.chat_input("Say something")
    if but1:
        placeholder.empty()
        generate_response(st.session_state['chat_history'],suggestions[0],client)
    elif but2:
        placeholder.empty()
        generate_response(st.session_state['chat_history'],suggestions[1],client)
    elif but3:
        placeholder.empty()
        generate_response(st.session_state['chat_history'],suggestions[2],client)
    
    if prompt:
        placeholder.empty()
        generate_response(st.session_state['chat_history'],prompt,client)
if __name__ == '__main__':
    main()
