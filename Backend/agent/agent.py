from google.adk.agents.llm_agent import LlmAgent
from agent.prompt import prompt_story_node_generator_agent,prompt_planner_agent
from agent.agents.root import RootAgent
from agent.tools.tools import  save_states,capture_final_response_node_generator


story_planner_agent = LlmAgent(
    model='gemini-2.5-flash',
    name = 'story_planner_agent',
    description = "Planes the story based on user's prompt. " ,
    instruction =  prompt_planner_agent,
    output_key = 'master_plotline',
    tools = [save_states]

)

story_node_generator_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'story_node_generator_agent',
    description = 'Generates the individual nodes of a story',
    instruction = prompt_story_node_generator_agent,
    tools = [capture_final_response_node_generator]
)


root_agent  = RootAgent(
    name='root_agent',
    story_planner_agent = story_planner_agent,
    story_node_generator_agent=story_node_generator_agent
)



