# Question and Answer on a Given Topic 
# Topic file is uploaded as a Text

import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 LMS Question & Answer 🎈")
st.write("Lecturer to Upload a document. "
    "Students can be tested using Autogenerated Q&A")

# Create a checkbox with the label "Agile Approach"
if st.checkbox("Agile Approach"):
    # Display a popup-like message
    st.warning("This software is being developed using an Agile approach. Development will proceed in stages. The model answer will be displayed only after grading in future versions.")
    
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Define a global variable
query = "Create a Question with a model answer"
document = None  # Initially set to None to indicate no document is uploaded
uploaded_file = None  # Define uploaded_file globally

#parse
# Function to parse the input string
import re
import json

def parse_chatgpt_response(response):
    # Extract the main content from the nested structure
    match = re.search(r'content="(.+?)", refusal=None', response, re.DOTALL)
    if not match:
        raise ValueError("Content not found in the response.")
    
    content = match.group(1)
    
    # Extract the question and model answer
    question_match = re.search(r'\*\*Question:\*\*\s*(.+?)\n\n', content, re.DOTALL)
    answer_match = re.search(r'\*\*Model Answer:\*\*\s*(.+)', content, re.DOTALL)
    
    if not question_match or not answer_match:
        raise ValueError("Could not find the question or model answer in the content.")
    
    # Clean up and return the extracted values
    question = question_match.group(1).strip()
    answer = answer_match.group(1).strip()
    return question, answer
#end of parsing




# Define the function to be called when the button is clicked
def AskQn():
    # Placeholder for future implementation
    global document, query  # Access the global variables
    # Conditionally avoid redundant parsing of the file
    if not document:
        document = uploaded_file.read().decode()
    messages =  [{"role": "user",
                 "content": f"Here's a document: {document} \n\n---\n\n {query}",}
                ]
                # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=False,)
    try:
        question, answer = parse_chatgpt_response(response)
        st.write("QQ:")
        st.write(question)
        st.write("\nAA:")
        st.write(answer)
    except ValueError as e:
        st.write(f"Error: {e}" )
    return  # Exits the function
#function ended


# openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = st.secrets["openai"]["secret_key"]
client = OpenAI(api_key=openai_api_key)

if not client:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Streamlit app layout
    st.title("Interactive Q&A Generator")
    # Add a button that calls the AskQn() function

        
    # OpenAI client already created.
    # client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )
    if uploaded_file:
        if st.button("Ask Question"):
            AskQn()
    
    
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
            messages =  [{"role": "user",
                        "content": f"Here's a document: {document} \n\n---\n\n {question}",}
                        ]
    
            # Generate an answer using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
            )
    
            # Stream the response to the app using `st.write_stream`.
            st.write_stream(stream)
