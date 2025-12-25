from click.decorators import pass_context
from uuid import uuid4
from pydantic import BaseModel

class Choice(BaseModel):
    id: int
    text: str

class StoryCreate(BaseModel):
    story_description: str

# class StorySegmentBase(BaseModel):
#     id: int

# class StoryCreate(StorySegmentBase):
#     story_description: str
   
# class StorySegment(StorySegmentBase):
#     storyname: str

# class StorySegementCreate(StorySegmentBase):
#     choices: int

# class StorySegmentPublic(StorySegmentBase):
#     segment: int
#     choices: list[str]
#     content: str
#     image: str




 

    #Story Table and Segment Table 

# Story Table :  StoryID Name Description 
# Segment Table : SegmentID StoryID Content Choices Image


class StoryBase(BaseModel):
    story_description: str

# class StoryCreate(StoryBase):
#     pass

class Story(StoryBase):
    story_id: uuid4
    storyname: str

class StorySegmentBase(BaseModel):
    pass


class StorySegment(StorySegmentBase):
    segment_id: uuid4
    story_id: uuid4
    content: str
    choices: int
    image: str
    # previous_segment_id: uuid4

class StorySegmentCreate(StorySegmentBase):
    previous_segment_choice: int

class StorySegmentPublic(StorySegmentBase):
    content: str
    choices: list[Choice]
    image: str
 