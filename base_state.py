#base_state.py

from map import Generator

class BaseState:
    
    def __init__(self, state_manager):
        self.state_manager = state_manager  # Zugriff auf Stack/Manager, um Transitionen auszulösen

    def enter(self):
        """Wird aufgerufen, wenn der State aktiv wird (gepusht oder oben gelandet)."""
        pass

    def exit(self):
        """Wird aufgerufen, wenn der State beendet/verlassen wird (gepoppt)."""
        pass

    def update(self):
        """Hauptschleife des States: Rendern & Input verarbeiten."""
        raise NotImplementedError
    

class MainMenuState(BaseState):

    def enter(self):
        print("\n=== WILLKOMMEN ZU SLAY THE SPIRE (CLI) ===")

    def update(self):
        print("1. Neues Spiel starten")
        print("2. Beenden")
        choice = input("> ").strip()

        if choice == "1":
            # 1. Generator anwerfen und neue Karte bauen
            map_generator = Generator(width=7, height=15, paths_count=6)
            grid = map_generator.generate()

            # 2. Zum MapState wechseln
            from map_state import MapState  # Dein neuer State für die Kartenanzeige
            self.state_manager.change_state(MapState(self.state_manager, map_generator))
            return

        if choice == "2":
            self.state_manager.pop_state()  # Beendet den Stack / das Spiel
            return

        print("Ungültige Eingabe!")