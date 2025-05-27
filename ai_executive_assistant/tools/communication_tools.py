from crewai_tools import BaseTool
import time
from utils.logging_utils import log_event

class CommunicationTool(BaseTool):
    name = "Communication Tool"
    description = (
        "Sends an email/message to a recipient. Optionally asks for human approval. "
        "Inputs: recipient (str, email or 'user'), subject (str), content (str), request_human_approval (bool, default False). "
        "Example: recipient='user@example.com', subject='Trip Results', content='Here are the hotels...', request_human_approval=True"
    )
    def _run(self, recipient: str, subject: str, content: str, request_human_approval: bool = False):
        print(f"\n[CommunicationTool] Preparing to send to {recipient}:\nSubject: {subject}\nContent: {content}\n")
        if "simulated_communication_fail" in content.lower():
            error_msg = f"Simulated comms failure to {recipient}."
            log_event("tool_error", self.name, input={"recipient": recipient, "subject": subject}, error_message=error_msg, status="failure")
            raise Exception(error_msg)
        if request_human_approval:
            print("\n[CommunicationTool] Awaiting human approval for this message:")
            print(f"  Recipient: {recipient}\n  Subject: {subject}\n  Content:\n{content}")
            while True:
                user_input = input("Approve sending? (type 'approve' or 'cancel'): ").strip().lower()
                if user_input == "approve":
                    print("[CommunicationTool] Human approved. Sending...")
                    break
                elif user_input == "cancel":
                    print("[CommunicationTool] Human cancelled. Message not sent.")
                    log_event("tool_invocation", self.name, input={"recipient": recipient, "subject": subject}, output="Cancelled by human", status="cancelled_by_human")
                    return "Message cancelled by human approval."
                else:
                    print("Invalid input. Please type 'approve' or 'cancel'.")
        time.sleep(1)
        confirmation = f"Email sent to {recipient} (Subject: {subject})."
        log_event("tool_invocation", self.name, input={"recipient": recipient, "subject": subject}, output=confirmation, status="success")
        return confirmation
