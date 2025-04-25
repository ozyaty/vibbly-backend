from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# Add allowed origins (localhost and production)
origins = [
    "http://localhost:5173",             # for local dev
    "https://vibbly-frontend.vercel.app" # your production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],           # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],           # Allow all headers
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

# For Railway deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
