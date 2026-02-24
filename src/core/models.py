from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class JobField(str, Enum):
    GAMEDEV = "gamedev"
    CSHARP = "c#"
    PYTHON = "python"
    CPP = "c++"
    MOBILE = "mobile"
    JAVA = "java"
    CV = "cv"
    BACKEND = "backend"
    FRONTEND = "frontend"
    SOFTWARE = "yazılım"
    OTHER = "diğer"

class JobLocation(str, Enum):
    ANKARA = "ankara"
    REMOTE = "remote"
    HYBRID_ANKARA = "hybrid_ankara"
    TURKIYE = "türkiye"
    ISTANBUL = "istanbul"
    IZMIR = "izmir"
    BURSA = "bursa"
    EUROPE = "avrupa"
    USA = "abd"
    OTHER = "diğer"
    DEAD = "dead"

class JobLevel(str, Enum):
    JUNIOR = "junior"
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    UNKNOWN = "bilinmiyor"

class Job(BaseModel):
    """Represents a raw job listing before processing."""
    title: str
    company: str
    location: str
    summary: str = ""
    description: Optional[str] = ""
    link: Optional[str] = None
    published: Optional[str] = None

    @field_validator('title', 'company')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Must not be empty')
        return v.strip()

class ScoredJob(Job):
    """Represents a job listing after being processed and scored."""
    detected_field: JobField
    detected_location: JobLocation
    detected_level: JobLevel
    total_score: float
    is_restricted: bool = False
    restricted_reason: Optional[str] = None
