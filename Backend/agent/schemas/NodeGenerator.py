from pydantic import BaseModel,Field
from typing import List, Dict





class StoryStateVariables(BaseModel):
    variables: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Key-value pairs representing state updates (e.g., {'gold': 10, 'health': 24})"
    )

class Choice(BaseModel):
    text: str = Field(...,'The text displayed to the user for this choice')
    next_node_id : str =  Field(...,'The ID of the Next Node this choice will lead to')
    storystatevariables : StoryStateVariables = Field(default= StoryStateVariables,description='The state changes that occure if the choice is picked')


class StoryNodeGeneratorAgentResponse(BaseModel):

    content: str = Field(default='No content availabl', description='The content of the story node.')
    choice: List[Choice] = Field(...,max_length=2,description='A list of 2 choices available to player')
    image_prompt : str = Field(defalut='No image available', description='the prompt to generate the image for the story node.')

