# Multi-Agent Architecture Overview

This prototype illustrates a basic multi-agent system for mold or plant disease diagnosis with optional AR tray placement.

- **DiagnosticAgent**
  - Loads the ML model and performs image classification.
- **TrayPlacementAgent**
  - Handles AR tray placement (currently a stub).
- **Controller**
  - Coordinates the agents. It runs the diagnostic agent and optionally triggers the tray placement agent depending on the command-line flag.

The architecture mirrors a simple orchestrator pattern where specialized agents focus on a single responsibility and the controller merges their actions. You can extend this design with additional agents for tasks like data logging or user interaction.
