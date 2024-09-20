from pydantic import BaseModel


class UserLoggingData(BaseModel):
    user_id: str = ""
    password: str = ""
    name: str = ""

class BookData(BaseModel):
    title: str = ""
    author: str = ""
    isbn: str = ""

class Assignment(BaseModel):
    isbn: str = ""
    user_id: str = ""
