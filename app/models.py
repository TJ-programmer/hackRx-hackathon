from pydantic import BaseModel, Field
from typing import List

class Request(BaseModel):
    document_url: str = Field(..., alias="documents")
    questions: List[str]

    class Config:
        allow_population_by_field_name = True

class Response(BaseModel):
    answers: List[str]
