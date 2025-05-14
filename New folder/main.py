from fastapi import FastAPI, Body, Header
app:FastAPI =FastAPI()

@app.post("/hi")  #post method
def greet(who:str = Body(embed=True)):
    return f"Hello, {who} with post method..."







app:FastAPI =FastAPI()

@app.post("/hi")  #post method
def greet(who:str = Header()):
    return f"Hello, {who} !"








# from model import Creature
# app:FastAPI =FastAPI()

# @app.post("/creature")  #post method
# def get_all() -> list[Creature]:
#     from data import get_creatures
#     return get_creatures()