from google import genai
from google.genai import types
from fastapi import APIRouter
from app.schemas.story import StoryCreate
from app.schemas.story import StorySegmentPublic


router = APIRouter(prefix='story')

create_segment_image_function = {
    "name": "create_segment_image",
    "description": "Creates Image of a Story Segment based on the prompt provided by LLM",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Prompt to Create a Story segment",
            },
        },
        "required": ['prompt'],
    },
}

client = genai.Client(api_key="AIzaSyDqeDBzNbtryW0jm6sVvcPYYeIL8KCPVbk")
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])


@router.post("/generate_story",response_model=StorySegmentPublic)
async def generate_story(story: StoryCreate):
    
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Generate a story about {story.story_description}. Also create two choices to choose from for deciding further story direction.Also create a prompt for creation of image based on the story segment.",
    config=config,
    )

    
    return response

