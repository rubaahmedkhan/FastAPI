from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return "dynamic route"

@app.get("/blog/{user_name}")
def blogpage(user_name):
    return {"page":"blogpage" ,"user_name":user_name}

         
     