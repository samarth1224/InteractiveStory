# Output Schemas for NodeGenerator agent.

from pydantic import BaseModel,Field
from typing import List, Dict,Any

class StoryStateVariables(BaseModel):
    variable_name: str = Field(..., description="The unique ID of the variable.")
    value: Any = Field(..., description='The initial value of this state variable. Its type is same as attribute type')


class Choice(BaseModel):
    text: str = Field('The text displayed to the user for this choice')
    next_node_id: str = Field('The ID of the Next Node this choice will lead to')
    story_state_variables: List[StoryStateVariables] = Field(description='The state changes that occure if the choice is picked')

class StoryNodeGeneratorAgentResponse(BaseModel):
    node_id: str
    level: int
    content: str = Field(default='No content available', description='The content of the story node.')
    choices: List[Choice] = Field(default_factory= list,max_length=2,description='A list of 2 choices available to player')
    image_prompt: str = Field(defalut='No image available', description='the prompt to generate the image for the story node.')



