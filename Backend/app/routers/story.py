from fastapi import APIRouter
from app.schemas.story import StoryBase,Choice,StorySegmentPublic
import asyncio


router = APIRouter(prefix='/story')
IMAGE_URL= ''

@router.post("/generate_story",response_model=StorySegmentPublic)
async def generate_story(story: StoryBase):
    print('Request recived')
    await asyncio.sleep(5)
    response = StorySegmentPublic(content=story.story_description+'this is content',
    choices=[Choice(id=1,text='Nimade'),Choice(id=2,text='Samarth')],
    image=IMAGE_URL)
    
    return response

