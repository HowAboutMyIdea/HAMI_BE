from pydantic import BaseModel
from typing import List  # ← 필수

class IdeaRequest(BaseModel):
    text: str

class ExtractedIdeaResponse(BaseModel):
    main_subject: str
    keywords: List[str]
    summary: str
    feedback: str