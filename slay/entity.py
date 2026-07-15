# entity.py
import random
import time
from card import CardPersistence
import card_factory

class Entity:
    def __init__(self, name, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.block = 0
        self.effects = {}

    def apply_effect(self, effect):
        if not effect: return
        if effect.is_instant:
            effect.trigger_instant(self)
            return

        if effect.name in self.effects:
            self.effects[effect.name].stacks += effect.stacks
            print(f"  [System] {self.name}s {effect.name} steigt auf {self.effects[effect.name].stacks}!")
            return

        self.effects[effect.name] = effect
        print(f"  [System] {self.name} erhält {effect.name} ({effect.stacks})!")

    def clean_expired_effects(self):
        expired = [name for name, eff in self.effects.items() if eff.stacks <= 0]
        for name in expired: del self.effects[name]

    def take_damage(self, damage):
        modified_damage = damage
        for eff in self.effects.values():
            modified_damage = eff.modify_damage_take(modified_damage)

        if self.block >= modified_damage:
            self.block -= modified_damage
            print(f"  {self.name} blockt den gesamten Schaden! ({self.block} Block übrig)")
            return

        remaining_damage = modified_damage - self.block
        self.block = 0
        self.hp = max(0, self.hp - remaining_damage)
        print(f"  {self.name} verliert {remaining_damage} HP! (HP: {self.hp}/{self.max_hp})")

    def add_block(self, amount):
        self.block += amount
        print(f"  {self.name} erhält {amount} Block! (Gesamtblock: {self.block})")

    def is_alive(self):
        return self.hp > 0

    def get_effects_string(self):
        if not self.effects: return ""
        eff_list = [f"{eff.name} ({eff.stacks})" for eff in self.effects.values()]
        return " | Effekte: " + ", ".join(eff_list)


class Player(Entity):
    def __init__(self, name="Der Eiserne", max_hp=80):
            super().__init__(name, max_hp)
            self.max_energy = 3
            self.energy = 3
            
            # Holt sich das saubere Startdeck aus der Factory (statt aus der db)
            self.deck = card_factory.get_starting_deck()  # <-- Hier anpassen!

            self.hand = []
            self.draw_pile = []
            self.discard_pile = []
            self.exhaust_pile = []

    def init_combat(self):
        self.draw_pile = self.deck.copy()
        random.shuffle(self.draw_pile)
        self.discard_pile, self.exhaust_pile, self.hand = [], [], []
        self.block = 0
        self.effects = {}

    def start_turn(self):
        self.energy = self.max_energy
        self.block = 0
        for eff in list(self.effects.values()): eff.on_turn_start(self)
        self.clean_expired_effects()
        
        cards_to_draw = 5 - len(self.hand)
        if cards_to_draw > 0:
            self.draw_cards(cards_to_draw)

    def end_turn(self):
        for card in list(self.hand):
            if card.persistence == CardPersistence.ETHEREAL:
                print(f"  [Flüchtig] {card.name} verflüchtigt sich und wird erschöpft!")
                self.exhaust_pile.append(card)
            elif card.persistence == CardPersistence.RETAIN:
                print(f"  [Beständig] Du behältst {card.name} auf deiner Hand.")
                continue
            else:
                self.discard_pile.append(card)
            self.hand.remove(card)
        
        for eff in list(self.effects.values()): eff.on_turn_end(self)
        self.clean_expired_effects()

    def draw_cards(self, num):
        for _ in range(num):
            if not self.draw_pile:
                self.draw_pile = self.discard_pile.copy()
                random.shuffle(self.draw_pile)
                self.discard_pile = []
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop(0))


class Enemy(Entity):
    def __init__(self, name, max_hp):
        super().__init__(name, max_hp)
        self.intent_type = None
        self.intent_value = 0

    def roll_intent(self):
        self.intent_type = "Attack" if random.random() < 0.6 else "Defend"
        self.intent_value = random.randint(5, 9)

    def show_intent(self):
        return f"Will für {self.intent_value} Schaden angreifen!" if self.intent_type == "Attack" else f"Will {self.intent_value} Block aufbauen."

    def execute_turn(self, player):
        if not self.is_alive(): return
        print(f"\n--- {self.name}s Zug ---")
        time.sleep(0.5)
        
        for eff in list(self.effects.values()): eff.on_turn_start(self)
        self.clean_expired_effects()

        if self.intent_type == "Attack":
            print(f"{self.name} greift an!")
            modified_damage = self.intent_value
            for eff in self.effects.values():
                modified_damage = eff.modify_damage_deal(modified_damage)
            player.take_damage(modified_damage)
        elif self.intent_type == "Defend":
            print(f"{self.name} bereitet sich vor.")
            self.add_block(self.intent_value)
            
        for eff in list(self.effects.values()): eff.on_turn_end(self)
        self.clean_expired_effects()