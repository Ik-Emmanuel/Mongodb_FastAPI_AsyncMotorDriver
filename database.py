import motor.motor_asyncio
from model import Todo

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.TodoListMotorDB
collection = database.todo


async def fetch_one_todo(todo_id):
    document = await collection.find_one({"todo_id": int(todo_id)})
    return document


async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos


async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_todo(todo_id, data):
    await collection.update_one({"todo_id": int(todo_id)}, {"$set": {"title": data.title, "description": data.description, "completed": data.completed}})
    document = await collection.find_one({"todo_id": int(todo_id)})
    return document

async def remove_todo(todo_id):
    await collection.delete_one({"todo_id": int(todo_id)})
    return True