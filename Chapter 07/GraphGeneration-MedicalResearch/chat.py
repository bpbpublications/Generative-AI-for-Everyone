from dotenv import load_dotenv
import streamlit as st
from util_chat import *
from memory import build_memory
from streamlit.runtime.scriptrunner import get_script_run_ctx
from chat_arg import ChatArgs


pine_index =st.secrets['index']

def get_session_id() -> str:
    ctx = get_script_run_ctx()
    if ctx is None:
        raise Exception("Failed to get the thread context")

    return ctx.session_id

def main():
    load_dotenv()

def chck_name(key_name):
        x = st.session_state[key_name]
        if x:
            st.session_state.chat_file_name = key_name
            st.session_state.chat_file_hash= st.session_state.upload_file_hash[key_name]
            st.session_state.conv_id= get_session_id()
            st.write(st.session_state.conv_id)

        else:
            st.session_state.chat_file_name = ''
            st.session_state.chat_file_hash= ''
            st.session_state.conv_id= get_session_id()
         


st.header("Chat with your document")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'file_count' not in st.session_state:
    st.write('upload your pdf using app')
else:
    st.write('chat with',st.session_state.file_count)
    
    with st.expander('your uploaded files'):
        for i in st.session_state.upload_file:
            if i==st.session_state.chat_file_name:
                st.checkbox(f''':green[{i}]''',key=i,help= '(Last selected)',on_change=chck_name, args=(i,))
            else:
                st.checkbox(i,key=i,on_change=chck_name, args=(i,))
        


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["persona"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your query here"):
    # Add user message to chat history
    st.session_state.messages.append({"persona": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("human"):
        st.markdown(prompt)

    # create embedding instance
    user_query_embed= create_embeddings_query_data()
    # function to pull index data from pine cone
    index_extract=pinecone_embd_extract(pine_index,user_query_embed,st.session_state.chat_file_name)

    # fetch relevant documents from vector store
    rag_embed=similar_search(index_extract,prompt,st.session_state.chat_file_name)
    #for result in rag_embed:
        #st.write(result[0])
        #st.write(result[1])

        # fine tuned response from LLM
    conv_id = st.session_state.conv_id
    chat_file_hash= st.session_state.chat_file_hash
    chat_file_name= st.session_state.chat_file_name
    chat_args=ChatArgs(conv_id= conv_id,chat_file_name=chat_file_name,chat_file_hash=chat_file_hash,streaming=0)
    memory=build_memory(chat_args)
    response = llm_response(rag_embed,prompt,memory)

    with st.chat_message("ai"):
        message_placeholder = st.empty()
        assistant_response =response

        message_placeholder.markdown(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"persona": "assistant", "content": assistant_response})
if __name__ == '__main__' :
    main()