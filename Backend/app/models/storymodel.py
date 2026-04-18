"""
Story-related Beanie document and Pydantic models.

Defines the data layer for interactive stories including story nodes,
choices with state-variable side-effects, and the top-level ``Story``
document persisted in MongoDB.
"""

from beanie import Document
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class StateVariable(BaseModel):
    """A single state variable and its current value.

    State variables track mutable story state (e.g. "health", "trust")
    that can change as the reader makes choices.

    Attributes:
        variable_name: Unique identifier for the variable.
        value: The current value; its Python type matches the variable's
            defined type in the story schema.
    """

    variable_name: str = Field(..., description="The unique ID of the variable.")
    value: Any = Field(
        ...,
        description="The initial value of this state variable. "
        "Its type is same as attribute type",
    )


class Choice(BaseModel):
    """A selectable choice presented at the end of a story node.

    Each choice leads to the next node and may modify state variables.

    Attributes:
        choice_id: Ordinal identifier of this choice within its node.
        text: The reader-facing label for the choice.
        next_node_id: The ``node_id`` of the node this choice leads to.
        story_state_variables: State variable mutations applied when this
            choice is selected.
    """

    choice_id: int
    text: str
    next_node_id: str
    story_state_variables: List[StateVariable]


class StoryNodeBase(BaseModel):
    """Base fields shared by all story-node representations.

    Attributes:
        node_id: Short human-readable identifier (e.g. ``"1"``, ``"2A"``).
        level: Depth level of this node in the story tree.
        content: The narrative text shown to the reader.
        choices: Available choices; empty for leaf / ending nodes.
        image_url: Optional URL of an illustration for this node.
        current_state: Snapshot of state variables at this point in the
            story.
    """

    node_id: str
    level: int
    content: str
    choices: List[Choice] = Field(default_factory=list)
    image_url: Optional[str] = None
    current_state: List[StateVariable] = Field(default_factory=list)


class StoryNode(StoryNodeBase):
    """Full story node stored in the database.

    Extends :class:`StoryNodeBase` with internal-only fields such as
    ``image_prompt`` and enforces a maximum of 2 choices per node.

    Attributes:
        choices: Overridden to enforce ``max_length=2``.
        image_prompt: Prompt text used to generate the node's image.
    """

    choices: List[Choice] = Field(default_factory=list, max_length=2)
    image_prompt: Optional[str] = None


class StoryNodePublic(StoryNodeBase):
    """Public-facing story node returned by the API.

    Identical to :class:`StoryNodeBase` — omits internal fields like
    ``image_prompt``.
    """

    pass


class StoryBase(BaseModel):
    """Common fields for every story representation.

    Attributes:
        public_id: Externally-visible UUID for the story.
        title: Display title of the story.
        created_at: Timestamp when the story was created (UTC).
        total_nodes: Number of nodes in the story tree.
        total_levels: Depth of the story tree.
        state_variable_definitions: Schema definitions for all state
            variables used throughout this story.
    """

    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_nodes: int
    total_levels: int
    state_variable_definitions: List[Dict[str, Any]]


class Story(Document, StoryBase):
    """MongoDB document for a complete interactive story.

    Inherits all :class:`StoryBase` fields and adds internal-only data
    that is not exposed via public API responses.

    Attributes:
        user_id: Public UUID of the owning user.
        master_plotline: Full plotline plan produced by the story agent.
        nodes: Ordered list of :class:`StoryNode` instances generated
            so far.
    """

    user_id: str  # Reference to User
    master_plotline: Dict[str, Any]  # Stores StoryPlotlinePlan
    nodes: List[StoryNode] = Field(default_factory=list)


class StoryPublic(StoryBase):
    """Public-facing story summary returned by the API.

    Inherits all fields from :class:`StoryBase`, deliberately excluding
    internal data such as ``master_plotline`` and ``nodes``.
    """

    pass