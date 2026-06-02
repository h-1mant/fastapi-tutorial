from fastapi import FastAPI
from app.routers import posts, auth, users, vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=users.router, prefix="/users", tags=["users"])
app.include_router(router=posts.router, prefix="/posts", tags=["posts"])
app.include_router(router=auth.router, prefix="/login", tags=["authentication"])
app.include_router(router=vote.router, prefix="/vote", tags=["votes"])

# Root
@app.get("/")
def root():
    return {"message": "Hello World!"}
