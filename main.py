from fastapi import FastAPI
from user import register, auth, editprofile

app = FastAPI()

app.include_router(register.router)
app.include_router(auth.router)
app.include_router(editprofile.router)
