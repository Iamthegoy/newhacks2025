from dataclasses import dataclass
from typing import List

@dataclass
class UserProfile:
    name: str
    major: str
    year: int
    identity: str
    favorite_subjects: List[str]
    hobbies: List[str]
    personality_type: str
    bio: str

