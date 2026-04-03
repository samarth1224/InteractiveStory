from beanie import Document
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class StateVariable(BaseModel):
    variable_name: str = Field(..., description="The unique ID of the variable.")
    value: Any = Field(..., description='The initial value of this state variable. Its type is same as attribute type')


# Choice with state variable effects
class Choice(BaseModel):
    choice_id: int
    text: str
    next_node_id: str
    story_state_variables: List[StateVariable]


class StoryNodeBase(BaseModel):
    node_id: str  # e.g., "1", "2A", "2B", "3A"
    level: int
    content: str
    choices: List[Choice] = Field(default_factory=list)
    image_url: Optional[str] = None
    current_state: List[StateVariable] = Field(default_factory=list)


# Story Node - individual story segment
class StoryNode(StoryNodeBase):
    node_id: str  # e.g., "1", "2A", "2B", "3A"
    level: int
    content: str
    choices: List[Choice] = Field(default_factory=list, max_length=2)
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None


class StoryNodePublic(StoryNodeBase):
    pass


# Story Model
class StoryBase(BaseModel):
    public_id: uuid.UUID = Field(unique=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.now)
    total_nodes: int
    total_levels: int
    state_variable_definitions: List[Dict[str, Any]]


class Story(Document, StoryBase):
    user_id: str  # Reference to User
    master_plotline: Dict[str, Any]  # Stores StoryPlotlinePlan
    nodes: List[StoryNode] = []


class StoryPublic(BaseModel):
    pass