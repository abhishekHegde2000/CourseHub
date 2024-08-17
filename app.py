from fastapi import Request
import logging
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Trusted Host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Adjust this in production
)

# Add GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


class TodoModel(BaseModel):
    nid: Optional[int] = None
    name: str
    is_completed: Optional[bool] = False


todos: List[TodoModel] = []


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests_and_responses(request: Request, call_next):
    """Middleware to log requests and responses, and add process time header."""
    start_time = time.time()

    # Log the incoming request details
    logger.info(f"Incoming request: {request.method} {request.url}")

    # Process the request
    response = await call_next(request)

    # Calculate the processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Log the response details
    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response headers: {response.headers}")

    return response


@app.get("/")
async def root() -> dict:
    """Root endpoint returning a welcome message."""
    return {"message": "Hello World"}


@app.post("/todo/", response_model=TodoModel)
async def create_todo(todo: TodoModel, background_tasks: BackgroundTasks) -> TodoModel:
    """Create a new todo item."""
    todo.nid = len(todos) + 1
    todos.append(todo)
    background_tasks.add_task(log_todo_creation, todo.nid)
    return todo


@app.get("/todo/{nid}", response_model=TodoModel)
async def get_todo(nid: int) -> TodoModel:
    """Retrieve a todo item by its ID."""
    todo = next((todo for todo in todos if todo.nid == nid), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.get("/allTodos", response_model=List[TodoModel])
async def get_all_todos(skip: int = 0, limit: int = 10) -> List[TodoModel]:
    """Retrieve all todo items with pagination."""
    return todos[skip: skip + limit]


@app.put("/todo/{nid}", response_model=TodoModel)
async def update_todo(nid: int, todo: TodoModel) -> TodoModel:
    """Update a todo item by its ID."""
    index = next((i for i, t in enumerate(todos) if t.nid == nid), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[index] = todo
    todos[index].nid = nid  # Ensure the ID remains the same
    return todos[index]


@app.delete("/todo/{nid}")
async def delete_todo(nid: int) -> dict:
    """Delete a todo item by its ID."""
    index = next((i for i, t in enumerate(todos) if t.nid == nid), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(index)
    return {"message": "Todo deleted successfully"}


def log_todo_creation(nid: int):
    """Background task to log todo creation."""
    print(f"Todo with ID {nid} has been created.")
