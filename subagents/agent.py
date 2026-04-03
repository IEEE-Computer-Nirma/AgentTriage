from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from google.adk.tools import google_search
from arxiv_search import arxiv_search
from google_search import google_search_agent
from semantic_search import semantic_scholar_search
from pdf_parser import pdf_parser_agent
from conference_rules import conference_rules_agent
from citation_graph import citation_graph_agent
from subagents.arxiv_search import arxiv_search_agent

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description="Orchestrate the search and writeups for the research paper.",
    instruction="",
    tools=[
        AgentTool(google_search_agent),
        AgentTool(arxiv_search_agent),
        AgentTool(pdf_parser_agent),
        AgentTool(conference_rules_agent),
        AgentTool(citation_graph_agent),
        semantic_scholar_search
    ],
)