
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)

from langchain.pydantic_v1 import BaseModel
from langchain.callbacks.tracers.schemas import Run
from langchain.schema.messages import BaseMessage
from langchain.schema.runnable.config import RunnableConfig
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
from sql_actions import (sql_insert,sql_retrive)

class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conv_id: str
    chat_file_hash:str
    chat_file_name:str

    @property
    def messages(self):
        return sql_retrive(self.chat_file_hash,self.conv_id)
    
    def add_message(self, message):
        return sql_insert(
            pdf_id= self.chat_file_hash,
            pdf_name= self.chat_file_name,
            conv_id=self.conv_id,
            conv_role=message.type,
            conv_message=message.content
        )

    def clear(self):
        pass

def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(
            conv_id=chat_args.conv_id,
            chat_file_hash=chat_args.chat_file_hash,
            chat_file_name=chat_args.chat_file_name
        ),
        return_messages=True,
        memory_key="chat_history",
        input_key="question",
        #output_key="answer"
    )