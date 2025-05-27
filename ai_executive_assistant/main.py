import time
from utils.request_tracker import RequestTracker
from agents.logger_agent import LoggerAgent
from agents.orchestrator_agent import ExecutiveAssistantCrew

def main():
    logger_agent = LoggerAgent()
    logger_agent.start()
    tracker = RequestTracker()
    executive_assistant_crew = ExecutiveAssistantCrew(tracker)

    print("\n--- AI Executive Assistant ---\nType your command or 'exit' to quit.")
    while True:
        user_command = input("\n> You: ").strip()
        if user_command.lower() == "exit":
            break
        request_id = f"req_{int(time.time())}"
        print(f"\n--- Running for: '{user_command}' (Request ID: {request_id}) ---")
        try:
            crew = executive_assistant_crew.create_crew(user_command, request_id)
            result = crew.kickoff()
            print(f"\n--- Task Completed for {request_id} ---")
            print(result)
        except Exception as e:
            print(f"\n--- Task Failed for {request_id} ---")
            print(f"Error: {e}")
        time.sleep(1)

    logger_agent.stop()
    print("Logger stopped.")

if __name__ == "__main__":
    main()
