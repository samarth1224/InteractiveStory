
from uuid import uuid4
from pydantic import BaseModel

class Choice(BaseModel):
    id: int
    text: str



    #Story Table and Segment Table 

# Story Table :  StoryID Name Description 
# Segment Table : SegmentID StoryID Content Choices Image


class StoryBase(BaseModel):
    story_description: str

class StoryCreate(BaseModel):
    story_description: str

class Story(StoryBase):
    story_id: uuid4
    storyname: str

class StoryNodeBase(BaseModel):
    pass


class StoryNode(StoryNodeBase):
    node_id: uuid4
    story_id: uuid4
    content: str
    choices: int
    image: str
    # previous_segment_id: uuid4

class StoryNodeCreate(StoryNodeBase):
    previous_node_choice: int

class StoryNodePublic(StoryNodeBase):
    content: str
    choices: list[Choice]
    image: str
 