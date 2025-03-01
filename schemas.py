from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    gender: str
    city: str
    interests: str

    class Config:
        orm_mode = True
