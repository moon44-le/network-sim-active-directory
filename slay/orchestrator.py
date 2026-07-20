import sys
from card_factory import get_starting_deck


class GamePhase(Enum):
    START       = 1  # Start
    CHOOSECHAR  = 2  # Charakterwahl
    NODE        = 4  # Kampf, Shop, Event
    FINISH      = 5  # Sieg, Niederlage

class GameObject(Enum):
    MAP = 1
    CARDS = 2
    MENU = 3


class Orchestrator:
    def __init__(self):
        self.player = None
        self.game_map = None        # Enthält alle fertig initialisierten Ebenen/Gegner
        self.current_floor = 1
        self.current_node = None    # Die aktuell ausgewählte Abzweigung/Node
        self.active_enemies = []    # Die Gegner für den aktuellen Kampf
        self.game_active = True

    def run(self):
        """Startet den sequentiellen Wasserfall-Prozess des Spiels."""
        print("🎮 Starte Slay the Spire (CLI-Edition)...")
        
        # --- PHASE 1: EINMALIGES SETUP ---
        self._phase_character_selection()
        
        # --- DER SPIEL-LOOP (Sequentieller Wasserfall pro Ebene) ---
        while self.game_active and self.player.is_alive():
            
            # --- PHASE 2: WEG-ENTSCHEIDUNG ---
            # Ermittelt die Node (und damit die feststehenden Monster) für diesen Schritt
            self._phase_path_decision()
            
            # Falls die Node ein Kampf ist, führen wir den Kampf-Wasserfall aus
            if self.current_node.type == "combat":
                self._phase_pre_combat_setup()
                combat_won = self._phase_combat_loop()
                
                if combat_won:
                    self._phase_post_combat_resolution()
                else:
                    self._phase_game_over()
                    break
            
            # Fortschritt zur nächsten logischen Ebene im Wasserfall
            self.current_floor += 1

    # ==========================================
    # PHASE 1: CHARAKTERAUSWAHL & SETUP
    # ==========================================
    def _phase_character_selection(self):
        print("\n--- [PHASE 1: CHARAKTERAUSWAHL] ---")
        print("-> Automatische Auswahl: Der Eiserne")
        
        # Spieler-Instanz (wurde in main.py vorbereitet oder hier erzeugt)
        from entity import Player
        self.player = Player()
        
        # Startdeck zuweisen
        starting_cards = get_starting_deck()
        for card in starting_cards:
            self.player.draw_pile.add_card(card)
            
        print(f"英雄 {self.player.name} wurde mit {len(starting_cards)} Karten im Deck erstellt!")

    # ==========================================
    # PHASE 2: PFAD-ENTSCHEIDUNG (Keine Gegner-Init mehr!)
    # ==========================================
    def _phase_path_decision(self):
        print(f"\n--- [PHASE 2: ENTSCHEIDUNG EBENE {self.current_floor}] ---")
        
        # Wir holen uns die Abzweigungen für die aktuelle Ebene aus unserer Map
        available_nodes = self.game_map.get_nodes_for_floor(self.current_floor)
        
        print("Wähle deinen Weg auf dieser Ebene:")
        for idx, node in enumerate(available_nodes):
            # node.enemies enthält bereits die fertig initialisierten Gegner-Objekte!
            enemy_names = ", ".join([e.name for e in node.enemies])
            print(f"  {idx}: Weg {idx + 1} -> {node.display_name()} (Gegner: {enemy_names})")
            
        # Spieler wählt seinen Pfad
        while True:
            try:
                choice = int(input("Dein Weg: "))
                self.current_node = available_nodes[choice]
                break
            except (ValueError, IndexError):
                print("❌ Ungültige Abzweigung! Bitte wähle eine der angezeigten Nummern.")
        
        # Die Gegner für diesen Kampf stehen nun fest:
        self.active_enemies = self.current_node.enemies
        print(f"\n➡️ Du hast den Weg gewählt. Ein Kampf gegen {', '.join([e.name for e in self.active_enemies])} beginnt!")

    # ==========================================
    # PHASE 3: KAMPF-VORBEREITUNG
    # ==========================================
    def _phase_pre_combat_setup(self):
        print("\n--- [PHASE 3: KAMPF-VORBEREITUNG] ---")
        
        self.player.discard_pile.clear()
        self.player.hand.clear()
        
        self.player.reset_deck_for_combat() 
        self.player.draw_pile.shuffle()
        
        # Block-Effekt (falls vorhanden) zu Kampfbeginn löschen
        if "block" in self.player.effects:
            self.player.modify_block(-self.player.block)
            
        print("🃏 Deck wurde gemischt. Bereit zum Kampf!")

    # ==========================================
    # PHASE 4: DER KAMPF (COMBAT LOOP)
    # ==========================================
    def _phase_combat_loop(self) -> bool:
        print("\n--- [PHASE 4: KAMPF BEGONNEN] ---")
        turn = 1
        
        while self.player.is_alive() and any(e.is_alive() for e in self.active_enemies):
            print(f"\n--- RUNDE {turn} ---")
            
            # 1. ZUG-START (Gegner-Absichten rollen)
            alive_enemies = [e for e in self.active_enemies if e.is_alive()]
            for enemy in alive_enemies:
                enemy.roll_intent()
                enemy.display_intent()

            self.player.start_turn()

            # 2. SPIELER-ZUG
            self._player_turn_input_loop(alive_enemies)

            # 3. SPIELER-ZUGENDE
            self.player.end_turn()

            # 4. GEGNER-ZÜGE
            alive_enemies = [e for e in self.active_enemies if e.is_alive()]
            for enemy in alive_enemies:
                if enemy.is_alive() and self.player.is_alive():
                    enemy.execute_turn(self.player)

            # 5. RUNDEN-ENDE
            self.player.update_effects_at_turn_end()
            for enemy in alive_enemies:
                enemy.update_effects_at_turn_end()

            turn += 1

        return self.player.is_alive()

    def _player_turn_input_loop(self, alive_enemies):
        """Interne Hilfsmethode für den Spieler-Input im Kampf."""
        while True:
            self.player.display_status()
            for i, enemy in enumerate(alive_enemies):
                print(f"[{i}] {enemy.name} (HP: {enemy.hp}/{enemy.max_hp}) - Absicht: {enemy.intent_type}")
            
            print("\nVerfügbare Handkarten:")
            for i, card in enumerate(self.player.hand.cards):
                print(f"  {i}: {card}")
            
            choice = input("\nKarten-Index eingeben (oder 'e' für Zug beenden): ").strip()
            
            if choice.lower() == 'e':
                break
                
            try:
                card_index = int(choice)
                card = self.player.hand.cards[card_index]
                
                target = None
                if len(alive_enemies) == 1:
                    target = alive_enemies[0]
                elif len(alive_enemies) > 1:
                    target_idx = int(input("Wähle Ziel-Gegner (Index): "))
                    target = alive_enemies[target_idx]
                
                if self.player.play_card(card, target):
                    self.player.hand.transfer_card(self.player.discard_pile, card)
                    if not any(e.is_alive() for e in alive_enemies):
                        break
            except (ValueError, IndexError) as e:
                print(f"❌ Ungültige Eingabe: {e}")

    # ==========================================
    # PHASE 5: POST-COMBAT ODER GAME OVER
    # ==========================================
    def _phase_post_combat_resolution(self):
        print("\n--- [PHASE 5: KAMPF GEWONNEN!] ---")
        print("🎉 Alle Gegner wurden bezwungen!")
        print("🎁 Du erhältst: Gold und Kartenoptionen.")
        input("\nDrücke ENTER, um fortzufahren...")

    def _phase_game_over(self):
        print("\n💀 --- GAME OVER --- 💀")
        self.game_active = False