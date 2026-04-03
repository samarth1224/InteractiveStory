from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from ..schemas.StoryPlanner import StoryPlotlinePlan


def save_states(callback_context: CallbackContext, llm_response :LlmResponse):
    """
      To save the states when agent wants to update them
    """
    if llm_response.content and llm_response.content.parts:
        final_response_text = llm_response.content.parts[0].text
        final_response = StoryPlotlinePlan.model_validate_json(final_response_text)
        callback_context.state['total_nodes'] = final_response.bottleneck_map[0].total_nodes
        callback_context.state['total_levels'] = final_response.bottleneck_map[0].total_levels
    else:
        return None






