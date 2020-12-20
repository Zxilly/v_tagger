from typing import List

from pydantic import BaseModel


class clip(BaseModel):
    start: float
    end: float
    tag: str
    tagger: List[str]


class setInfo(BaseModel):
    hash: str
    length:float
    clip: List[clip]
