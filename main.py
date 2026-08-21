from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class JobApplication(BaseModel):
    company: str
    position: str
    status: str
    location: str | None = None
    job_url: str | None = None
    notes: str | None = None


applications = []


@app.get("/")
def home():
    return {"message": "HireTrack API is running"}


@app.post("/applications")
def create_application(application: JobApplication):
    applications.append(application)
    return {
        "message": "Application added successfully",
        "application": application
    }


@app.get("/applications")
def get_applications():
    return applications