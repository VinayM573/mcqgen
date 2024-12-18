import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file
with open('C:\Complete_Content\All_Project\Test_For_EVERYTHING\langchain\Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

#Creating a title for the app
st.title("MCQ Creator Application with Langchain")

#Create a form using st.form
with st.form("user_inputs"):
    #file upload
    uploaded_files=st.file_uploader("Upload files")

    #input fields
    mcq_count=st.number_input("No. of MCQ", min_value=3,max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)

    #Quiz Tone
    tone=st.text_input("Complexity Level of Questions",max_chars=20, placeholder="Simple")

    #Add Button
    buttons=st.form_submit_button("Create MCQ")

    #Check if the button is clicked and all fields have input

    if buttons and uploaded_files is not None and mcq_count and subject and tone:
        with st.spinner("Loading"):
            try:
                text=read_file(uploaded_files)
                #count tokens and the cost of API
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )

                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    #Extract Quiz
                    quiz= response.get("quiz",None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.write(response)
