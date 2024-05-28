import streamlit as st
import requests
import uuid
import ast
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(page_title="3D-Model Buildr", layout="wide", initial_sidebar_state="auto", page_icon="favicon.ico")

st.title("3D-Model Buildr")

placeholder = st.empty()

if 'question_list' not in st.session_state:
    st.session_state.question_list = None
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

with placeholder:
    user_input = st.chat_input("What do you want to build now?")

    if user_input:
        response = requests.post("http://127.0.0.1:8000/new_request", json={"message": user_input})
        if response.ok:
            response_dict = response.json()
            st.session_state.question_list = ast.literal_eval(response_dict["data"])
            st.session_state.current_question_index = 0
            st.session_state.answers = []
            placeholder.empty()
        else:
            st.write("Error:", response.status_code, response.text)

# Function to handle answering the current question
def answer_question():
    current_answer = st.session_state[f'answer_{st.session_state.current_question_index}']
    st.session_state.answers.append(current_answer)
    st.session_state.current_question_index += 1

if st.session_state.question_list:
    current_index = st.session_state.current_question_index

    if current_index < len(st.session_state.question_list):
        st.write("Your Input:", user_input)
        current_question = st.session_state.question_list[current_index]
        st.write(f"Question {current_index + 1}: {current_question}")
        
        answer_key = f'answer_{current_index}'
        st.text_input("Answer:", key=answer_key)
        
        if st.button("Submit Answer"):
            if st.session_state[answer_key]:
                answer_question()
            else:
                st.write("Please provide an answer.")

    else:
        st.write("All questions answered. Thank you!")
        st.write("Your answers were:")
        for i, answer in enumerate(st.session_state.answers):
            st.write(f"Answer {i + 1}: {answer}")

else:
    st.write("Please enter something to build.")



file_path = r"samples\centipede.stl"
if st.sidebar.button("render model"):

    ## Initialize a plotter object
    plotter = pv.Plotter(window_size=[400,400])

    ## Load the mesh from file
    mesh = pv.read(file_path)


    ## Add mesh to the plotter
    plotter.add_mesh(mesh, cmap='bwr')

    ## Final touches
    plotter.view_isometric()
    plotter.background_color = 'white'

    ## Send to streamlit
    stpyvista(plotter, key="pv_cube")
