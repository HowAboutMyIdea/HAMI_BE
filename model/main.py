from pydantic import BaseModel

class IdeaRequest(BaseModel):
    text: str

class ExtractedIdeaResponse(BaseModel):
    main_subject: str
    keywords: list[str]
    summary: str