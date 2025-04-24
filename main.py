from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

# This is crucial for Railway:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
