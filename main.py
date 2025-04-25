from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# ✅ CORS setup
origins = [
    "http://localhost:5173",              # local development
    "https://vibbly-frontend.vercel.app"  # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route setup
app.include_router(router)

# ✅ Root route (for testing)
@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

