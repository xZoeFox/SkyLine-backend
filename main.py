from fastapi import FastAPI
from user import register

app = FastAPI()

app.include_router(register.router)