from pydantic import BaseModel


class Metadata(BaseModel, extra='allow'):
    conv_id: str
    user_id: str
    chat_file_hash: str


class ChatArgs(BaseModel, extra='allow'):
    conv_id: str
    chat_file_name: str
    chat_file_hash: str
    streaming: bool
