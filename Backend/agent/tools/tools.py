from google.adk.tools.tool_context import ToolContext
from agent.schemas.NodeGenerator import StoryNodeGeneratorAgentResponse
from typing import Dict


def save_states(context: ToolContext, states: Dict):
    """
      To save the states when agent wants to update them
      Args:
          states (dict) : states in a key-value pair to update or create them.
      """
    for key,value in states.items():
        print(f'{key} : {value}')
        context.state[key] = value
    return {'success': True}
def capture_final_response_node_generator(context: ToolContext, final_response: StoryNodeGeneratorAgentResponse):
    """
      Tool to capture the final response of the agent in a structured way
      Args:
          final_response (StoryNodeGeneratorAgentResponse): Final response of the agent
                                              containing content,choices and image prompt
      """
    print(type(final_response))
    print(final_response)
    return {'success':True}



