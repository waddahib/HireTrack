from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class JobApplicationCreate(BaseModel):
    company: str
    position: str
    status: str
    location: str | None = None
    job_url: str | None = None
    notes: str | None = None


class JobApplication(JobApplicationCreate):
    id: int


applications = []
next_id = 1


@app.get("/")
def home():
    return {"message": "HireTrack API is running"}


@app.post("/applications")
def create_application(application: JobApplicationCreate):
    global next_id

    new_application = JobApplication(
        id=next_id,
        **application.model_dump()
    )

    applications.append(new_application)
    next_id += 1

    return {
        "message": "Application added successfully",
        "application": new_application
    }


@app.get("/applications")
def get_applications():
    return applications

@app.get("/applications/{application_id}")
def get_application(application_id: int):
    for application in applications:
        if application.id == application_id:
            return application

    return {"error": "Application not found"}

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    for index, application in enumerate(applications):
        if application.id == application_id:
            deleted_application = applications.pop(index)

            return {
                "message": "Application deleted successfully",
                "application": deleted_application
            }

    return {"error": "Application not found"}

@app.put("/applications/{application_id}")
def update_application(application_id: int, updated_application: JobApplicationCreate):
    for index, application in enumerate(applications):
        if application.id == application_id:
            new_application = JobApplication(
                id=application_id,
                **updated_application.model_dump()
            )

            applications[index] = new_application

            return {
                "message": "Application updated successfully",
                "application": new_application
            }

    return {"error": "Application not found"}