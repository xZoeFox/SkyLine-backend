from fastapi import FastAPI
from user import register, auth

app = FastAPI()

app.include_router(register.router)
app.include_router(auth.router)
