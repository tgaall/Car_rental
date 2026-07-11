from fastapi import FastAPI

app = FastAPI(
    title = "Car rental",
    version = "0.1.0",
)


#корневой эндпоинт

@app.get("/")
async def root():
    return {"message": "Welcome to car rental utility"}
