from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user import register, auth, editprofile
from posts import post, comment

app = FastAPI()

# CORS:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes:

app.include_router(register.router)
app.include_router(auth.router)
app.include_router(editprofile.router)

app.include_router(post.router)
app.include_router(comment.router)
