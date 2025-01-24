from langchain_openai import ChatOpenAI
from langchain.llms import OpenAI
from cost import cost_decorator
import os
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain.chains import LLMChain
api_key = os.environ["OPENAI_API_KEY"]

@cost_decorator
def response(prompt,temperature, model,system_message):
    chat_model = ChatOpenAI(api_key=api_key,temperature=temperature, model_name=model, n=3)
    system_template = SystemMessagePromptTemplate.from_template(system_message)
    user_template = HumanMessagePromptTemplate.from_template("{prompt}")
    template = ChatPromptTemplate.from_messages([system_template, user_template])
    chain = LLMChain(llm=chat_model, prompt=template)
    response=chain.invoke({"prompt": prompt})
    print(response)
    return(response)




