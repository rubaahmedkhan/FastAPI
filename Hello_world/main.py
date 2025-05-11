from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return "hello world"

@app.get("/about")
def about():
    dataobj = {
        "name" : "ruba",
        "age" : 22,
        "subject": "maths"
    }
         
     
    return dataobj  
     

