import streamlit as st
import main as mn
import textwrap

import time

st.title("Question generation")

with st.sidebar.form(key='my_form'):
    youtube_url = st.text_area(
        label="What is the YouTube video URL?", max_chars=150)

    submit_button = st.form_submit_button(label='Submit')

    

if youtube_url:
    if youtube_url == "Error":
        st.subheader("Questions testing knowledge about the video")
        st.text("Please make sure the youtube url is correct and have a corresponding transcripts.")
    else:
        with st.spinner("Please wait, generating questions...It usually takes upto 20 to 40 seconds"):
            questions = mn.generate_question(youtube_url)

        st.subheader("Questions testing knowledge about the video")
        for i, question in enumerate(questions, 1):
            st.text(f"{i}. {textwrap.fill(question, width=85)}")




