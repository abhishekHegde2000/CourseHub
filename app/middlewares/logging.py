import logging
from fastapi import FastAPI


app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("kimo_api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
