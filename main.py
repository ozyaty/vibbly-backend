from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.users import router as users_router  # 👈 (this is new)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://vibbly-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(users_router)  # 👈 (this is new)

@app.get("/")
def read_root():
    return {"message": "Welcome to Vibbly Backend!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
