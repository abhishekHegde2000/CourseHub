import logging
from fastapi import FastAPI
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import populate_db

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(levelname)s\n%(message)s\n",
    handlers=[
        logging.FileHandler("kimo_api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
