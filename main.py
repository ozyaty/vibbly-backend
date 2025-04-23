from fastapi import FastAPI
from api.routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Telegram Social App"}

app.include_router(router)