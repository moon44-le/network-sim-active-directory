# main.py
from entity import Player, Enemy
from map import Level, Room
from orchestrator import Orchestrator

def build_act_one() -> Level:
    """Generiert die feste Struktur für das erste Level (Act 1)."""
    act1 = Level(act_number=1, name="Die Ruinen")

    # --- Floor 1: Erste Verzweigung (Zwei optionale leichte Kämpfe) ---
    floor_1_rooms = [
        Room(room_type="combat", enemies=[Enemy("Schleim A", 22), Enemy("Schleim B", 14)]),
        Room(room_type="combat", enemies=[Enemy("Wandernde Laus", 18)])
    ]
    act1.add_floor(1, floor_1_rooms)

    # --- Floor 2: Zweite Verzweigung (Ein schwererer Kampf oder eine Pause) ---
    floor_2_rooms = [
        Room(room_type="combat", enemies=[Enemy("Kultist", 48)]),
        Room(room_type="campfire")  # Ein Lagerfeuer als alternative Abzweigung!
    ]
    act1.add_floor(2, floor_2_rooms)

    # --- Floor 3: Bosskampf (Keine Verzweigung, nur ein Raum) ---
    floor_3_rooms = [
        Room(room_type="combat", enemies=[Enemy("Der Wachposten (Boss)", 120)], name="👹 BOSS: Wachposten")
    ]
    act1.add_floor(3, floor_3_rooms)

    return act1


def main():
    # 1. Level-Struktur generieren (Gegner stehen hier bereits fest!)
    act_one_map = build_act_one()

    # 2. Orchestrator instanziieren und die generierte Map übergeben
    orchestrator = GameOrchestrator(game_map=act_one_map)
    
    # 3. Wasserfall starten
    orchestrator.run()

if __name__ == "__main__":
    main()