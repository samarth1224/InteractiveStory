from google.adk.agents.llm_agent import LlmAgent
from prompt import prompt_story_node_generator_agent,prompt_planner_agent


story_planner_agent = LlmAgent(
    model='gemini-2.5-flash',
    name = 'story_planner_agent',
    description = "Planes the story based on user's prompt. " ,
    instruction =  prompt_planner_agent,
    output_key = 'master_plotline'

)

story_node_generator_agent = LlmAgent(
    model = 'gemini-2.5-flash',
    name = 'story_node_generator_agent',
    description = 'Generates the individual nodes of a story',
    instruction = prompt_story_node_generator_agent
)




