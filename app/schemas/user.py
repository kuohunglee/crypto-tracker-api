from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    uersname: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    passwerd: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr