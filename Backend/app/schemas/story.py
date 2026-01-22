# Story State Variables - tracks dynamic state per choice
class StateVariables(BaseModel):
    variables: Dict[str, Any] = {}
# Choice with state variable effects
class Choice(BaseModel):
    choice_id: int
    text: str
    next_node_id: str
    state_changes: StateVariables = StateVariables()
# Story Node - individual story segment
class StoryNodeBase(BaseModel):
    node_id: str  # e.g., "1", "2A", "2B", "3A"
    content: str
    choices: List[Choice]
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None
    current_state: StateVariables = StateVariables()
    level: int
class StoryNodeCreate(StoryNodeBase):
    story_id: str
class StoryNodeInDB(StoryNodeBase):
    id: str  # MongoDB ObjectId as string
    story_id: str
    created_at: datetime
class StoryNodePublic(BaseModel):
    node_id: str
    content: str
    choices: List[Choice]
    image_url: Optional[str] = None
    current_state: StateVariables
# Story metadata
class StoryBase(BaseModel):
    title: str
    description: str
class StoryCreate(StoryBase):
    pass
class StoryInDB(StoryBase):
    id: str
    owner_id: str  # Reference to User
    created_at: datetime
    total_nodes: int
    total_levels: int
    master_plotline: Dict[str, Any]  # Stores StoryPlotlinePlan
    state_variable_definitions: List[Dict[str, Any]]
class StoryPublic(BaseModel):
    id: str
    title: str
    description: str
    current_node: Optional[StoryNodePublic] = None