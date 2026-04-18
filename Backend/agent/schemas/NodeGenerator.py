"""
Output schema for the Story Node Generator agent.

Defines the structured response format that the LLM must produce when
generating an individual story node, including narrative content,
branching choices, and an image-generation prompt.
"""

from pydantic import BaseModel, Field
from typing import List, Any


class StoryStateVariables(BaseModel):
    """A state variable snapshot attached to a choice.

    When the reader picks a choice, these values become the starting
    state for the next node.

    Attributes:
        variable_name: Unique identifier matching a variable defined in
            the master plotline's branching logic.
        value: The new value for this variable after the choice is made.
    """

    variable_name: str = Field(
        ..., description="The unique ID of the variable."
    )
    value: Any = Field(
        ...,
        description="The initial value of this state variable. "
        "Its type is same as attribute type",
    )


class Choice(BaseModel):
    """A single branching choice within a story node.

    Each node presents up to 2 choices.  Every choice carries an ID,
    display text, the target node it leads to, and any state-variable
    mutations that take effect when chosen.

    Attributes:
        choice_id: 1-based ordinal (1 or 2) identifying this choice.
        text: Reader-facing label for the choice.
        next_node_id: ``node_id`` of the node this choice transitions to.
        story_state_variables: State changes applied if this choice is
            selected.
    """

    choice_id: int = Field(
        ..., description="Ordinal ID of this choice (1 or 2)."
    )
    text: str = Field(
        ..., description="The text displayed to the user for this choice"
    )
    next_node_id: str = Field(
        ..., description="The ID of the Next Node this choice will lead to"
    )
    story_state_variables: List[StoryStateVariables] = Field(
        description="The state changes that occur if the choice is picked"
    )


class StoryNodeGeneratorAgentResponse(BaseModel):
    """Structured output produced by the node-generator agent.

    The LLM must return a response conforming to this schema for every
    node it generates.

    Attributes:
        node_id: Short identifier for this node (e.g. ``"3A"``).
        level: Graph-level depth of this node.
        content: The narrative text for the story segment.
        choices: Up to 2 branching choices (empty for ending nodes).
        image_prompt: Description used to generate an illustration for
            this node.
    """

    node_id: str
    level: int
    content: str = Field(
        default="No content available",
        description="The content of the story node.",
    )
    choices: List[Choice] = Field(
        default_factory=list,
        max_length=2,
        description="A list of 2 choices available to player",
    )
    image_prompt: str = Field(
        default="No image available",
        description="The prompt to generate the image for the story node.",
    )
