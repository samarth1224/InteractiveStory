from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService,Session
from google.genai import types
from .schemas.NodeGenerator import StoryNodeGeneratorAgentResponse


from agents.root import RootAgent

from dotenv import load_dotenv
import os


load_dotenv()


APP_NAME = "Interactive Story"

session_service = DatabaseSessionService(
    db_url=os.getenv('DATABASE_URL')
)


runner = Runner(app_name=APP_NAME,
                session_service=session_service,
                agent=RootAgent)


async def create_session(user_id,story_id) -> Session:
    return await session_service.create_session(app_name=APP_NAME,
                                                user_id=str(user_id),
                                                session_id=str(story_id))

async def call_agent_async(prompt: str,runner: Runner, user_id, story_id):
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=str(user_id), session_id=str(story_id),new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                final_response = StoryNodeGeneratorAgentResponse.model_validate_json(final_response_text)
                return final_response
            elif event.actions and event.actions.escalate:
                error_msg = event.error_message or "No specific message provided."
                raise RuntimeError(f"Agent escalated with error: {error_msg}")
            break



