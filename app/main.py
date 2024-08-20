from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import populate_db
from app.middlewares.logging import logger
from app.middlewares.cors import origins
from app.controllers.course_controller import router as course_router

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: status_code={response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    populate_db()
except Exception as e:
    logger.error(f"Failed to populate the database: {e}")
    raise HTTPException(status_code=500, detail="Internal Server Error")

app.include_router(course_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
