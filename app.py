import streamlit as st
import requests
import ast
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(page_title="3D-Model Buildr", layout="wide", initial_sidebar_state="auto", page_icon="favicon.ico")

# Function to create message dictionary
def message(role, content):
    return {
        "role": role,
        "content": content
    }

st.title("3D-Model Buildr")

# Function to handle answering the current question
def answer_question(answer):
    current_index = st.session_state.current_question_index
    st.session_state.answers.append(answer)
    st.session_state.current_question_index += 1

# Initialize session state variables if they do not exist
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'question_list' not in st.session_state:
    st.session_state.question_list = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Placeholder for the user input form
form_placeholder = st.empty()

# User input form
if not st.session_state.form_submitted:
    with form_placeholder.form(key="user_input_form"):
        user_input = st.text_input("What do you want to build now?", st.session_state.user_input)
        submit_button = st.form_submit_button(label="Submit")

    # Handle form submission
    if submit_button and user_input:
        st.session_state.user_input = user_input
        response = requests.post("http://127.0.0.1:8000/new_request", json={"message": user_input})
        if response.ok:
            response_dict = response.json()
            st.session_state.question_list = ast.literal_eval(response_dict["data"])
            st.session_state.current_question_index = 0
            st.session_state.answers = []
            st.session_state.form_submitted = True

            # Prompting
            st.session_state.messages.append(message("user", user_input))
            st.session_state.messages.append(message("assistant", "I'd be happy to help you with building a 3D model. But before that, can you answer the following questions about the model?"))
            st.session_state.messages.append(message("user", "Sure, please proceed."))
            form_placeholder.empty()

# Display questions and answers
if st.session_state.user_input and st.session_state.form_submitted:
    current_index = st.session_state.current_question_index
    if current_index < len(st.session_state.question_list):
        st.text(f"Your Input: {st.session_state.user_input}")
        current_question = st.session_state.question_list[current_index]
        # st.write(f"Question {current_index + 1}: {current_question}")

        answer_key = f'answer_{current_index}'

        with st.form(key="answer_form"):
            st.text(f"Question {current_index + 1}: {current_question}")
            answer = st.text_input("Answer:", key=answer_key)
            answer_submit_button = st.form_submit_button(label="Submit Answer")

        if answer_submit_button:
            if answer:
                answer_question(answer)
            if answer != "":
                st.session_state.messages.append(message("assistant", current_question))
                st.session_state.messages.append(message("user", answer))
                
    else:
        st.write("Thank you!")
        st.write(st.session_state.messages)
        response = requests.post("http://127.0.0.1:8000/post_messages", json=st.session_state.messages)
        print(response.json())
else:
    st.write("Please enter what you want to build.")
