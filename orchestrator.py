import sys
from enum import Enum, auto
from base_state import MainMenuState

class GameState(Enum):
    MAIN_MENU = auto()
    MAP = auto()
    COMBAT = auto()
    SHOP = auto()
    DECK_VIEW = auto()      # Overlay (z. B. Deck anschauen während der Karte oder im Kampf)
    SETTINGS = auto()       # Overlay (Einstellungen)
    GAME_OVER = auto()

class StateManager:
    def __init__(self):
        self.state_stack = []

    def push_state(self, state):
        self.state_stack.append(state)
        state.enter()

    def pop_state(self):
        if self.state_stack:
            top_state = self.state_stack.pop()
            top_state.exit()

    def change_state(self, state):
        """Ersetzt den aktuellen State durch einen neuen."""
        if self.state_stack:
            self.pop_state()
        self.push_state(state)

    def run(self):
        # Startzustand setzen
        self.push_state(MainMenuState(self))

        # Haupt-Spielschleife
        while self.state_stack:
            current_state = self.state_stack[-1]
            current_state.update()

        print("Spiel beendet. Auf Wiedersehen!")
    
    def get_current_state(self):
        # Gibt den obersten State auf dem Stack zurück (ohne ihn zu entfernen)
        return self.state_stack[-1]

    def has_states(self):
        # Prüft, ob noch mindestens ein State aktiv ist
        return len(self.state_stack) > 0


class Orchestrator:
    def __init__(self, state_manager):
        # Der Stack startet z.B. mit dem Hauptmenü
        self.state_manager = state_manager

    @property
    def current_state(self):
        # Der aktive Zustand ist immer ganz oben auf dem Stack
        return self.state_manager[-1] if self.state_manager else None

    def push_state(self, new_state: GameState):
        """Wechselt in ein Overlay (z.B. Deck-Anzeige) ohne den alten Zustand zu vergessen."""
        print(f"-> Wechsel zu: {new_state.name}")
        self.state_manager.append(new_state)

    def pop_state(self):
        """Kehrt automatisch zum vorherigen Zustand zurück."""
        if len(self.state_manager) > 1:
            removed = self.state_manager.pop()
            print(f"<- Zurück von: {removed.name} zu {self.current_state.name}")

    def change_state(self, new_state: GameState):
        """Ersetzt den aktuellen Zustand komplett (z.B. Kampf beendet -> zurück zur Map)."""
        if self.state_manager:
            self.state_manager.pop()
        self.state_manager.append(new_state)

    def run(self):
        # 1. Startzustand setzen (z. B. das Hauptmenü)
        self.state_manager.push_state(MainMenuState(self.state_manager))

        # 2. Die Haupt-Spielschleife
        while self.state_manager.has_states():
            current_state = self.state_manager.get_current_state()
            current_state.update()

        # 3. Aufräumen / Spielende
        print("Das Spiel wurde beendet. Auf Wiedersehen!")