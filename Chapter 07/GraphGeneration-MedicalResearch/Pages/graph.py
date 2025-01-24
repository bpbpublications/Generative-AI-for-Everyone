import streamlit as st
from Pages.util_functions import *
import importlib
from pathlib import Path
from streamlit_ace import st_ace
import os
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
from neo4j import GraphDatabase
from extract_graph_comp import *
from query_res import *
from streamlit_feedback import streamlit_feedback
import shutil


file_name=st.session_state.chat_file_name

def reset():
    src = 'C:\\Users\\vaishnavi\\huggingface-repo\\GraphGeneration-MedicalResearch\\Pages\\tmp\\old'
    dest = 'C:\\Users\\vaishnavi\\huggingface-repo\\GraphGeneration-MedicalResearch\\Pages\\tmp\\new'
    shutil.copytree(src, dest, dirs_exist_ok=True)

    #keys = list(st.session_state.keys())
    #for key in keys:
        #st.session_state.pop(key)
def change_session_state():
    st.session_state.cnt = 1
    if os.path.exists("./Pages/tmp/new/"+option+'.py'):
                    os.remove("./Pages/tmp/new/"+option+'.py')
                    with open("./Pages/tmp/new/"+option +'.py', 'w') as the_file:
                        the_file.write("prompt = ''' "+ content + " '''")    
    article_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.article_prompt_tpl'), 'prompt')
    authors_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.authors_prompt_tpl'), 'prompt')
    cateogory_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.category_prompt_tpl'), 'prompt')
    keyword_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.keyword_prompt_tpl'), 'prompt')
    option_filter={'article_prompt_tpl':article_prompt_tpl,'authors_prompt_tpl':authors_prompt_tpl,
                'cateogory_prompt_tpl':cateogory_prompt_tpl,'keyword_prompt_tpl':keyword_prompt_tpl}
   

def generate_graph():
    
    article_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.article_prompt_tpl'), 'prompt')
    authors_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.authors_prompt_tpl'), 'prompt')
    cateogory_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.category_prompt_tpl'), 'prompt')
    keyword_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.keyword_prompt_tpl'), 'prompt')
    option={'article_prompt_tpl':article_prompt_tpl,'authors_prompt_tpl':authors_prompt_tpl,
                'cateogory_prompt_tpl':cateogory_prompt_tpl,'keyword_prompt_tpl':keyword_prompt_tpl}
                
   
    with st.expander('Steps-Processing'):
        with st.spinner('wait for it...'):
            st.write('1. Extraction of documents from pdf')
            doc=execute_query(file_name)

            st.write('2. Extraction of entities and relationships')
            results=extract_results(option,doc)

            st.write('3. Generation of cypher queries')
            ent_cyp, rel_cyp = generate_cypher('my_cv', [results])

            st.write('4. Generation of graph dataabase tables')
            neo4j_graph_creation(ent_cyp,rel_cyp)

        st.success('sucessfully graph table created')
        
    
st.title("Build graph out of Medical Journal Paper")
tab_tiles = ["prompt_templates","visualize_graph"]
tabs =st.tabs(tab_tiles)

with tabs[0]:

   
    article_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.article_prompt_tpl'), 'prompt')
    authors_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.authors_prompt_tpl'), 'prompt')
    category_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.category_prompt_tpl'), 'prompt')
    keyword_prompt_tpl=getattr(importlib.import_module('Pages.tmp.new.keyword_prompt_tpl'), 'prompt')
    option_filter={'article_prompt_tpl':article_prompt_tpl,'authors_prompt_tpl':authors_prompt_tpl,
                'category_prompt_tpl':category_prompt_tpl,'keyword_prompt_tpl':keyword_prompt_tpl}
   
    option = st.selectbox(
   "Select existing prompts",
   ("article_prompt_tpl","authors_prompt_tpl","category_prompt_tpl","keyword_prompt_tpl"),
   index=None,
   placeholder="Select prompt template...",
)
    st.button('Reset', on_click=reset)
       
    if option:
        if 'cnt' not in st.session_state:   
            reset()
            prompt=getattr(importlib.import_module('Pages.tmp.old.'+option), 'prompt')
            st.write('default prompts')

        elif 'cnt' in st.session_state: 
            prompt=getattr(importlib.import_module('Pages.tmp.new.'+ option), 'prompt')
            st.write('new prompts')

        # Spawn a new Ace editor
        content = st_ace(placeholder="Edity your prompt here!",value=prompt,auto_update= True)
        st.button("Edit -> Apply",on_click= change_session_state)
    
    b=st.button("Execute Prompt -> Response")
    if b:
        option_values = option_filter.get(option)
        option_dict={option:option_values}
        with st.expander('Steps-Processing'):
            with st.spinner('wait for it...'):
                st.write('1. Extraction of documents from pdf')
                st.write(file_name)
                doc=execute_query(file_name)

                st.write('2. Extraction of entities and relationships')
                st.write(option_dict)
                results=extract_results(option_dict,doc)
                st.write(results)
            st.success('Sucessfully generated')
    
                  

with tabs[1]:
    
    st.header ("visualize graph")
    st.button('Generate Graph',on_click= generate_graph)
    b=st.button('Visualize')
    if b:
        driver = GraphDatabase.driver(st.secrets['url'], auth= (st.secrets['username'], st.secrets['password']))
        G = nx.Graph()
        neo4j_nx(driver,G)
        net = Network(notebook=True, height="750px", width="100%")
        net.from_nx(G)
        physics=st.checkbox('add physics interactivity?')
        if physics:
            net.show_buttons(filter_=['physics'])
        net.show('property_graph.html')
        HtmlFile = open("property_graph.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 900,width=1200)
        