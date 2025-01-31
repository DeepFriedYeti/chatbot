import streamlit as st
from pdf import handle_query

def print_history(chat_history):
    for i in chat_history:
        if i["role"]=="user":
            with st.chat_message("user"):
                st.write(i["content"])
        elif i["role"]=="assistant":
            with st.chat_message("assistant"):
                st.write(i["content"])

def generate_info(prompt):
    info_list = handle_query(prompt)
    info=""
    for i in info_list:
        info += i+"\n"
    return info

def stream_output(generator):
    for token in generator:
        response = token.choices[0].delta.content
        yield response  

def generate_response(messages,prompt,client):
    print_history(messages)
    info = generate_info(prompt)
    prompt_template="""
    The user has sent the following message, "{query}". If you think that this is referring to some external information,
    then use the following information, "{info}". If you think you can answer the question yourself, then completely ignore the additional information, as if it was never provided. If you think that the question needs more information, and the provided information isn't enough, then tell the user.
    """
    llm_prompt = prompt_template.format(query=prompt,info=info)
    
    messages.append({"role":"user","content":llm_prompt})
    print_history([{"role":"user","content":prompt}])
    status_placeholder=st.empty()
    with status_placeholder:
        with st.status("Generating...") as status:
            response=client.chat_completion(messages,max_tokens=1024,temperature=0.1,seed=69)
    status_placeholder.empty()
    with st.chat_message("assistant"):
        # temperature of 0.1 for low randomness 
        # and maximum tokens set to 1024, to not cut-off the response in between
        response_text = client.chat_completion(messages,stream=False,max_tokens=1024,temperature=0.1).choices[0].message.content
        st.write(response_text)
    messages.pop()
    messages.append({"role":"user","content":prompt})    
    messages.append({"role":"assistant","content":response_text})
    return messages
