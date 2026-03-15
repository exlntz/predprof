from pydantic import BaseModel


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    password: str
    password_repeat: str