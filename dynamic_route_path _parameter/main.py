from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/")
def home():
    return "dynamic route"

@app.get("/blog/{user_name}")
def blogpage(user_name):
    return {"page":"blogpage" ,"user_name":user_name}

# Give condition 
@app.get("/{username}/{user_id}")
def get_info(
    username:str = Path(..., min_length=3, max_length=15),
    user_id:int = Path(..., gt=0, lt=1000)):
    return {"username":username, "user_id":user_id}


