from crewai_tools import BaseTool
import time
from utils.logging_utils import log_event

class SchedulerTool(BaseTool):
    name = "Scheduler Tool"
    description = (
        "Schedules meetings or reminders. "
        "Inputs: event_desc (str), date_time (str, ISO8601), participants (list of str). "
        "Example: event_desc='Project Kickoff', date_time='2024-07-01T10:00:00Z', participants=['a@b.com', 'c@d.com']"
    )
    def _run(self, event_desc: str, date_time: str, participants: list):
        print(f"\n[SchedulerTool] Scheduling: '{event_desc}' at {date_time} for {participants}")
        time.sleep(1)
        result = f"Scheduled '{event_desc}' at {date_time} for {', '.join(participants)}."
        log_event("tool_invocation", self.name, input={"event_desc": event_desc, "date_time": date_time, "participants": participants}, output=result, status="success")
        return result
