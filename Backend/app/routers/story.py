from fastapi import APIRouter
from app.schemas.story import StoryBase,Choice,StoryNodePublic
import asyncio


router = APIRouter(prefix='/story')
IMAGE_URL= ''

@router.post("/generate_story",response_model=StoryNodePublic)
async def generate_story(story: StoryBase):
    print('Request recived')
    response = StoryNodePublic(content=story.story_description+'this is content',
    choices=[Choice(id=1,text='Nimade'),Choice(id=2,text='Samarth')],
    image=IMAGE_URL)
    
    return response

@router.get('/get_story/{story_id}',response_model= list[StroyNodePublic])
async def get_story():
    pass

@router.get('/get_segment',response_model= StoryNodePublic)
async def get_segment():
    pass

