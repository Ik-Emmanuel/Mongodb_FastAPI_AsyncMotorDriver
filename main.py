from fastapi import FastAPI, HTTPException
from model import Todo
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)


from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo/{todo_id}", response_model=Todo)
async def get_todo_by_title(todo_id):
    response = await fetch_one_todo(todo_id)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {todo_id}")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/todo/{todo_id}", response_model=Todo)
async def put_todo(todo_id: int, todo: Todo):
    response = await update_todo(todo_id, todo)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the id {todo_id}")

@app.delete("/api/todo/{todo_id}")
async def delete_todo(todo_id):
    response = await remove_todo(todo_id)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {todo_id}")