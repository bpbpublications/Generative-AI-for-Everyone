import streamlit as st
from Pages.util_functions import *
from dotenv import load_dotenv
import base64
import tempfile
from pathlib import Path

# Pinecone index
index =st.secrets['index']


# function to internally preview the pdf
def show_pdf(file_path):
    st.write(file_path)
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    load_dotenv(override=True)
    st.set_page_config(page_title="dump PDF to pinecone -vector store")
    if 'file_count' in st.session_state:
        st.write('No of files already process -',st.session_state.file_count)
        upload_file=st.session_state.upload_file

    else:
        st.session_state.file_count = 0
        st.session_state.upload_file = []
        st.session_state.chat_file_name = []
        st.session_state.upload_file_hash = {}



    st.write('your latest upload',st.session_state.chat_file_name)
    st.write('your uploaded files - ',st.session_state.upload_file)
    st.title("please upload your files......")

    file=st.file_uploader('only PDF file',type =['pdf'])


    if file is not None :
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            file_hash = hash_file(fp)
            st.write(file_hash)
            fp.write_bytes(file.getvalue())
            st.write(show_pdf(tmp_file.name))        
            st.session_state['chat_file_name'] = file.name
        b=st.button('process')
        if b:
            with st.spinner('wait for it...'):
                loader=load_pdf(tmp_file.name)
                st.write('1. Reading pdf done')
                doc_chunks=chunk_data(loader,st.session_state.chat_file_name)
                st.write('2. Splitting data into chunks done')
                doc_embeddings=create_embeddings_load_data()
                st.write('3. Creating embedding done')
                pinecone_embd(index,doc_embeddings, doc_chunks,file.name)
                st.session_state.file_count+=1
                upload_file.append(file.name)
                st.session_state.upload_file_hash[file.name]=file_hash
                st.session_state['upload_file']=upload_file

            st.success('Sucessfully pushed data to pinecone')

if __name__ == '__main__' :
    main()
