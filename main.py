from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# 👇 Add this CORS block:
origins = [
    "http://localhost:5173",              # for local dev
    "https://vibbly-frontend.vercel.app"  # your production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # allow these origins
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods
    allow_headers=["*"],              # allow all headers
)

app.include_router(router)

# existing code…


@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

# This is crucial for Railway:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
