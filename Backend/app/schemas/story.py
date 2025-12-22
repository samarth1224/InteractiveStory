from pydantic import BaseModel

class StorySegmentBase(BaseModel):
    id: int
   
class StorySegment(StorySegmentBase):
    storyname: str

class StorySegmentPublic(StorySegment):
    segment: int
    choices: list[str]
    content: str
