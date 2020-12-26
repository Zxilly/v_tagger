from typing import List, Optional

from pydantic import BaseModel


class clip(BaseModel):
    start: float
    end: float
    tag: str
    tagger: str


class setInfo(BaseModel):
    hash: str
    length: float
    clips: List[clip]
