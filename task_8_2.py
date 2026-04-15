import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

DB_NAME = "todos.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str

app = FastAPI()
init_db()

def get_todo_or_404(todo_id: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return dict(row)

@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO todos (title, description) VALUES (?, ?)",
        (todo.title, todo.description)
    )
    
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return get_todo_or_404(todo_id)

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    return get_todo_or_404(todo_id)

@app.get("/todos", response_model=List[Todo])
async def get_all_todos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todos ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate):
    existing = get_todo_or_404(todo_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    update_fields = []
    values = []
    
    if todo.title is not None:
        update_fields.append("title = ?")
        values.append(todo.title)
    
    if todo.description is not None:
        update_fields.append("description = ?")
        values.append(todo.description)
    
    if todo.completed is not None:
        update_fields.append("completed = ?")
        values.append(1 if todo.completed else 0)
    
    if not update_fields:
        conn.close()
        return existing
    
    query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
    values.append(todo_id)
    
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    return get_todo_or_404(todo_id)

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    get_todo_or_404(todo_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    
    return None