"""Task model and REST API.

Field       | Purpose                              | Example
------------|--------------------------------------|--------------------------
id          | Unique identifier, generated as UUID | 2b2b... (generated)
title       | Short task name                      | Prepare report
description | Optional task details                | Summarize results
priority    | Importance: low, medium, or high     | high
status      | todo, in_progress, or done           | in_progress
due_date    | Optional deadline (YYYY-MM-DD)       | 2025-12-31

Endpoints: GET /tasks, GET /tasks/{task_id}, POST /tasks,
PATCH /tasks/{task_id}, DELETE /tasks/{task_id}.
Run: uvicorn datamodel:app --reload
Dependencies: pip install fastapi uvicorn
"""

from datetime import date
from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


class Priority(str, Enum):
	low = "low"
	medium = "medium"
	high = "high"


class TaskStatus(str, Enum):
	todo = "todo"
	in_progress = "in_progress"
	done = "done"


class TaskCreate(BaseModel):
	title: str = Field(min_length=1, max_length=200, examples=["Prepare report"])
	description: str | None = None
	priority: Priority = Priority.medium
	status: TaskStatus = TaskStatus.todo
	due_date: date | None = None


class TaskUpdate(BaseModel):
	title: str | None = Field(default=None, min_length=1, max_length=200)
	description: str | None = None
	priority: Priority | None = None
	status: TaskStatus | None = None
	due_date: date | None = None


class Task(TaskCreate):
	id: UUID = Field(default_factory=uuid4)


app = FastAPI(title="Task API", version="1.0.0")
tasks: dict[UUID, Task] = {}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
	task = Task(**payload.model_dump())
	tasks[task.id] = task
	return task


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
	return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID) -> Task:
	task = tasks.get(task_id)
	if task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, payload: TaskUpdate) -> Task:
	task = tasks.get(task_id)
	if task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	updated = task.model_copy(update=payload.model_dump(exclude_unset=True))
	tasks[task_id] = updated
	return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> Response:
	if tasks.pop(task_id, None) is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return Response(status_code=status.HTTP_204_NO_CONTENT)
