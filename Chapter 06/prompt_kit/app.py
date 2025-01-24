import streamlit as st
import importlib
from pathlib import Path
from streamlit_ace import st_ace
import os
import streamlit.components.v1 as components
from streamlit_feedback import streamlit_feedback
from get_prompt import *
from exec_prompt import *
from dotenv import load_dotenv,find_dotenv
import time
from streamlit_feedback import streamlit_feedback
from complete_relevance import llm_eval_prompt
from language_check import check_grammar
from bias_check import bias_identify
import st_pop_up_component as sp
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
import datetime

# Hyper Parameters for prompt template
st.sidebar.title("Set LLM Hyperparameter")
temperature =st.sidebar.slider("temperature", 0.0, 1.0, 0.1,key='temperature')
model = st.sidebar.radio("Model", ["gpt-3.5-turbo-1106","gpt-3.5-turbo"],key='modelname')

# Default prompt scores initialized - Took one metric parameter of latency to verify
if "latency" not in st.session_state:
    st.session_state["latency"]=0  
    st.session_state["cost"]=0
    st.session_state["grammar"]=0
    st.session_state["comp_rel_res"]=0
    st.session_state["score"]=0
    st.session_state["feedback_score"]=0
    st.session_state["res"]=0


ctx = get_script_run_ctx()
session_id=ctx.session_id
key = 'feedback-'+ session_id # Human feedback key for this session

# Initializes session variable

if 'template_name' not in st.session_state:
    st.session_state['template_name']='initial' # default template name
if 'option' not in st.session_state:
    st.session_state['option']='initial' # Prompt option from drop down
if 'key' not in st.session_state:
    st.session_state['key']=key # Initialize feedback key
if st.session_state.key not in st.session_state:
        st.session_state[st.session_state.key]={"type": "faces","score": "😞","text": ''} #Default feedback values
def main():
    # Api keys for OpenAI 
    load_dotenv(find_dotenv(usecwd=True)) # Loading Environment varialbes

st.title("Prompt Playground")
tab_tiles = ["New Prompt","Execute Prompts",]
tabs =st.tabs(tab_tiles) 
     
# Creation of new prompt base template
# This will be empty template with  purpose and any business objective
# It remain unedited
with tabs[0]:
    new_prompt_name=st.text_input('Enter Prompt Name')
    new_prompt_meta=st.text_input('Enter Prompt Purpose')
    b1=st.button("New Prompt")
    if b1:
        if new_prompt_name:
            if os.path.exists("./new/"+new_prompt_name+'_base.py'):
                output =sp.st_custom_pop_up("Name exist",key="first-key")
                st.write(output)      
            else:
                with open("./new/"+new_prompt_name +'_base.py', 'w') as file:
                    prompt_details = "prompt = ''' "+ " '''\n" #Blank template creation 
                    meta = "metadata = ''' "+ new_prompt_meta + " ''' \n"
                    file.writelines([prompt_details,meta])
with tabs[1]:
    
    def on_edit():
        #Timestamp extraction
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        ts_str=str(ts).replace(".","_")
        
        #Unique template version with timestamp
        template_name ="./new/"+st.session_state.option +str(ts_str)+'.py'
        st.session_state['template_name']=template_name
        
        #Writing prompt template file with metadata 
        with open(template_name, 'w') as file:
            prompt_details= "prompt = ''' "+ content + " '''\n"
            latency_details = "latency = ''' "+str(st.session_state.latency)+ " '''\n"
            cost_details = "cost = ''' "+str(st.session_state.cost)+ " '''\n"
            bias_details = "bias = ''' "+str(st.session_state.score)+ " '''\n"
            grammar_details = "grammar = ''' "+str(st.session_state.grammar)+ " '''\n"
            comp_rel_res_details = "comp_rel_res = ''' "+str(st.session_state.comp_rel_res)+ " '''\n"
            feedback_score_details = "feedback_score = ''' "+str(st.session_state.feedback_score)+ " '''\n"
            response_details = "response = ''' "+ str(st.session_state.res) + " '''\n"
            temperature_details = "temperature = ''' "+ str(st.session_state.temperature) + " '''\n"
            model_name_details = "modelname = ''' "+ str(st.session_state.modelname) + " '''\n"
            session_details = "sessionid = ''' "+str(session_id)+ " '''\n"
            time_details = "time = ''' "+str(ts)+ " '''\n"

            file.writelines([prompt_details,latency_details,cost_details,bias_details,grammar_details, comp_rel_res_details,feedback_score_details,response_details,temperature_details, model_name_details,session_details,time_details,])    

            return template_name
        
    prompt_names=list_prompt()
    option_filter={}
    print(prompt_names)
    for i in prompt_names:
         attr_path=str('new.'+i)
         option_filter[i] = getattr(importlib.import_module(attr_path), 'prompt')

    option = st.selectbox("Select existing prompts",prompt_names,index=None,placeholder="Select prompt template...",key = "select")
    st.session_state['option']=option
    if option:
        content = st_ace(placeholder="Edity your prompt here!",value=option_filter[option],auto_update= True)
        st.button("Edit -> Apply",on_click= on_edit)
        st.session_state['template_name']="./new/"+str(option)+'.py'

 
    b=st.button("Execute Prompt -> Response")
    if b:
        option_values = option_filter.get(option)
        option_dict={option:option_values}
        with st.expander('Steps-Processing'):
            with st.spinner('wait for it...'):
                st.write('Generating the response')
                system_message='you are an Infrastructure expert'
                start_time = time.time()
                res,cost=response(option_values,temperature, model,system_message)
                st.session_state.cost=cost
                end_time = time.time()
                latency = (end_time - start_time) 
                st.session_state.latency=latency
                st.write(res['text'])
                st.session_state['res']=res['text']
            st.success("Success!")
            
        comp_rel_res=llm_eval_prompt(option_values , res)
        grammar=check_grammar(res['text'])
        score=bias_identify(res['text'])
        st.session_state['score']=score
        st.session_state['grammar']=grammar
        st.session_state['comp_rel_res']=comp_rel_res
    b=st.button('feedback')
    st.session_state['key']=key
    
    if b:
        streamlit_feedback(feedback_type="faces",optional_text_label='give your feedback',key=key)
    
    helpful_feedback=st.session_state[st.session_state.key]
    score_mappings = {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25 , "😞": 0}
    feedback_score=score_mappings.get(helpful_feedback["score"])
    st.session_state['feedback_score'] = feedback_score
    st.write('Human feedback:' ,st.session_state.feedback_score,'Latency: ',st.session_state.latency,'Cost:heavy_dollar_sign: ',st.session_state.cost,'Bias: ',st.session_state.score,'Grammar error: ',st.session_state.grammar,st.session_state.comp_rel_res)
    if st.session_state.feedback_score:
        os.remove(st.session_state.template_name)
        on_edit()

