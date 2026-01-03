from google.adk.tools.tool_context import ToolContext
from google.adk.agents.callback_context import CallbackContext



def before_callback_segment(context:CallbackContext):
    context.state['current_node_number'] += 1
    context.state['remaining_nodes'] -= 1
    return None

def save_story_state(context:ToolContext,**kwargs):
    for state,value in kwargs.items():
        context.state[state] = value
    return True


def generate_image(context:ToolContext):
    pass



