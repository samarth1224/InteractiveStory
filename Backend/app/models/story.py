from beanie import Document,PydanticObjectId
from pydantic import BaseModel
from typing import Any,Dict,List,Optional
from datetime import datetime

class StateVariables(BaseModel):
    variables: Dict[str, Any] = {}

# Choice with state variable effects
class Choice(BaseModel):
    choice_id: int
    text: str
    next_node_id: str
    state_changes: StateVariables = StateVariables()

# Story Node - individual story segment
class StoryNode(BaseModel):
    node_id: str  # e.g., "1", "2A", "2B", "3A"
    level: int
    content: str
    choices: List[Choice]
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None
    current_state: StateVariables = StateVariables()

class Story(Document):
    title: str
    description: str
    owner_id: str  # Reference to User
    created_at: datetime
    total_nodes: int
    total_levels: int
    master_plotline: Dict[str, Any]  # Stores StoryPlotlinePlan
    state_variable_definitions: List[Dict[str, Any]]
    nodes: List[StoryNode] = []


