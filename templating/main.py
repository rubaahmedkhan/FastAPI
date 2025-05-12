from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return "hello RUBA"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
