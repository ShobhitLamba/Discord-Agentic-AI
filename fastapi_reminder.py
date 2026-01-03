from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class Reminder(BaseModel):
    title: str
    date: str
    start_time: str
    end_time: str
    description: str

SWIFT_EXECUTABLE = "./SetReminder"

@app.post("/setreminder")
async def set_reminder(reminder: Reminder):
    try:
        result = subprocess.run(
            [
                SWIFT_EXECUTABLE,
                reminder.title,
                reminder.date,
                reminder.start_time,
                reminder.end_time,
                reminder.description
            ],
            capture_output=True,
            text=True,
            timeout=3,
            check=True
        )
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}
    except subprocess.TimeoutExpired:
        return {"status": "error", "output": "Calendar operation timed out"}
