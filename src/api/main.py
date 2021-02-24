import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from api.routers import root

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

app = FastAPI()
app.include_router(root.router)
