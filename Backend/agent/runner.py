"""
Agent runner and session management for the Interactive Story engine.

Provides:
- A pre-configured :class:`Runner` instance wired to the root agent.
- :func:`create_session` for initialising per-story ADK sessions.
- :func:`call_agent_async` for invoking the agent pipeline and
  extracting the structured node response.
"""

from dotenv import load_dotenv
import os

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, Session
from google.genai import types

from .agent import root_agent
from .schemas.NodeGenerator import StoryNodeGeneratorAgentResponse


APP_NAME = "Interactive Story"

session_service = DatabaseSessionService(
    db_url=os.getenv("DATABASE_URL")
)

runner = Runner(
    app_name=APP_NAME,
    session_service=session_service,
    agent=root_agent,
)


async def create_session(user_id, story_id) -> Session:
    """Create a new ADK session for a story generation run.

    Each session is scoped to one story and stores the agent's
    intermediate state (master plotline, graph-level counters, etc.)
    across multiple invocations.

    Args:
        user_id: The public UUID of the requesting user.
        story_id: A unique UUID for the new story.

    Returns:
        The newly created :class:`Session` instance.
    """
    return await session_service.create_session(
        app_name=APP_NAME,
        user_id=str(user_id),
        session_id=str(story_id),
    )


async def call_agent_async(
    prompt: str,
    runner: Runner,
    user_id,
    story_id,
) -> StoryNodeGeneratorAgentResponse:
    """Invoke the agent pipeline and return the generated story node.

    Sends *prompt* to the runner, iterates over events until the final
    response is received, validates it against
    :class:`StoryNodeGeneratorAgentResponse`, and returns it.

    Args:
        prompt: The user-facing or internal prompt string to send.
        runner: The :class:`Runner` instance to execute with.
        user_id: The user's public UUID.
        story_id: The story's public UUID / session ID.

    Returns:
        The validated :class:`StoryNodeGeneratorAgentResponse`.

    Raises:
        RuntimeError: If the agent escalates with an error or produces
            no usable final response.
    """
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(
        user_id=str(user_id),
        session_id=str(story_id),
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
                final_response = (
                    StoryNodeGeneratorAgentResponse.model_validate_json(
                        final_response_text
                    )
                )
                return final_response
            elif event.actions and event.actions.escalate:
                error_msg = (
                    event.error_message or "No specific message provided."
                )
                raise RuntimeError(
                    f"Agent escalated with error: {error_msg}"
                )

    raise RuntimeError(
        "Agent produced no final response. The pipeline may have "
        "completed without generating a story node."
    )
