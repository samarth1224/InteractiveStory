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


    @override
    async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:

        if 'master_plotline' not in ctx.session.state or not ctx.session.state['master_plotline']:
            async for event in self.story_planner_agent.run_async(ctx):
                yield event


        async for event in self.story_node_generator_agent.run_async(ctx):
            yield event






