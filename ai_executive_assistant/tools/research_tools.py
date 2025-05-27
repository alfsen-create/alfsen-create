from crewai_tools import BaseTool
import time
from utils.logging_utils import log_event

class ResearchTool(BaseTool):
    name = "Research Tool"
    description = (
        "Performs web research using an API. "
        "Input: query (str): what to search for.\n"
        "Example: query='business hotels in London for business travel July 2024'"
    )
    def _run(self, query: str):
        print(f"\n[ResearchTool] Searching: '{query}'...")
        if "simulated_research_fail" in query.lower():
            error_msg = f"Simulated research failure for query: '{query}'."
            log_event("tool_error", self.name, input={"query": query}, error_message=error_msg, status="failure")
            raise Exception(error_msg)
        time.sleep(1.5)
        findings = (
            f"Top business hotels in London: Canary Riverside, The Savoy, and The Ned. "
            f"(Simulated research for: {query})"
        )
        log_event("tool_invocation", self.name, input={"query": query}, output=findings, status="success")
        return findings
