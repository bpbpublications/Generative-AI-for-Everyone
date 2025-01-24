from dotenv import load_dotenv
import streamlit as st
import sys
import os
from os.path import dirname
import util_chat
import time
sys.path.append(dirname(dirname(dirname(__file__))))
pine_index = st.secrets['index']


def execute_query(file_name):
    load_dotenv()
    article_user_query = "extract the article name , type of article, DOI, publication data, summarize abstract of article in 20 words  and summarize conclusion of article in 10 words"
    reference_user_query= "extract article names with all author details in References section and list out in format {Reference: }"
    authors_user_query = "extract the journal author names and corresponding author details with author affliation details "
    category_user_query = "extract the categories in the article mentioned in the categories section"
    keywords_user_query = "extract all the keywords used in this article mentioned in the Keywords section  "

    query_list={'authors_prompt_tpl':authors_user_query,'reference_prompt_tpl':reference_user_query,'category_prompt_tpl':category_user_query,'article_prompt_tpl':article_user_query,'keyword_prompt_tpl':keywords_user_query}
    doc={}

    for user_query in query_list:

        # create embedding instance
        user_query_embed= util_chat.create_embeddings_query_data()
        # function to pull index data from pine cone
        index_extract=util_chat.pinecone_embd_extract(pine_index,user_query_embed,file_name)

        # fetch relevant documents from vector store
        rag_embed=util_chat.similar_search(index_extract,query_list[user_query],file_name)

        # fine tuned response from LLM
        response = util_chat.llm_response_graph(rag_embed,query_list[user_query])
        response=str(response)
        doc[user_query] = response
        time.sleep(2)
    return doc
