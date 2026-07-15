# effect.py

class Effect:
    def __init__(self, name, stacks, is_instant=False):
        self.name = name
        self.stacks = stacks
        self.is_instant = is_instant

    def modify_damage_deal(self, damage): return damage
    def modify_damage_take(self, damage): return damage
    def on_turn_start(self, entity): pass
    def on_turn_end(self, entity): pass
    def trigger_instant(self, entity): pass


class VulnerableEffect(Effect):
    def __init__(self, stacks):
        super().__init__("Verwundbar", stacks)

    def modify_damage_take(self, damage):
        print(f"  [Effekt] Verwundbar erhöht den erlittenen Schaden um 50%!")
        return int(damage * 1.5)

    def on_turn_end(self, entity):
        self.stacks -= 1
        if self.stacks <= 0:
            print(f"  [Effekt] {entity.name} ist nicht mehr verwundbar.")


class StrengthEffect(Effect):
    def __init__(self, stacks):
        super().__init__("Stärke", stacks)

    def modify_damage_deal(self, damage):
        print(f"  [Effekt] Stärke erhöht den ausgeteilten Schaden um +{self.stacks}!")
        return damage + self.stacks


class ZuwachsEffect(Effect):
    def __init__(self, stat_name, stacks_per_turn):
        super().__init__(f"Zuwachs_{stat_name}", stacks_per_turn)
        self.stat_name = stat_name

    def on_turn_start(self, entity):
        print(f"  [Macht] {self.name} triggert!")
        if self.stat_name == "Stärke":
            entity.apply_effect(StrengthEffect(self.stacks))


class HealEffect(Effect):
    def __init__(self, amount):
        super().__init__("Heilung", amount, is_instant=True)

    def trigger_instant(self, entity):
        entity.hp = min(entity.max_hp, entity.hp + self.stacks)
        print(f"  💖 Heilung! {entity.name} regeneriert {self.stacks} HP.")


class BufferEffect(Effect):
    def __init__(self, stacks):
        super().__init__("Puffer", stacks)

    def modify_damage_take(self, damage):
        if damage > 0:
            print(f"  🛡️ [Puffer] Der Effekt absorbiert den gesamten Schaden von {damage}!")
            self.stacks -= 1
            return 0
        return damage