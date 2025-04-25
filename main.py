from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# ✅ Allowed frontend origins (local + production)
origins = [
    "http://localhost:5173",               # for local development
    "https://vibbly-frontend.vercel.app",  # your deployed frontend
]

# ✅ Enable CORS for frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # which frontend URLs can access
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods
    allow_headers=["*"],              # allow all headers
)

# ✅ Mount API routes
app.include_router(router)

# ✅ Simple root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

# ✅ Railway will call this when container starts
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
