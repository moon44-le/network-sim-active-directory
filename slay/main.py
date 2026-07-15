# main.py
import time
from entity import Player, Enemy
from card import CardTarget

def combat_loop(player, enemies):
    player.init_combat()
    print(f"\n⚔️ Kampf beginnt! Gegner: {', '.join([e.name for e in enemies])} ⚔️")
    
    turn = 1
    while player.is_alive() and any(e.is_alive() for e in enemies):
        active_enemies = [e for e in enemies if e.is_alive()]
        print(f"\n==================== RUNDE {turn} ====================")
        for enemy in active_enemies: 
            enemy.roll_intent()
        
        player.start_turn()
        player_acting = True

        while player_acting and any(e.is_alive() for e in active_enemies):
            active_enemies = [e for e in active_enemies if e.is_alive()]
            if not active_enemies: 
                break

            print(f"\n--- {player.name} (HP: {player.hp}/{player.max_hp} | Block: {player.block}{player.get_effects_string()} | Energie: {player.energy}/{player.max_energy}) ---")
            print("Gegner im Raum:")
            for idx, enemy in enumerate(active_enemies):
                print(f"  ({idx + 1}) {enemy.name} (HP: {enemy.hp}/{enemy.max_hp} | Block: {enemy.block}{enemy.get_effects_string()}) -> Intent: {enemy.show_intent()}")
            
            print("\nDeine Handkarten:")
            for idx, card in enumerate(player.hand): 
                print(f"  [{idx + 1}] {card}")
            
            choice = input("\nAktion (Zahl oder '0' für Zug beenden): ").strip()
            if choice == "0":
                player_acting = False
                continue

            if not choice.isdigit() or not (0 < int(choice) <= len(player.hand)):
                print("❌ Ungültige Kartenauswahl!")
                continue

            card = player.hand[int(choice) - 1]
            if player.energy < card.cost:
                print("❌ Nicht genug Energie!")
                continue

            # --- ZIELAUSWAHL ---
            target_enemies = []
            if card.target_type == CardTarget.SINGLE_ENEMY:
                target_choice = input(f"Wähle ein Ziel (1 bis {len(active_enemies)}): ").strip()
                if not target_choice.isdigit() or not (0 < int(target_choice) <= len(active_enemies)):
                    print("❌ Ungültiges Ziel!")
                    continue
                target_enemies.append(active_enemies[int(target_choice) - 1])
                
            if card.target_type == CardTarget.ALL_ENEMIES:
                target_enemies = active_enemies

            # Karte ausspielen
            player.energy -= card.cost
            player.hand.remove(card)
            print(f"\nDu spielst {card.name}!")

            # --- EFFEKT-LOGIK (ohne else) ---
            if card.card_type == "Angriff":
                for target in target_enemies:
                    for _ in range(card.attacks_count):
                        if not target.is_alive(): 
                            break
                        dmg = card.value
                        for eff in player.effects.values(): 
                            dmg = eff.modify_damage_deal(dmg)
                        target.take_damage(dmg)
                        
            if card.card_type == "Fertigkeit" and card.value > 0:
                player.add_block(card.value)

            # Effekte auf Entitäten anwenden
            for eff in card.effects:
                if card.target_type == CardTarget.SELF:
                    player.apply_effect(eff)
                    continue
                # Wenn nicht SELF, dann auf alle anvisierten Gegner anwenden
                for target in target_enemies: 
                    target.apply_effect(eff)

            # --- KARTENVERBLEIB (ohne else) ---
            if card.card_type == "Macht" or card.exhausts:
                player.exhaust_pile.append(card)
                continue
                
            player.discard_pile.append(card)

        # Gegner-Zug (Guard Clause für Schleife)
        if not any(e.is_alive() for e in active_enemies):
            continue
            
        player.end_turn()
        for enemy in active_enemies:
            enemy.execute_turn(player)
        turn += 1

    # --- KAMPF-ENDE (ohne else) ---
    if player.is_alive():
        print("\n🎉 Kampf gewonnen! Alle Gegner wurden besiegt!")
        return True
        
    print("\n💀 Game Over...")
    return False

if __name__ == "__main__":
    spieler = Player()
    gegner_gruppe = [Enemy("Schleim A", 22), Enemy("Schleim B", 14)]
    combat_loop(spieler, gegner_gruppe)