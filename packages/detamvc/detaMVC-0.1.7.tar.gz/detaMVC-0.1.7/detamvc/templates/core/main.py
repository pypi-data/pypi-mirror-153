from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from static_pages.router import static_pages_router

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static_pages/static"), name="static")

app.include_router(static_pages_router, tags=["pages"], prefix="")
