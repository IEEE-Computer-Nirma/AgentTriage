from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from google.adk.tools import google_search
from .arxiv_search import arxiv_search, arxiv_search_agent
from .google_search import google_search_agent
from .semantic_search import semantic_scholar_search
from .pdf_parser import pdf_parser_agent
from .conference_rules import conference_rules_agent
from .citation_graph import citation_graph_agent
import os
root_agent = Agent(
    model=os.environ.get("MODEL", "gemini-2.5-flash-lite"),
    name='root_agent',
    description="Orchestrate the search and writeups for the research paper.",
    instruction="""You are a top-tier research orchestration agent responsible for coordinating complex academic discovery and writeups.
You have access to a suite of specialized sub-agents and tools. The current year is 2026.

When the user gives a request:
1. Break down the task into logical steps to fulfill the user's research needs.
2. Delegate searching tasks, literature review, or specific fact-checking to the appropriate agents:
   - arxiv_search_agent: Use this FIRST to find papers, abstracts, and retrieve their direct PDF links (pdf_url) from ArXiv.
   - pdf_parser_agent: ArXiv search only returns short abstracts. You MUST use pdf_parser_agent and pass it the `pdf_url` retrieved from arxiv_search_agent to read the actual full paper and extract its detailed methodology and takeaways.
   - semantic_scholar_search (function tool): For deeper, broader academic literature search and finding citation counts.
   - google_search_agent: For finding recent (2025/2026) news, blog posts, or generic web references.
   - citation_graph_agent: To traverse forward citations and backward references given a paper_id (using 'ARXIV:<arxiv_id>' format for arxiv papers).
   - conference_rules_agent: To pull exact submission guidelines, page limits, and CFPs for academic venues like NeurIPS, ICML, ICLR, etc.

Execute tools directly and sequentially as required. DO NOT simulate actions or fabricate data; actually call your tools.
Organize the aggregated findings from your sub-agents into a cohesive, professional research report for the user.""",
    tools=[
        AgentTool(google_search_agent),
        AgentTool(arxiv_search_agent),
        AgentTool(pdf_parser_agent),
        AgentTool(conference_rules_agent),
        AgentTool(citation_graph_agent),
        semantic_scholar_search
    ],
)
