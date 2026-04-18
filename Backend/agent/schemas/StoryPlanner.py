"""
Output schema for the Story Planner agent.

Defines the master plotline blueprint that the planner agent produces,
including world-building, the bottleneck map of hard nodes, and
branching logic with tracked state variables.
"""

from typing import List, Literal, Any
from pydantic import BaseModel, Field, ConfigDict


# --- Section 1: The World & Rules ---

class WorldAndRules(BaseModel):
    """World-building and tonal guidelines for the story.

    Attributes:
        setting: Detailed description of geography, era, and atmosphere.
        tone_guidelines: Prose style instructions (vocabulary, mood, etc.).
        core_conflict: The main antagonist or systemic force opposing
            the player.
    """

    setting: str = Field(
        ...,
        description="Detailed description of the geography, era, and atmosphere.",
    )
    tone_guidelines: str = Field(
        ...,
        description="Instructions for prose style (e.g., vocabulary, sentence length, mood).",
    )
    core_conflict: str = Field(
        ...,
        description="The main antagonist or systemic force working against the player.",
    )


# --- Section 2: The Bottleneck Map (The Pearls) ---

class GraphStats(BaseModel):
    """Quantitative metadata for the story graph.

    Attributes:
        total_levels: Depth of the story graph (4–10).
        total_nodes: Total number of nodes, inclusive of hard and soft
            nodes (4–20).
    """

    total_levels: int = Field(
        ...,
        ge=4,
        le=10,
        description="Total level depth of the story graph theory-wise.",
    )
    total_nodes: int = Field(
        ...,
        ge=4,
        le=20,
        description="Total count of inclusive soft and hard nodes.",
    )


class HardNode(BaseModel):
    """A mandatory plot point (pearl) in the bottleneck model.

    Hard nodes are the fixed structural pillars of the story that every
    playthrough must pass through.

    Attributes:
        node_type: Structural role — one of Opening, Midpoint, Climax,
            or Ending.
        node_name: A unique, thematic name for this plot point.
        mandatory_event: The narrative event that MUST occur here.
        key_revelation: Crucial information unlocked at this stage.
        exit_conditions: State or achievement required to progress past
            this node.
    """

    node_type: Literal["Opening", "Midpoint", "Climax", "Ending"] = Field(
        ...,
        description="The structural role of this hard node.",
    )
    node_name: str = Field(
        ...,
        description="A unique, thematic name for the plot point.",
    )
    mandatory_event: str = Field(
        ...,
        description="The specific narrative event that MUST occur.",
    )
    key_revelation: str = Field(
        ...,
        description="Crucial information unlocked at this stage.",
    )
    exit_conditions: str = Field(
        ...,
        description="The state or achievement required to progress.",
    )


class BottleneckMap(BaseModel):
    """The structural backbone of the story — graph stats, title, and
    hard nodes combined into a single typed model.

    Replaces the previous heterogeneous list approach for type safety
    and clarity.

    Attributes:
        stats: Graph-level metadata (total levels and nodes).
        title: A catchy title for the story.
        hard_nodes: Exactly 4 hard nodes (Opening, Midpoint, Climax,
            Ending).
    """

    stats: GraphStats = Field(
        ...,
        description="Graph metadata: total levels and total nodes.",
    )
    title: str = Field(
        ...,
        description="A catchy title for the story.",
    )
    hard_nodes: List[HardNode] = Field(
        ...,
        description="Exactly 4 hard nodes defining the story's structural pillars.",
    )


# --- Section 3: The Branching Logic (The Strings) ---

class StateVariable(BaseModel):
    """A trackable state variable defined in the branching logic.

    Attributes:
        variable_name: Unique identifier (e.g. ``"Corruption_Level"``).
        type: Data type — Integer, Boolean, or String.
        description: How this variable impacts the story.
        value: Initial value; its Python type matches *type*.
    """

    variable_name: str = Field(
        ..., description="The unique ID of the variable."
    )
    type: Literal["Integer", "Boolean", "String"] = Field(
        ..., description="The data type."
    )
    description: str = Field(
        ..., description="How this variable impacts the story."
    )
    value: Any = Field(
        ...,
        description="The initial value of this state variable. "
        "Its type is same as attribute type",
    )


class BranchingLogic(BaseModel):
    """Branching rules and state tracking for the story.

    Attributes:
        branching_philosophy: Narrative style of branches between hard
            nodes (e.g. "Exploration vs. Combat").
        state_variables: List of variables the generator agent must
            track throughout the story.
    """

    branching_philosophy: str = Field(
        ...,
        description="Narrative style of the connective tissue between hard nodes.",
    )
    state_variables: List[StateVariable] = Field(
        ...,
        description="List of variables the Generator Agent must track.",
    )


# --- Final Root Model ---

class StoryPlotlinePlan(BaseModel):
    """The master blueprint for an interactive story using the Bottleneck
    Model.

    This is the structured output produced by the story planner agent
    and stored in the ADK session state under the ``master_plotline``
    key.

    Attributes:
        world_and_rules: World-building and tonal configuration.
        bottleneck_map: Structural backbone containing graph stats,
            title, and the 4 hard nodes.
        branching_logic: Branching rules and tracked state variables.
    """

    world_and_rules: WorldAndRules
    bottleneck_map: BottleneckMap = Field(
        ...,
        description="Structural backbone: graph stats, title, and hard nodes.",
    )
    branching_logic: BranchingLogic

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "world_and_rules": {
                    "setting": "Neo-Tokyo, 2121. Constant acid rain and neon fog.",
                    "tone_guidelines": "Hard-boiled cyberpunk. Short, punchy sentences.",
                    "core_conflict": "The OmniCorp AI Surveillance Grid.",
                },
                "bottleneck_map": {
                    "stats": {"total_levels": 6, "total_nodes": 15},
                    "title": "Neon Shadows",
                    "hard_nodes": [
                        {
                            "node_type": "Opening",
                            "node_name": "The Glitch",
                            "mandatory_event": "The player receives a ghost-signal.",
                            "key_revelation": "The signal is from their dead sibling.",
                            "exit_conditions": "Decipher the signal.",
                        },
                    ],
                },
                "branching_logic": {
                    "branching_philosophy": "Soft nodes focus on hacking vs. social manipulation.",
                    "state_variables": [
                        {
                            "variable_name": "System_Alert",
                            "type": "Integer",
                            "description": "0-100 danger level.",
                            "value": 0,
                        }
                    ],
                },
            }
        }
    )