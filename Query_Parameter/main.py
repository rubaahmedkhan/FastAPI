from fastapi import FastAPI, Query
app:FastAPI = FastAPI()

@app.get("/notification")
def notification(filter:str):
    return {"data":f"filter{filter}"}


# write in browser
#http://127.0.0.1:8000/notification?filter=test

@app.get("/user/all")
def get_all_users(limit: int | None = Query(None, gt=0, lt=100)):
    print(f"limit: {limit}")
    if limit:
        return {"users": ["Ruba Ahmed"]}
    else:
        return {"users": ["Ruba Khan"]}
         
     