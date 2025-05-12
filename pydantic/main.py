from pydantic import BaseModel, EmailStr

class person(BaseModel):
    name : str
    age : int
    email : EmailStr

ram = person(name="ruba", age = 22, email = "ruba@gmail.com")

print(person)