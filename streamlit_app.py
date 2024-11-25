# Question and Answer on a Given Topic 
# Topic file is uploaded as a Text

import streamlit as st
from openai import OpenAI
import re
import json

# Show title and description.
st.title("📄 LMS Question & Answer 🎈")
st.write("Lecturer to Upload a document. "
    "Students can be tested using Autogenerated Q&A")

# Create a checkbox with the label "Agile Approach"
if st.checkbox("Agile Approach"):
    # Display a popup-like message
    st.warning("This software is being developed using an Agile approach. Development will proceed in stages. The model answer will be displayed only after grading in future versions.")
hide_ans =0
if st.checkbox("Agile Approach"):
    hide_ans =1
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

# Define a global variable
query = "Create a random Question with an Answer"
document = None  # Initially set to None to indicate no document is uploaded
uploaded_file = None  # Define uploaded_file globally

#parse
# Function to parse the input string

def extract_question_and_answer(generated_content):
    """
    Extracts the question and answer from a given string based on the keywords 'Question:' and 'Answer:'.
    
    Parameters:
        generated_content (str): The input string containing the question and answer.
        
    Returns:
        tuple: A tuple containing the question (qn) and the answer (ans).
    """
    try:
        # Split the content into parts based on the keywords
        question_part = generated_content.split("Question:", 1)[-1]
        answer_part = question_part.split("Answer:", 1)
        
        # Extract the question and answer
        qn = answer_part[0].strip()  # Question part
        ans = answer_part[1].strip() if len(answer_part) > 1 else ""  # Answer part
        # Remove '**' from the question and answer
        qn = qn.replace("**", "")
        ans = ans.replace("**", "")
        return qn, ans
    except Exception as e:
        raise ValueError(f"Error parsing content: {e}")
#end of parsing


# Define the function to be called when the button is clicked
def AskQn():
    # Placeholder for future implementation
    global document, query  # Access the global variables
    # Conditionally avoid redundant parsing of the file
    if not document:
        document = uploaded_file.read().decode()

    messages = [
        {"role": "system", "content": f"Keep the scope of answering strictly within the context of the document: {document}."},
        {"role": "system", "content": f"If a question is not within the scope of the document, respond with 'I am not sure'."},
        {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {query}"}
    ]
    
                # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=False)
    generated_content = stream.choices[0].message.content
    
    #st.write(generated_content)
    q,a =extract_question_and_answer(generated_content)
    st.write(q)
    if(not hide_ans):st.write(a)  
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
