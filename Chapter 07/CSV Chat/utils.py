from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd 

def generate_script(file , query ):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')

    df = pd.read_table(file,sep=",",header=1)
    agent = create_pandas_dataframe_agent(llm,df,verbose=True)
    answer = agent.run(query)

    return answer,df
  
   