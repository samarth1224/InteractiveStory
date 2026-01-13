from google.adk.tools.tool_context import ToolContext
from google.adk.agents.callback_context import CallbackContext
from agent.schemas.StoryPlanner import StoryPlotlinePlan
from agent.schemas.NodeGenerator import StoryNodeGeneratorAgentResponse
from typing import Dict



def final_response_planner(context:ToolContext, final_response: StoryPlotlinePlan ):
    print(type(final_response))
    print(final_response)
    return {'success': True}

def save_states(context: ToolContext, states: Dict):
    for key,value in states.items():
        print(f'{key} : {value}')
        context.state[key] = value
    return {'success': True}
def capture_final_response_node_generator(context: ToolContext, final_response: StoryNodeGeneratorAgentResponse):
    print(type(final_response))
    print(final_response)
    return {'success':True}



