from typing import List, Optional

from pydantic import BaseModel


class marks(BaseModel):
    accuracy: int
    conherent: int
    relevance: int
    usability: int


class clip(BaseModel):
    start: float
    end: float
    tag: str
    tagger: str
    tagsentence: str
    mark: Optional[marks]

class setInfo(BaseModel):
    hash: str
    length: float
    full: Optional[str]
    clips: List[clip]
    conjunctions: List[str]



class video(BaseModel):
    hash: str
    length: float
