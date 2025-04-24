ffrom fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

<<<<<<< HEAD
# This is crucial for Railway:
=======
>>>>>>> 49ebd018b937298f56d0b2c7f6c97cecb77ddca1
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
