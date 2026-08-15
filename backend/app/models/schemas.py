from typing import Optional, List
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class Payload(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    content: str
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: str
    params: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None

class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    result_id: str
    run_id: str
    payload_id: int
    outcome: str
    guardrail_json: Optional[str] = None
    llm_response_json: Optional[str] = None
    validator_json: Optional[str] = None
    timestamps_json: Optional[str] = None

class RagSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))
