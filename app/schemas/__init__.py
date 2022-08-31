from .user import User, UserCreate, UserDB, UserUpdate
from pydantic import UUID4, BaseModel, EmailStr, Field

class BaseRequestResponse(BaseModel):
    class Config:
        # SQLAlchemy does not return a dictionary, which is what pydantic expects by default. 
        # You can configure your model to also support loading from standard orm parameters
        # reference: https://stackoverflow.com/a/69504636/7639845
        orm_mode = True