import sqlite3
from pydantic.v1 import BaseModel, Field
from typing import List
from langchain.tools import Tool
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
_ = load_dotenv(find_dotenv())

conn = sqlite3.connect("my_db.db") # Establish DB connection
def run_sqlite_query(query): # Function to execute sql query
	c = conn.cursor()
	c.execute(query)
	return c.fetchall()
	
# Creation of Tool class
class RunQueryArgsSchema(BaseModel): 
	query: str

run_query_tool = Tool.from_function(
	name="run_sqlite_query",
	description="Run a sqlite query.",
	func=run_sqlite_query,
	args_schema=RunQueryArgsSchema
	)

model = ChatOpenAI(temperature=0)
tables ="student"
prompt = ChatPromptTemplate(
	messages=[
	    SystemMessage(content=(
	        "You are an AI that has access to a SQLite database.\n"
	        f"The database has tables of: {tables}\n"
	        "Do not make any assumptions about what tables exist "
	        "or what columns exist. Instead, use the 'describe_tables' function"
	    )),
	    HumanMessagePromptTemplate.from_template("{input}"),
	    MessagesPlaceholder(variable_name="agent_scratchpad")
	    ]
	)
	
tools = [
	run_query_tool,
	]
	
agent = OpenAIFunctionsAgent(
	llm=model,
	prompt=prompt,
	tools=tools
	)
agent_executor = AgentExecutor(
	agent=agent,
	verbose=True,
	tools=tools
	)
agent_executor("Get me total number of students")
	# agent_executor("how many users are there?")
