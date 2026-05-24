"""Story router — CRUD and AI generation of interactive stories."""

from app.models.storymodel import StoryPublic, Story, StoryNodePublic, StoryNode, StateVariable
from app.models.usermodel import User
from app.utility.dependencies import verify_user_access_token

from agent.runner import call_agent_async, create_session, runner
from agent.schemas.StoryPlanner import StoryPlotlinePlan
from agent.schemas.NodeGenerator import StoryNodeGeneratorAgentResponse

from fastapi import APIRouter, HTTPException, Body, Depends

from typing import Annotated, List, Dict
import uuid

VerifyUserTokenDep = Annotated[User, Depends(verify_user_access_token)]

router = APIRouter(prefix="/story", tags=["Story"])


@router.get("/stories", response_model=List[StoryPublic])
async def get_stories() -> List[StoryPublic]:
    """List all stories from all users (limit to 10 latest)."""
    # Sort by database ID descending to get the most recent, and limit to 10
    stories = await Story.find_all().sort("-id").limit(10).to_list()
    return stories


@router.get("/stories/my", response_model=List[StoryPublic])
async def get_my_stories(user: VerifyUserTokenDep) -> List[StoryPublic]:
    """List all stories owned by the authenticated user."""
    stories = await Story.find(Story.user_id == user.public_id).sort("-id").to_list()
    return stories


@router.get("/{public_id}", response_model=StoryPublic)
async def get_story(public_id: uuid.UUID) -> StoryPublic:
    """Retrieve a single story by its public UUID."""
    story = await Story.find_one(Story.public_id == public_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story Not Found")
    print(story.state_variable_definitions)
    return story


@router.post("/generate", response_model=Story)
async def generate_story(
    user: VerifyUserTokenDep,
    prompt: Annotated[str, Body()],
) -> StoryPublic:
    """Generate a brand-new interactive story from a user prompt."""
    try:
        story_id = uuid.uuid4()
        await create_session(
            user_id=user.public_id, story_id=story_id
        )
        async for response in call_agent_async(
            prompt=prompt,
            runner=runner,
            user_id=user.public_id,
            story_id=story_id,
        ):

            if isinstance(response, StoryPlotlinePlan):
                master_plotline = response
            if isinstance(response, StoryNodeGeneratorAgentResponse):
                generated_node = response

        if master_plotline is None or generated_node is None:
            raise HTTPException(
                status_code=500, detail="Agent failed to generate story."
            )

        first_node_state_variables = [
            variable.model_dump()
            for variable in master_plotline.branching_logic.state_variables
        ]
        first_node = StoryNode(
            **generated_node.model_dump(),
        )
        new_story = Story(
            public_id=story_id,
            title=master_plotline.bottleneck_map.title,
            summary=master_plotline.bottleneck_map.summary,
            user_id=user.public_id,
            master_plotline=master_plotline.model_dump(),
            total_nodes=master_plotline.bottleneck_map.stats.total_nodes,
            total_levels=master_plotline.bottleneck_map.stats.total_levels,
            state_variable_definitions=first_node_state_variables,
            nodes={first_node.node_id: first_node},
        )
        await new_story.insert()
        return new_story
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{public_story_id}/nodes", response_model=Dict[str, StoryNodePublic])
async def get_story_nodes(
    public_story_id: uuid.UUID,
) -> Dict[str, StoryNodePublic]:
    """Retrieve all generated nodes for a given story."""
    story = await Story.find_one(Story.public_id == public_story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story Not Found")
    return story.nodes


@router.post("/{public_story_id}/create_node", response_model=StoryNodePublic)
async def create_node(
    user: VerifyUserTokenDep,
    public_story_id: uuid.UUID,
    previous_node_id: Annotated[str, Body()],
    choice_id: Annotated[int, Body()],
) -> StoryNodePublic:
    """Create the next story node based on a reader's choice."""
    story = await Story.find_one(Story.public_id == public_story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story Not Found")

    previous_node = story.nodes.get(previous_node_id)
    if not previous_node:
        raise HTTPException(status_code=404, detail="Previous node not found")

    if choice_id < 1 or choice_id > len(previous_node.choices):
        raise HTTPException(status_code=400, detail="Invalid choice_id")

    choice = previous_node.choices[choice_id - 1]

    # If the target node has already been generated, return it directly
    existing_node = story.nodes.get(choice.next_node_id)
    if existing_node:
        return existing_node

    prompt = f"previous_node_id:{previous_node_id}, choice_id:{choice_id}"
    try:
        async for response in call_agent_async(
            prompt=prompt,
            runner=runner,
            user_id=str(user.public_id),
            story_id=public_story_id,
        ):
            if isinstance(response, StoryNodeGeneratorAgentResponse):
                generated_node = response
            else: continue
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if generated_node is None:
        raise HTTPException(status_code=500, detail="Agent failed to generate story.")

    next_node = StoryNode(
        **generated_node.model_dump(),
    )

    # Persist the new node to the database
    story.nodes[next_node.node_id] = next_node
    await story.save()

    return next_node
