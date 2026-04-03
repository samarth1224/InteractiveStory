from google.adk.agents.llm_agent import LlmAgent

from agent.agents.root import RootAgent
from agent.prompt import prompt_story_node_generator_agent,prompt_planner_agent
from schemas.NodeGenerator import StoryNodeGeneratorAgentResponse
from schemas.StoryPlanner import StoryPlotlinePlan
from callbacks.StoryPlannerCallbacks import save_states


story_planner_agent = LlmAgent(
    model='gemini-2.5-flash',
    name = 'story_planner_agent',
    description = "Planes the story based on user's prompt. " ,
    instruction =  prompt_planner_agent,
    output_key = 'master_plotline',
    output_schema = StoryPlotlinePlan,
    after_model_callback = save_states
)

story_node_generator_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'story_node_generator_agent',
    description = 'Generates the individual nodes of a story',
    instruction = prompt_story_node_generator_agent,
    output_schema = StoryNodeGeneratorAgentResponse
)


root_agent  = RootAgent(
    name='root_agent',
    story_planner_agent = story_planner_agent,
    story_node_generator_agent=story_node_generator_agent
)



