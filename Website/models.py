from dataclasses import dataclass
from typing import List

@dataclass
class UserProfile:
    name: str
    age: int
    nationality: str
    gender:str
    favorite_subjects: List[str]
    hobbies: List[str]
    bio: str
    water_points: int = 0
