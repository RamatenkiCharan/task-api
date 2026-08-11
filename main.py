from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a to-do list."
)


# -------------------------
# In-memory task list
# -------------------------

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Publish to GitHub",
        "done": False
    }
]


# -------------------------
# Request models
# -------------------------

class TaskCreate(BaseModel):
    title: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


# -------------------------
# GET /
# -------------------------

@app.get(
    "/",
    summary="API information",
    description="Returns basic information about the Task API."
)
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# -------------------------
# GET /health
# -------------------------

@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the Task API is running."
)
def health():
    return {
        "status": "ok"
    }


# -------------------------
# GET /tasks
# -------------------------

@app.get(
    "/tasks",
    summary="Get all tasks",
    description="Returns all tasks currently stored in memory."
)
def get_tasks():
    return tasks


# -------------------------
# GET /tasks/{task_id}
# -------------------------

@app.get(
    "/tasks/{task_id}",
    summary="Get one task",
    description="Returns a single task using its ID."
)
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )


# -------------------------
# POST /tasks
# -------------------------

@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task and adds it to the in-memory task list."
)
def create_task(task: TaskCreate):

    # Validate title
    if task.title is None or not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "Title is required and cannot be empty"
            }
        )

    # Generate next ID
    new_id = max(task["id"] for task in tasks) + 1

    # Create new task
    new_task = {
        "id": new_id,
        "title": task.title.strip(),
        "done": False
    }

    # Add task to list
    tasks.append(new_task)

    return new_task


# -------------------------
# PUT /tasks/{task_id}
# -------------------------

@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title and/or completion status of an existing task."
)
def update_task(task_id: int, task_update: TaskUpdate):

    # Find the task
    for task in tasks:

        if task["id"] == task_id:

            # Update title
            if task_update.title is not None:

                if not task_update.title.strip():
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "Title cannot be empty"
                        }
                    )

                task["title"] = task_update.title.strip()

            # Update done status
            if task_update.done is not None:
                task["done"] = task_update.done

            # Nothing was provided
            if (
                task_update.title is None
                and task_update.done is None
            ):
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Nothing to update"
                    }
                )

            return task

    # Task doesn't exist
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )


# -------------------------
# DELETE /tasks/{task_id}
# -------------------------

@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes an existing task from the in-memory task list."
)
def delete_task(task_id: int):

    # Find the task
    for i, task in enumerate(tasks):

        if task["id"] == task_id:

            tasks.pop(i)

            return

    # Task doesn't exist
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )