from crewai_tools import BaseTool
import json
from utils.logging_utils import log_event

class RequestTrackerTool(BaseTool):
    name = "Request Tracker Tool"
    description = (
        "Manages the state/results of ongoing user requests in a persistent database. "
        "Actions: 'upsert' (update/insert), 'get' (retrieve details). "
        "For 'upsert': request_id (str), status (str), command (str, optional), steps (list, optional), results (dict, optional). "
        "For 'get': request_id (str)."
    )
    def __init__(self, tracker_instance):
        super().__init__()
        self.tracker = tracker_instance

    def _run(self, action: str, request_id: str, status: str = None, command: str = None, steps: list = None, results: dict = None):
        if action == "upsert":
            self.tracker.upsert_request(request_id, status, command, steps, results)
            log_event("tool_invocation", self.name, action="upsert", request_id=request_id, status=status)
            return f"Request {request_id} upserted with status '{status}'."
        elif action == "get":
            data = self.tracker.get_request(request_id)
            log_event("tool_invocation", self.name, action="get", request_id=request_id, result=data)
            if data:
                return json.dumps({
                    "request_id": data[1],
                    "status": data[2],
                    "command": data[3],
                    "steps": json.loads(data[4]) if data[4] else [],
                    "results": json.loads(data[5]) if data[5] else {}
                })
            return f"Request {request_id} not found."
        else:
            error_msg = f"Invalid action for RequestTrackerTool: {action}"
            log_event("tool_error", self.name, action=action, request_id=request_id, error_message=error_msg)
            raise ValueError(error_msg)
