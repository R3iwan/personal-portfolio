from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    live_demo: str | None = None

@app.get("/projects")
async def get_projects():
    cursor.execute("SELECT * FROM portfolio_project")
    projects = cursor.fetchall()
    return {"projects": projects}

@app.get("/projects")
async def add_project(project: Project):
    cursor.execute(
        "INSERT INTO portfolio_project(title, description, github_link, live_demo) VALUES(%s, %s, %s, %s, NOW())",
        (project.title, project.description, project.github_link, project.live_demo)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
