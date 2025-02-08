from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

conn = psycopg2.connect(
    dbname="django_db",
    user="django_db_user",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

class Project(BaseModel):
    title: str
    description: str
    github_link: str
    live_demos: str | None = None
    
@app.get('/projects')
async def get_projects():
    cursor.execute("SELECT * FROM portfolio_project")
    projects = cursor.fetchall()
    return {
        "projects": projects
    }

@app.post('/projects')
async def create_project(project: Project):
    cursor.execute(
        "INSERT INTO portfolio_project(title, description, github_link, live_demo, created_at) VALUES (%s, %s, %s, %s, NOW())",
        (project.title, project.description, project.github_link, project.live_demos)
    )
    conn.commit()
    return {"message": "Project added successfully"}

@app.delete('/projects/{project_id}')
async def delete_project(project_id):
    cursor.execute(
        "DELETE FROM portfolio_project WHERE id = %s",
        (project_id)
    )
    conn.commit()
    return {"message": "Project deleted sucessfully!"}

