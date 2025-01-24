from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from sql_class import Message
import os

def sql_insert(pdf_id,pdf_name,conv_id,conv_role,conv_message):
            db_uri = 'sqlite:///C:\Program Files\sqllite\chat_history.db'
            engine = create_engine(db_uri)
            Session = sessionmaker(bind = engine)
            session = Session()
            user_id = os.getenv("user_id")

              
            print(inspect(engine).get_table_names())

            session.add(Message(pdf_id=pdf_id,pdf_name=pdf_name,conv_id=conv_id,conv_role=conv_role,conv_message=conv_message))

            session.commit()
            session.close()

def sql_retrive(pdf_id,conv_id)-> AIMessage | HumanMessage | SystemMessage:
            db_uri = 'sqlite:///C:\Program Files\sqllite\chat_history.db'
            engine = create_engine(db_uri)

            #print(inspect(engine).get_table_names())
            Session = sessionmaker(bind = engine)
            session = Session()

            messages = (
                session.query(Message)
                .filter_by(pdf_id=pdf_id,conv_id=conv_id)
                .order_by(Message.created_on.desc())
                )
            print(messages)
            return [message.as_lc_message() for message in messages]

