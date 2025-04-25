from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI()

# ✅ Temporarily allow all origins for testing — change later to origins list
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🚨 Allow any origin (for CORS debugging only!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your routes
app.include_router(router)

# ✅ Simple root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

# ⚠️ REMOVE uvicorn.run() block for Railway — it's not needed and breaks deployment
