from fastapi import FastAPI, Path, Query, HTTPException

app = FastAPI()

@app.get("/info/{user_name}")
def get_info(
    user_name: str = Path(..., min_length=3, max_length=15),
    user_id: int = Query(..., gt=0, lt=100)):

    if user_name == "test":
        raise HTTPException(status_code=404, detail=f"{user_name} not found")
    return {"uswrname": user_name, "user_id": user_id}

    