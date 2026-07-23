# map_state.py

from map import Generator

class MapState(BaseState):
    def __init__(self, state_manager, map_generator):
        super().__init__(state_manager)
        self.map_generator = map_generator

    def enter(self):
        print("\nEin neues Abenteuer beginnt! Hier ist deine Karte:")

    def update(self):
        # Zeigt die ASCII-Karte an
        self.map_generator.draw_ascii_map()

        print("\nWas möchtest du tun?")
        print("1. Einen Weg wählen (Wegpunkt auf Etage 1)")
        print("2. Zurück ins Hauptmenü")
        choice = input("> ").strip()

        if choice == "1":
            # Hier startet später die Knoten-Wahl oder der direkte Übergang in den ersten Kampf!
            pass
        elif choice == "2":
            # Wechselt zurück ins Hauptmenü
            from main_menu_state import MainMenuState
            self.state_manager.change_state(MainMenuState(self.state_manager))