from fastapi import APIRouter,HTTPException,Body

from ..models.storymodel import StoryPublic,Story,StoryNodePublic,StoryNode,StateVariable
from agent.runner import call_agent_async,create_session,runner

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
    try:
        session = await create_session(user_id=user_id, story_id=uuid.uuid4())
        generated_node = await call_agent_async(prompt=prompt,
                                runner=runner,
                                user_id=session.user_id,
                                story_id=session.id)
        master_plotline = session.state['master_plotline']
        if not master_plotline:
            raise HTTPException(status_code=500, detail="Agent failed to generate story.")
        first_node_state_variables = []
        for variable in master_plotline.branching_logic.state_variables:
            first_node_state_variables.append(StateVariable(
                variable_name = variable.variable_name,
                value = variable.value
            ))

        first_node = StoryNode(
            **generated_node.model_dump(),
            current_state=first_node_state_variables
        )
        new_story = Story(
            public_id = session.id,
            title=master_plotline.bottleneck_map[1].title,
            user_id=session.user_id,
            master_plotline=master_plotline,
            total_nodes=master_plotline.bottleneck_map[0].total_nodes,
            total_levels=master_plotline.bottleneck_map[0].total_levels,
            state_variable_definitions = master_plotline.branching_logic.state_variables,
            nodes = [first_node]
        )
        await new_story.insert()
        return new_story
    except RuntimeError as e:
        raise HTTPException(status_code=500,detail=e)


@router.get('/{public_story_id}/nodes', response_model=List[StoryNodePublic])
async def get_story_nodes(public_story_id: uuid.UUID):
    nodes = await Story.find_one(Story.public_id==public_story_id)
    if not nodes:
        raise HTTPException(status_code=404,detail='Story Not Found')
    return nodes.nodes

@router.get('/{public_story_id}/nodes', response_model=StoryNodePublic)
async def create_node(public_story_id: uuid.UUID, previous_node_id: str,choice_id: int):
    story = await Story.find_one(Story.public_id == public_story_id)
    previous_node = next(
        (node for node in story.nodes if node.node_id == previous_node_id),
        None
    )
    choice = previous_node.choices[choice_id-1]
    if not story:
        raise HTTPException(status_code=404,detail='Story Not Found')


    prompt = f'previous_node_id:{previous_node_id}, choice_id:{choice_id}'
    try:
        generated_node = await call_agent_async(prompt=prompt,runner=runner,user_id=user_id,story_id=public_story_id)
    except RuntimeError as e:
        raise HTTPException(status_code=500,detail=e)
    next_node = StoryNode(
        **generated_node.model_dump(),
        current_state=choice.story_state_variables
    )
    return next_node











