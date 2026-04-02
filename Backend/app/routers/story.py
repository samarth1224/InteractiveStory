from fastapi import APIRouter,HTTPException,Body
from beanie.operators import ElemMatch
from ..models.storymodel import StoryPublic,Story,StoryNodePublic
from typing import Annotated,List
import uuid

router = APIRouter(prefix='/story',tags=['Story'])

@router.get('/stories', response_model=List[StoryPublic])
async def get_stories():
    stories = await Story.find_all(limit=5).to_list()
    return stories


@router.get('/{public_id}', response_model=StoryPublic)
async def get_story(public_id:uuid.UUID):
    story = await Story.find_one(Story.public_id == public_id)
    if not story:
        raise HTTPException(status_code=404,detail='Story Not Found')
    return story

@router.post('/generate', response_model=StoryPublic)
async def generate_story(prompt:Annotated[str,Body()]):
    # TODO story creation logic using google ADK.
    new_story = Story()
    await new_story.insert()
    return new_story

@router.get('/{public_story_id}/nodes', response_model=List[StoryNodePublic])
async def get_story_nodes(public_story_id: uuid.UUID):
    nodes = await Story.find_one(Story.public_id==public_story_id)
    if not nodes:
        raise HTTPException(status_code=404,detail='Story Not Found')
    return nodes.nodes




