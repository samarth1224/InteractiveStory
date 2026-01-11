from typing import List, Literal, Union, Dict, Any
from pydantic import BaseModel, Field, conint

# --- Section 1: The World & Rules ---

class WorldAndRules(BaseModel):
    setting: str = Field(
        ..., 
        description="Detailed description of the geography, era, and atmosphere."
    )
    tone_guidelines: str = Field(
        ..., 
        description="Instructions for prose style (e.g., vocabulary, sentence length, mood)."
    )
    core_conflict: str = Field(
        ..., 
        description="The main antagonist or systemic force working against the player."
    )

# --- Section 2: The Bottleneck Map (The Pearls) ---

class GraphStats(BaseModel):
    total_levels: int = Field(
        ..., 
        ge=4, 
        le=10, 
        description="Total level depth of the story graph theory-wise."
    )
    total_nodes: int = Field(
        ..., 
        ge=4, 
        le=20, 
        description="Total count of inclusive soft and hard nodes."
    )

class HardNode(BaseModel):
    node_type: Literal["Opening", "Midpoint", "Climax", "Ending"] = Field(
        ..., 
        description="The structural role of this hard node."
    )
    node_name: str = Field(
        ..., 
        description="A unique, thematic name for the plot point."
    )
    mandatory_event: str = Field(
        ..., 
        description="The specific narrative event that MUST occur."
    )
    key_revelation: str = Field(
        ..., 
        description="Crucial information unlocked at this stage."
    )
    exit_conditions: str = Field(
        ..., 
        description="The state or achievement required to progress."
    )

# --- Section 3: The Branching Logic (The Strings) ---

class StateVariable(BaseModel):
    variable_name: str = Field(..., description="The unique ID of the variable.")
    type: Literal["Integer", "Boolean", "String"] = Field(..., description="The data type.")
    description: str = Field(..., description="How this variable impacts the story.")

class BranchingLogic(BaseModel):
    branching_philosophy: str = Field(
        ..., 
        description="Narrative style of the connective tissue between hard nodes."
    )
    state_variables: List[StateVariable] = Field(
        ..., 
        description="List of variables the Generator Agent must track."
    )

# --- Final Root Model ---

class StoryPlotlinePlan(BaseModel):
    """
    The master blueprint for an interactive story using the Bottleneck Model.
    Designed for a Narrative Architect Agent.
    """
    world_and_rules: WorldAndRules
    
    # Using a tuple/list structure to match your specific requirement 
    # of [GraphStats, List[HardNode]]
    bottleneck_map: List[Union[GraphStats, List[HardNode]]] = Field(
        ..., 
        description="Contains graph metadata followed by the definition of 4 Hard Nodes."
    )
    
    branching_logic: BranchingLogic

    class Config:
        json_schema_extra = {
            "example": {
                "world_and_rules": {
                    "setting": "Neo-Tokyo, 2121. Constant acid rain and neon fog.",
                    "tone_guidelines": "Hard-boiled cyberpunk. Short, punchy sentences.",
                    "core_conflict": "The OmniCorp AI Surveillance Grid."
                },
                "bottleneck_map": [
                    {"total_levels": 6, "total_nodes": 15},
                    [
                        {
                            "node_type": "Opening",
                            "node_name": "The Glitch",
                            "mandatory_event": "The player receives a ghost-signal.",
                            "key_revelation": "The signal is from their dead sibling.",
                            "exit_conditions": "Decipher the signal."
                        },
                        # ... other hard nodes
                    ]
                ],
                "branching_logic": {
                    "branching_philosophy": "Soft nodes focus on hacking vs. social manipulation.",
                    "state_variables": [
                        {"variable_name": "System_Alert", "type": "Integer", "description": "0-100 danger level."}
                    ]
                }
            }
        }