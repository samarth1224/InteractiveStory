from google.adk.tools import ToolContext

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



