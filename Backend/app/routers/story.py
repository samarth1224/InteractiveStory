from fastapi import APIRouter,HTTPException
from ..models.storymodel import StoryPublic,Story
from typing import List
import uuid

router = APIRouter(prefix='/story',tags=['Story'])

@router.get('/stories', response_model=List[StoryPublic])
async def get_stories():
    stories = await Story.find_all(limit=5).to_list()
    return stories


@router.get('/story/{public_id}', response_model=StoryPublic)
async def get_story(public_id:uuid.UUID):
    story = await Story.find_one(Story.public_id == public_id)
    if not story:
        raise HTTPException(status_code=404,detail='Story Not Found')
    return story




