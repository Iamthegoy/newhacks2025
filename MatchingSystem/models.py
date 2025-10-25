from dataclasses import dataclass
from typing import List

@dataclass
class UserProfile:
    name: str
    age: int
    nationality: str
    gender:str
    favorite_subjects: List[str]
    hobby1: List[str]
    hobby2: str
    bio: str

