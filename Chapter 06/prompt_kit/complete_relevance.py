import streamlit as st
import vertexai
from google.cloud import aiplatform
from google.oauth2 import service_account
from string import Template
from vertexai.preview.language_models import TextGenerationModel


def llm_eval_prompt(question , response):

    project_id = st.secrets['project_id']
    location = st.secrets['location']
    key_path= st.secrets['key_path']


    credentials =  service_account.Credentials.from_service_account_file(key_path)
    vertexai.init(project=project_id , location = location , credentials = credentials)
    model = TextGenerationModel.from_pretrained("text-bison")

    prompt = Template(''' You are LLM evaluator. You must evaluate Logical consistency and Topic relevance of the response .
    I will provide you with a question and an response as below. 
    Question:$question
    Answer: $response
    Metrics:
    - Logical Consistency: Is the resposne is logical and donot contradict with any parts of question ?
    - Relevance: is the response is relevant to the  question and adress all parts of question ?
    JUST GIVE THE SCORES BETWEEN 0 AND 5 WHERE 0 BEING LOWEST non logical,non relevant
    AND 1 BEING HIGHEST FOR METRIC for highly logical and highly relevant
    DO NOT ELABORATE
    ''')
    prompt = prompt.substitute(question=question, response=response)
    #print(prompt)

    response = model.predict(prompt,temperature =0 ,max_output_tokens=1024, top_k=4, top_p=0.8)
    response = response.text

    return response


