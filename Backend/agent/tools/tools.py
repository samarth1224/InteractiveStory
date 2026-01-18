from google.adk.tools import ToolContext
from agent.schemas.NodeGenerator import StoryNodeGeneratorAgentResponse



def save_states(tool_context: ToolContext, states: dict):
    """
      To save the states when agent wants to update them
      Args:
          states (dict) : states in a key-value pair to update or create them.
      """
    try:
        for key,value in states.items():
            print(f'{key} : {value}')
            tool_context.state[key] = value
        return {'success': True}
    except Exception as e:
        return {'success':False,'error': e}

def capture_final_response_node_generator(final_response: StoryNodeGeneratorAgentResponse):
    """
      Tool to capture the final response of the agent in a structured way
      Args:
          final_response (StoryNodeGeneratorAgentResponse): Final response of the agent
                                              containing content,choices and image prompt
      """
    try:
        print(type(final_response))
        print(final_response)
        return {'success':True}
    except Exception as e:
        return {'success':False,'error': e}



