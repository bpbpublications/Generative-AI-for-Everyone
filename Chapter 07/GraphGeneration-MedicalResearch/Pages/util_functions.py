from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
import pinecone
import os
from langchain_community.vectorstores import Pinecone
import hashlib



def  load_pdf(file) : 
        loader = PyPDFLoader(file)
        return (loader)

def chunk_data(loader,file_name):
        text_splitter = CharacterTextSplitter( separator="\n", chunk_size=500,chunk_overlap=0)
        chunks = loader.load_and_split(text_splitter= text_splitter)
        docs = text_splitter.split_documents(chunks)
        for idx, text in enumerate(docs):
                  docs[idx].metadata['file_name'] = file_name

        return docs

def create_embeddings_load_data():
        embeddings=OpenAIEmbeddings()
        return (embeddings)
	
def pinecone_embd(index,embeddings, docs,file_name):
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV"),  # next to api key in console
        )
        index_name = index
        print(index_name)
        print(os.getenv("PINECONE_API_KEY"))
        if index_name not in pinecone.list_indexes():
        # we create a new index
                pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
        
        index = Pinecone.from_documents(docs, embeddings,index_name =index_name)
        return index
def neo4j_nx(driver,G) :
    query = """ MATCH (n)-[r]->(m) RETURN n,r,m , labels(n) ,labels(m)  """
    try:
        with driver.session() as session:
            result = session.run(query)
            data     = result.data()
            #print(data[0])
            i=0
            for row in data:
                # Extract the nodes and relationships from the query result

                node1 = row['n']
                rel = row['r']
                node2 = row['m']
                node1_label = row['labels(n)']
                node2_label = row['labels(m)']
                print(node1 ['id'],node2 ['id'] , rel[1], node1_label [0], node2_label [0])
                print(i)
                i=i+1

                # Add nodes to the graph
                G.add_node(node1['id'], label=node1_label[0]+':'+node1['id'] , properties=node1)
                G.add_node(node2['id'], label=node2_label[0]+':'+node2['id'],properties=node2)
            
                # Add edges to the graph
                G.add_edge(node1['id'], node2['id'], relationship=rel[1])
    finally:
        driver.close()



def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


