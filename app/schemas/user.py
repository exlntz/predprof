from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    password_repeat: str