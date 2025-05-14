from fastapi import FastAPI
app:FastAPI = FastAPI()

@app.get("/notification")
def notification(filter:str):
    return {"data":f"filter{filter}"}




# write in browser
#http://127.0.0.1:8000/notification?filter=test