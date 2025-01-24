from langchain_community.embeddings import OpenAIEmbeddings
import pinecone
import os
from Handler import ChatModelStartHandler
from langchain_community.vectorstores import Pinecone
from langchain_community.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.docstore.document import Document
handler = ChatModelStartHandler()

def create_embeddings_query_data():
        embeddings=OpenAIEmbeddings()
        return (embeddings)

def pinecone_embd_extract(pine_index,embeddings,file_name):
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV"),  # next to api key in console
        )
        index_extract = Pinecone.from_existing_index(index_name = pine_index,embedding=embeddings)
        return index_extract

def similar_search(index, query ,file_name,k=3):
        
        similar_docs= index.similarity_search_with_score(query, k=k ,filter={"file_name":file_name})
        return similar_docs

def llm_response(rag_embed,user_query,memory):
        chain = load_qa_chain(OpenAI(),chain_type="stuff", memory=memory,callbacks=[handler])
        rag_embed = [Document(page_content=str(result[0]), metadata={"score": str(result[1])}) 
                     for result in rag_embed]

        with get_openai_callback() as cb:
                response = chain({"input_documents":rag_embed, "question":user_query},return_only_outputs=True)
        return response

def llm_response_graph(rag_embed,user_query):
        chain = load_qa_chain(OpenAI(),chain_type="stuff", callbacks=[handler])
        rag_embed = [Document(page_content=str(result[0]), metadata={"score": str(result[1])}) for result in rag_embed]

        with get_openai_callback() as cb:
                response = chain({"input_documents":rag_embed, "question":user_query},return_only_outputs=True)
        return response