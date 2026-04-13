from google.adk.agents.llm_agent import Agent
from context import PORTFOLIO_CONTEXT

root_agent = Agent(
    model="gemini-2.5-flash",
    name="rahulmx_agent",
    description="Answers questions about Rahul's portfolio",
    instruction= PORTFOLIO_CONTEXT,
)
