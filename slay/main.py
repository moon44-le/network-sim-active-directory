# main.py
from entity import Player, Enemy
from map import Level, Room
from orchestrator import Orchestrator

def main():

    orchestrator = Orchestrator()
    orchestrator.run()

if __name__ == "__main__":
    main()