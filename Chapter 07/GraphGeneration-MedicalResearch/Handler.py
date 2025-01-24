from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
import streamlit as st

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        st.write("\n\n===========sending messages=============\n\n")
        
        
        
        