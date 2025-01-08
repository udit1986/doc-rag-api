from pydantic import BaseModel
from typing import List

class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass

# Models
class DocumentRequest(BaseRequest):
    id: int
    content: str

class QuestionRequest(BaseRequest):
    question: str
    document_ids: List[int]