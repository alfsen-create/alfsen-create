from crewai_tools import BaseTool
import time
from utils.logging_utils import log_event

class FileManagerTool(BaseTool):
    name = "File Manager Tool"
    description = (
        "Manages local files. "
        "Inputs: action (str), file_info (str). "
        "Example: action='organize', file_info='trip_docs/'"
    )
    def _run(self, action: str, file_info: str):
        print(f"\n[FileManagerTool] Performing '{action}' on {file_info}")
        time.sleep(0.5)
        result = f"File action '{action}' completed on {file_info}."
        log_event("tool_invocation", self.name, input={"action": action, "file_info": file_info}, output=result, status="success")
        return result
