from typing import List

from pydantic import BaseModel


class clip(BaseModel):
    start: float
    end: float
    tag: str
    tagger: str
    tagsentence: str


class setInfo(BaseModel):
    hash: str
    length: float
    clips: List[clip]
    conjunctions: List[str]
