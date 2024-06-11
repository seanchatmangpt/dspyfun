"""Generate Pydantic models and DSPy."""
import dspy
import typer
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from dspyfun.utils.dspy_tools import init_ol

app = typer.Typer()


class Appointment(BaseModel):
    uid: str = Field(..., description="Unique identifier for the event")
    dtstamp: datetime = Field(..., description="Timestamp of when the event was created")
    dtstart: datetime = Field(..., description="Start date and time of the event")
    dtend: Optional[datetime] = Field(None, description="End date and time of the event")
    summary: Optional[str] = Field(None, description="Brief description of the event")
    description: Optional[str] = Field(None, description="Detailed description of the event")
    location: Optional[str] = Field(None, description="Location of the event")
    organizer: Optional[str] = Field(None, description="Organizer of the event")
    attendees: Optional[list[str]] = Field(None, description="List of attendees")

    class Config:
        json_schema_extra = {
            "example": {
                "uid": "1234567890@example.com",
                "dtstamp": "2023-10-01T12:00:00Z",
                "dtstart": "2023-10-01T15:00:00Z",
                "dtend": "2023-10-01T16:00:00Z",
                "summary": "Team Meeting",
                "description": "Discuss project updates and next steps.",
                "location": "Conference Room 1",
                "organizer": "organizer@example.com",
                "attendees": ["attendee1@example.com", "attendee2@example.com"]
            }
        }


@app.command(name="text")
def pyd_text():
    """Convert unstructured text into Pydantic Model"""
    # typer.echo("Running text subcommand.")
    # print(Appointment.schema_json())

    print("Initialize Ollama")
    init_ol()

    pred = dspy.ChainOfThought('text, json_schema -> valid_json_for_text')
    response = pred.forward(text="Dentist at 5PM", json_schema=Appointment.schema_json()).valid_json_for_text
    # print(response)
    print(Appointment.model_validate_json(response))


@app.command(name="cypher")
def pyd_cypher():
    """Convert unstructured text into the cypher language"""

    print("Initialize Ollama")
    init_ol()

    pred = dspy.ChainOfThought(cypherConverter)
    response = pred.forward(text="Meet me at the park at 5PM", cypher_language="cypher").valid_cypher_text
    print(response)
