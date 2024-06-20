import streamlit as st

def print_history(chat_history):
    for i in chat_history:
        if i["role"]=="user":
            with st.chat_message("user"):
                st.write(i["content"])
        elif i["role"]=="assistant":
            with st.chat_message("assistant"):
                st.write(i["content"])

def generate_info(prompt):
    info=""
    return info

def generate_response(messages,prompt,client,info="",tokenizer=""):
    prompt_template="""
    Please answer the following query, "{query}", only based on your previous interactions 
    with me, and the following information, "{info}". If the information seems to be insufficient, then
     tell that, instead of generating any arbitrary result
    """
    new_prompt = prompt_template.format(query=prompt,info=info)
    # use the below new prompt for RAG implementation
    # messages.append({"role":"user","content":new_prompt})
    messages.append({"role":"user","content":prompt})
    print_history(messages)
    status_placeholder=st.empty()
    with status_placeholder:
        with st.status("Generating...") as status:
            response=client.chat_completion(messages,max_tokens=1024,temperature=0.1,seed=69)
    status_placeholder.empty()
    response_text = response.choices[0].message.content
    messages.append({"role":"assistant","content":response_text})
    print_history([messages[-1]])