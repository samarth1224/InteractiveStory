"""Story-related Beanie document and Pydantic models."""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class StateVariable(BaseModel):
    """A single state variable and its current value."""

    variable_name: str = Field(..., description="The unique ID of the variable.")
    value: Any = Field(
        ...,
        description="The initial value of this state variable. "
        "Its type is same as attribute type",
    )


class Choice(BaseModel):
    """A selectable choice presented at the end of a story node."""

    choice_id: int
    text: str
    next_node_id: str
    story_state_variables: List[StateVariable]


class StoryNodeBase(BaseModel):
    """Base fields shared by all story-node representations."""

    node_id: str
    level: int
    content: str
    choices: List[Choice] = Field(default_factory=list)
    image_url: Optional[str] = None


class StoryNode(StoryNodeBase):
    """Full story node stored in the database."""

    choices: List[Choice] = Field(default_factory=list, max_length=2)
    image_prompt: Optional[str] = None


class StoryNodePublic(StoryNodeBase):
    """Public-facing story node returned by the API."""

    pass


class StoryBase(BaseModel):
    """Common fields for every story representation."""

    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_nodes: int
    total_levels: int
    state_variable_definitions: List[Dict[str, Any]]
    story_state_variables: List[StateVariable] = Field(default_factory=list)


class Story(Document, StoryBase):
    """MongoDB document for a complete interactive story."""

    user_id: uuid.UUID  # Reference to User
    master_plotline: Dict[str, Any]  # Stores StoryPlotlinePlan
    nodes: Dict[str, StoryNode] = Field(default_factory=dict)


class StoryPublic(StoryBase):
    """Public-facing story summary returned by the API."""

    pass