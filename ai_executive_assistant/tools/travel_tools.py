from crewai_tools import BaseTool
import time
from utils.logging_utils import log_event

class TravelTool(BaseTool):
    name = "Travel Tool"
    description = (
        "Books flights/hotels. "
        "Inputs: destination (str), start_date (str, YYYY-MM-DD), end_date (str, YYYY-MM-DD), preferences (str, optional). "
        "Example: destination='London', start_date='2024-07-01', end_date='2024-07-04', preferences='near conference venue'"
    )
    def _run(self, destination: str, start_date: str, end_date: str, preferences: str = ""):
        print(f"\n[TravelTool] Booking for {destination} ({start_date} - {end_date}), prefs: {preferences}")
        time.sleep(1)
        result = f"Booked hotel in {destination} from {start_date} to {end_date} (prefs: {preferences})."
        log_event("tool_invocation", self.name, input={"destination": destination, "start_date": start_date, "end_date": end_date, "preferences": preferences}, output=result, status="success")
        return result
