"""
Story router — CRUD and AI generation of interactive stories.

Provides endpoints for listing, retrieving, and generating stories, as
well as creating new story nodes when the reader makes a choice.
"""

from app.models.storymodel import StoryPublic, Story, StoryNodePublic, StoryNode, StateVariable
from app.models.usermodel import User
from app.utility.dependencies import verify_user_access_token

from agent.runner import call_agent_async, create_session, runner

from fastapi import APIRouter, HTTPException, Body, Depends

from typing import Annotated, List
import uuid

VerifyUserTokenDep = Annotated[User, Depends(verify_user_access_token)]

router = APIRouter(prefix="/story", tags=["Story"])


@router.get("/stories", response_model=List[StoryPublic])
async def get_stories(user: VerifyUserTokenDep) -> List[StoryPublic]:
    """List all stories owned by the authenticated user.

    Queries MongoDB for every :class:`Story` document whose
    ``user_id`` matches the caller's ``public_id``.

    Args:
        user: The authenticated user (injected via dependency).

    Returns:
        A list of :class:`StoryPublic` summaries.
    """
    stories = await Story.find(Story.user_id == str(user.public_id)).to_list()
    return stories


@router.get("/{public_id}", response_model=StoryPublic)
async def get_story(public_id: uuid.UUID) -> StoryPublic:
    """Retrieve a single story by its public UUID.

    Args:
        public_id: The story's public UUID (path parameter).

    Returns:
        The matching :class:`StoryPublic` summary.

    Raises:
        HTTPException: 404 if no story with the given ID exists.
    """
    story = await Story.find_one(Story.public_id == public_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story Not Found")
    return story


@router.post("/generate", response_model=StoryPublic)
async def generate_story(
    user: VerifyUserTokenDep,
    prompt: Annotated[str, Body()],
) -> StoryPublic:
    """Generate a brand-new interactive story from a user prompt.

    Delegates to the AI agent to produce a master plotline and the
    first story node, then persists the resulting :class:`Story`
    document.

    Args:
        user: The authenticated user (injected via dependency).
        prompt: Free-text description of the desired story.

    Returns:
        The newly created :class:`StoryPublic` summary.

    Raises:
        HTTPException: 500 if the agent fails to produce a valid
            story or an unexpected runtime error occurs.
    """
    try:
        session = await create_session(
            user_id=user.public_id, story_id=uuid.uuid4()
        )
        generated_node = await call_agent_async(
            prompt=prompt,
            runner=runner,
            user_id=session.user_id,
            story_id=session.id,
        )
        master_plotline = session.state["master_plotline"]
        if not master_plotline:
            raise HTTPException(
                status_code=500, detail="Agent failed to generate story."
            )

        first_node_state_variables = [
            StateVariable(
                variable_name=variable.variable_name,
                value=variable.value,
            )
            for variable in master_plotline.branching_logic.state_variables
        ]

        first_node = StoryNode(
            **generated_node.model_dump(),
            current_state=first_node_state_variables,
        )
        new_story = Story(
            public_id=session.id,
            title=master_plotline.bottleneck_map.title,
            user_id=session.user_id,
            master_plotline=master_plotline,
            total_nodes=master_plotline.bottleneck_map.stats.total_nodes,
            total_levels=master_plotline.bottleneck_map.stats.total_levels,
            state_variable_definitions=master_plotline.branching_logic.state_variables,
            nodes=[first_node],
        )
        await new_story.insert()
        return new_story
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{public_story_id}/nodes", response_model=List[StoryNodePublic])
async def get_story_nodes(
    public_story_id: uuid.UUID,
) -> List[StoryNodePublic]:
    """Retrieve all generated nodes for a given story.

    Args:
        public_story_id: The story's public UUID (path parameter).

    Returns:
        An ordered list of :class:`StoryNodePublic` nodes.

    Raises:
        HTTPException: 404 if no story with the given ID exists.
    """
    story = await Story.find_one(Story.public_id == public_story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story Not Found")
    return story.nodes


@router.post("/{public_story_id}/create_node", response_model=StoryNodePublic)
async def create_node(
    user: VerifyUserTokenDep,
    public_story_id: uuid.UUID,
    previous_node_id: str,
    choice_id: int,
) -> StoryNodePublic:
    """Create the next story node based on a reader's choice.

    Looks up the story and the node the reader just finished, validates
    the chosen option, invokes the AI agent to generate a continuation,
    persists the new node, and returns it.

    Args:
        user: The authenticated user (injected via dependency).
        public_story_id: The story's public UUID (path parameter).
        previous_node_id: ``node_id`` of the node the reader just read.
        choice_id: 1-based index of the selected choice.

    Returns:
        The newly generated :class:`StoryNodePublic` node.

    Raises:
        HTTPException: 404 if the story or previous node is not found.
        HTTPException: 400 if the choice_id is invalid.
        HTTPException: 500 if the agent encounters a runtime error.
    """
    story = await Story.find_one(Story.public_id == public_story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story Not Found")

    previous_node = next(
        (node for node in story.nodes if node.node_id == previous_node_id),
        None,
    )
    if not previous_node:
        raise HTTPException(status_code=404, detail="Previous node not found")

    if choice_id < 1 or choice_id > len(previous_node.choices):
        raise HTTPException(status_code=400, detail="Invalid choice_id")

    choice = previous_node.choices[choice_id - 1]

    prompt = f"previous_node_id:{previous_node_id}, choice_id:{choice_id}"
    try:
        generated_node = await call_agent_async(
            prompt=prompt,
            runner=runner,
            user_id=str(user.public_id),
            story_id=public_story_id,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    next_node = StoryNode(
        **generated_node.model_dump(),
        current_state=choice.story_state_variables,
    )

    # Persist the new node to the database
    story.nodes.append(next_node)
    await story.save()

    return next_node
