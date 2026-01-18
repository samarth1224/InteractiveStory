from google.adk.agents import BaseAgent,LlmAgent,InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
class RootAgent(BaseAgent):
    ''' root agent to orchestrate the sub agents.'''

    story_planner_agent: LlmAgent
    story_node_generator_agent: LlmAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self,name:str,
                 story_planner_agent:LlmAgent,
                 story_node_generator_agent:LlmAgent):

        sub_agents_list = [story_planner_agent,
                           story_node_generator_agent]
        
        super().__init__(name = name,
                         story_node_generator_agent=story_node_generator_agent,
                         story_planner_agent=story_planner_agent,
                         sub_agents = sub_agents_list)



    async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:


        # Call the story planner agent if theres is no plotline available
        if 'master_plotline' not in ctx.session.state or not ctx.session.state['master_plotline']:
            async for event in self.story_planner_agent.run_async(ctx):
                yield event
        # Initalize the story's graph state variable during story startup.
        if 'current_story_graph_level' and 'remaining_level_of_story_graph' not in ctx.session.state:
            # # total_levels are intialized when story planner agent is called.
            ctx.session.state['remaining_level_of_story_graph'] = ctx.session.state.get('total_levels')
            ctx.session.state['current_story_graph_level'] = 0

        # Call the Node Generator agent to generate the node.
        async for event in self.story_node_generator_agent.run_async(ctx):
            yield event









