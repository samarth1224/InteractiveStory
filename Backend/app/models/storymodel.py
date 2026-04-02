from beanie import Document,PydanticObjectId
from pydantic import BaseModel,Field
from typing import Any,Dict,List,Optional
from datetime import datetime
import uuid

class StateVariables(BaseModel):
    variables: Dict[str, Any] = {}

# Choice with state variable effects
class Choice(BaseModel):
    choice_id: int
    text: str
    next_node_id: str
    state_changes: StateVariables = StateVariables()

class StoryNodeBase(BaseModel):
    node_id: str  # e.g., "1", "2A", "2B", "3A"
    level: int
    content: str
    choices: List[Choice]
    image_url: Optional[str] = None
    current_state: StateVariables = StateVariables()
# Story Node - individual story segment
class StoryNode(StoryNodeBase):
    node_id: str  # e.g., "1", "2A", "2B", "3A"
    level: int
    content: str
    choices: List[Choice]
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None
    current_state: StateVariables = StateVariables()
class StoryNodePublic(StoryNodeBase):
    pass

# Story Model

class StoryBase(BaseModel):
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)
    title: str
    description: str
    created_at: datetime
    total_nodes: int
    total_levels: int
    state_variable_definitions: List[Dict[str, Any]]

class Story(Document,StoryBase):
    owner_id: str  # Reference to User
    master_plotline: Dict[str, Any]  # Stores StoryPlotlinePlan
    nodes: List[StoryNode] = []

class StoryPublic(BaseModel):
    pass





