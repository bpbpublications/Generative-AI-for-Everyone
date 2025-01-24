import streamlit as st
from dotenv import load_dotenv
from utils import generate_script

load_dotenv()
st.title(' Chat with your excel')
st.image("pexels-junior-teixeira-2047905.jpg", width=500,caption='Analyse your csv files')
st.header(' upload your excel here')
file=st.file_uploader("upload your csv", type=["csv"] ,key ="uploaded_file")
#file=st.session_state["uploaded_file"]

query = st.text_area("Enter your query")
submit = st.button('Generate response for me')

if submit:
    ans ,df = generate_script(file,query)
    st.write(ans)
    with st.expander('show me'):
        st.write(df)

        
