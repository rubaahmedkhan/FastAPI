from fastapi import FastAPI, Body, Header
from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

class UserResponse(BaseModel):
    user_id: int
    status: str

app:FastAPI =FastAPI()


@app.post("/create-user")
def create_user(user: User):
    return {"name": user.name, "age": user.age, "status": "user created"}

                             #Fast API response
@app.post("/create-user1", response_model=UserResponse)
def create_user(user: User, user_id: int):
    print("\n[User]", user)
    return {"status":"user created", "user_id": user_id}




@app.post("/hi")  #post method
def greet(who:str = Body(embed=True)):
    return f"Hello, {who} with post method..."



# from model import Creature
# app:FastAPI =FastAPI()

# @app.post("/creature")  #post method
# def get_all() -> list[Creature]:
#     from data import get_creatures
#     return get_creatures()




# PUT -> Update Entire Resource
@app.put("/update-user/{user_id}")
def update_user(user_id:int, user: User):
    print("\n[User]", user)
    return {"user_id": user_id, "status": "user_updated"}



 # PATCH -> Update Partial Resource
@app.patch("/update-user-partial/{user_id}")
def update_user(user_id:int, user: User):
    print("\n[User]", user)
    return {"user_id": user_id, "status": "user updated partial"}   


# DELETE -> Deete
@app.delete("/delete-user/{user_id}")
def update_user(user_id:int):
    return {"user_id": user_id, "status": "user deleted"}    