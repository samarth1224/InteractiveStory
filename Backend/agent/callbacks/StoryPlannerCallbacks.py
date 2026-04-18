"""
Callbacks for the Story Planner agent.

Contains post-model callbacks that extract and persist critical
metadata from the planner's structured output into the ADK session
state.
"""

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from ..schemas.StoryPlanner import StoryPlotlinePlan


def save_states(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> None:
    """Extract graph metadata from the planner response and save to
    session state.

    Called automatically after the story planner agent produces its
    response.  Parses the raw LLM output as a
    :class:`StoryPlotlinePlan`, then writes ``total_nodes`` and
    ``total_levels`` into the session state so that downstream agents
    (and the root orchestrator) can access them.

    Args:
        callback_context: ADK callback context providing access to
            session state.
        llm_response: The raw LLM response containing the plotline
            JSON in its first text part.

    Returns:
        ``None``.  If the response has no content parts, the function
        is a no-op.
    """
    if llm_response.content and llm_response.content.parts:
        final_response_text = llm_response.content.parts[0].text
        final_response = StoryPlotlinePlan.model_validate_json(
            final_response_text
        )
        callback_context.state["total_nodes"] = (
            final_response.bottleneck_map.stats.total_nodes
        )
        callback_context.state["total_levels"] = (
            final_response.bottleneck_map.stats.total_levels
        )
    else:
        return None
