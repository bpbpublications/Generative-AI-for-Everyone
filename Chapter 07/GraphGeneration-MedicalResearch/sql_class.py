
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
import sqlalchemy
import uuid



Base=declarative_base()
     
class Message(Base):
    
        #table class
        __tablename__ = 'karthik_chat_history'
        id: str = Column(String(), primary_key=True, default=lambda: str(uuid.uuid4()))
        pdf_id = Column(String)
        pdf_name = Column(String)
        conv_id = Column(String)
        conv_role = Column(String)
        conv_message = Column(String)
        created_on = Column(DateTime,server_default=sqlalchemy.func.now())


        def as_dict(self):
            return {"pdf_id": self.pdf_id,"pdf_name":self.pdf_name, "conv_id": self.conv_id, "conv_role": self.conv_role,"conv_message":self.conv_message}
        
        def as_lc_message(self) -> HumanMessage | AIMessage | SystemMessage:
            if self.conv_role == "human":
                return HumanMessage(content=self.conv_message)
            elif self.conv_role == "ai":
                return AIMessage(content=self.conv_message)
            elif self.conv_role == "system":
                return SystemMessage(content=self.conv_message)
            else:
                raise Exception(f"Unknown message role: {self.conv_role}")

db_uri = 'sqlite:///C:\Program Files\sqllite\chat_history.db'
engine = create_engine(db_uri)
Base.metadata.create_all(engine)