# main.py
from orchestrator import Orchestrator, StateManager


if __name__ == "__main__":
    state_manager = StateManager()
    orchestrator = Orchestrator(state_manager)
    orchestrator.run()