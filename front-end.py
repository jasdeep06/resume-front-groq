import streamlit as st
import random
import time
import requests
import os


# # Streamed response emulator
# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

def make_api_call(query):
    response = requests.get("https://resume-grok.translatetracks.com/query", params={"query": query})
    # response = requests.get("http://localhost:8000/query", params={"query": query})
    return response.json()["response"], response.json()["images"]





st.title("Resume RAG on Llama3-80b")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"""
                                  This is a comprehensive RAG built upon top of Jasdeep Singh Chhabra's resume.
                                  The data sources include his resume, 8 multimodal blog post written by him on his blog https://jasdeep06.github.io/,
                                  2 Multimodal reports written by him detailing his technical experience in the two startups he cofounded namely
                                  Vinglabs(https://alpla.netlify.app) and TranslateTracks(https://translatetracks.netlify.app).
                                  Few things that should be kept in mind - 
                                  1. Due to resource contraints, each query is independent and does not take into account the context of the previous queries.
                                  2. Comprehensive questions that involve pulling data from multiple indexes may take longer to respond.

                                  This is running on llama-3-80b deployed on groq for faster inference.
                                  What do you want to know about Jasdeep?
                                  Hint: You can ask any question related to Jasdeep's career. Example - "Does Jasdeep has experience in SQL?","Can you give examples where Jasdeep has used SQL?"
                                  or more specific to projects like "What is the stack used in TranslateTracks?" etc. 
                                  """, "images":[]}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # st.markdown("")
        st.markdown(message["content"])
        if message["role"] == "assistant":
            for image in message["images"]:
                st.image(os.path.join("all_images",image))

# Accept user input
prompt = st.chat_input("What is up?")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # response = st.write_stream(response_generator())
        with st.spinner("Thinking..."):
            response,images = make_api_call(prompt)
        st.markdown(response)
        for image in images:
            st.image(os.path.join("all_images",image))

        # st.image('8351cf45-92df-4157-be3f-b6c8535bcae2-img_p1_1.png')
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "images":images})