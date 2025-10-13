"""Types"""

from enum import Enum
from pydantic import BaseModel

class DraftClass(Enum):
    """Enumeration for draft classification types."""
    FEATURE = 1
    BUG = 2

class DraftClassification(BaseModel):
    """Model for classifying draft documents."""
    draft_class: DraftClass

class BranchDescription(BaseModel):
    """Model for short branch description."""
    short_description: str
