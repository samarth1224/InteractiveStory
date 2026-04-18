"""
Root orchestrator agent for the Interactive Story engine.

Implements a custom :class:`BaseAgent` that coordinates the story
planner and node generator sub-agents.  On the first invocation (when
no plotline exists yet) the planner runs first; on subsequent calls
only the node generator is invoked.
"""

from google.adk.agents import BaseAgent, LlmAgent, InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator


class RootAgent(BaseAgent):
    """Custom orchestrator that delegates to planner and generator agents.

    On each invocation:

    1. If ``master_plotline`` is absent from session state, run the
       **story planner** first to generate it.
    2. Initialise graph-level counters (``current_story_graph_level``,
       ``remaining_level_of_story_graph``) if they don't exist yet.
    3. Run the **story node generator** to produce the next node.

    Attributes:
        story_planner_agent: The LLM agent responsible for creating the
            master plotline.
        story_node_generator_agent: The LLM agent responsible for
            generating individual story nodes.
    """

    story_planner_agent: LlmAgent
    story_node_generator_agent: LlmAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        story_planner_agent: LlmAgent,
        story_node_generator_agent: LlmAgent,
    ):
        sub_agents_list = [story_planner_agent, story_node_generator_agent]

        super().__init__(
            name=name,
            story_node_generator_agent=story_node_generator_agent,
            story_planner_agent=story_planner_agent,
            sub_agents=sub_agents_list,
        )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Execute the orchestration logic for a single invocation.

        Args:
            ctx: The ADK invocation context carrying session state and
                message history.

        Yields:
            :class:`Event` objects produced by the delegated sub-agents.

        Raises:
            RuntimeError: If ``total_levels`` is missing from session
                state after the planner has supposedly run.
        """
        # Call the story planner agent if there is no plotline available
        if (
            "master_plotline" not in ctx.session.state
            or not ctx.session.state["master_plotline"]
        ):
            async for event in self.story_planner_agent.run_async(ctx):
                yield event

        # Initialise the story's graph state variables during story startup
        if (
            "current_story_graph_level" not in ctx.session.state
            or "remaining_level_of_story_graph" not in ctx.session.state
        ):
            total_levels = ctx.session.state.get("total_levels")
            if total_levels is None:
                raise RuntimeError(
                    "Story planner did not set 'total_levels' in session "
                    "state. Cannot initialise graph-level counters."
                )
            ctx.session.state["remaining_level_of_story_graph"] = total_levels
            ctx.session.state["current_story_graph_level"] = 0

        # Call the Node Generator agent to generate the node
        async for event in self.story_node_generator_agent.run_async(ctx):
            yield event
