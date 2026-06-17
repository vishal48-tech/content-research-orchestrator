from pydantic import BaseModel
from typing import List, Dict, Any

class Source(BaseModel):
    id: str = ""
    title: str = ""
    url: str = ""
    content: str = ""
    word_count: int = 0
    credibility_score: float = 0.5

class OutlineSection(BaseModel):
    title: str = ""
    points: List[str] = []

class Outline(BaseModel):
    sections: List[OutlineSection] = []
    raw: str = ""

class ResearchState(BaseModel):
    query: str = ""
    research_plan: Dict[str, Any] = {}
    sources: List[Source] = []
    outline: Outline = Outline()
    evaluation: Dict[str, Any] = {}
    current_step: str = "planning"
    messages: List[Dict[str, str]] = []