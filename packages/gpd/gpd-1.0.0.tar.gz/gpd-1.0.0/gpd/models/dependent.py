from pydantic import BaseModel


class Dependent(BaseModel):
    name: str
    stars: int
    forks: int
    author: str
    url: str
