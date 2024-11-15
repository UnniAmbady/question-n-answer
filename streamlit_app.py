# Question and Answer on a Given Topic 
# Topic file is uploaded as a Text

import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 LMS Question & Answer 🎈")
st.write("Lecturer to Upload a document "
    "Students can be tested using Autogenerated Q&A")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = st.secrets["openai"]["secret_key"]
client = OpenAI(api_key=openai_api_key)

if not client:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # OpenAI client already created.
    # client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
   
    #question = st.text_area(
    #    "Now ask a question about the document!",
    #    placeholder="Can you give me a short summary?",
    #    disabled=not uploaded_file,)
    if not uploaded_file:
        st.write("Upload a file before you can ask a Question.")
    if uploaded_file:
        if question := st.chat_input("What is up?"):
            # Process the uploaded file and question.
            document = uploaded_file.read().decode()
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
            ]
    
            # Generate an answer using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
            )
    
            # Stream the response to the app using `st.write_stream`.
            st.write_stream(stream)
