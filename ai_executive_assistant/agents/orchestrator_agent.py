from crewai import Agent as CrewAgent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL_NAME
from tools.research_tools import ResearchTool
from tools.communication_tools import CommunicationTool
from tools.scheduler_tools import SchedulerTool
from tools.travel_tools import TravelTool
from tools.file_manager_tools import FileManagerTool
from tools.request_tracker_tools import RequestTrackerTool

class ExecutiveAssistantCrew:
    def __init__(self, request_tracker):
        self.tracker = request_tracker

        self.llm = ChatOpenAI(
            model=OPENAI_MODEL_NAME,
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY
        )

        self.research_tool = ResearchTool()
        self.communication_tool = CommunicationTool()
        self.scheduler_tool = SchedulerTool()
        self.travel_tool = TravelTool()
        self.file_manager_tool = FileManagerTool()
        self.request_tracker_tool = RequestTrackerTool(self.tracker)

        self.orchestrator_agent = CrewAgent(
            role='Executive Assistant Orchestrator',
            goal=(
                'Strategically break down complex user requests into sub-tasks, delegate to specialized tools, '
                'use the Request Tracker Tool for persistent state, and ensure human approval for critical steps.'
            ),
            backstory=(
                'You are the brain of an advanced AI executive assistant system. Plan, delegate, track, and automate.'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                self.research_tool,
                self.communication_tool,
                self.scheduler_tool,
                self.travel_tool,
                self.file_manager_tool,
                self.request_tracker_tool
            ]
        )

    def create_task(self, user_query: str, request_id: str) -> Task:
        return Task(
            description=(
                f"Automate: '{user_query}' for request ID: '{request_id}'.\n"
                "First, use the Request Tracker Tool to upsert the request's initial 'started' status. "
                "Think step-by-step, use the right tools, persist progress, and ask for human approval for critical steps. "
                "Send a final summary to the user."
            ),
            expected_output=(
                "A final message confirming completion, with all relevant details and approvals."
            ),
            agent=self.orchestrator_agent,
            context=[]
        )

    def create_crew(self, user_query: str, request_id: str) -> Crew:
        return Crew(
            agents=[self.orchestrator_agent],
            tasks=[self.create_task(user_query, request_id)],
            verbose=2,
            process=Process.sequential
        )
