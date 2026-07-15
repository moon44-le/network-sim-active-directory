# card.py
from enum import Enum

# ANSI-Farbcodes für das Terminal (hier zentralisiert)
COLOR_RED = "\033[31m"      # Angriff
COLOR_BLUE = "\033[34m"     # Fertigkeit
COLOR_YELLOW = "\033[33m"   # Macht
COLOR_GREY = "\033[90m"     # Farblos / Erschöpft
COLOR_RESET = "\033[0m"     # Zurücksetzen

class CardPersistence(Enum):
    NORMAL = 1      # Wird am Rundenende abgeworfen
    ETHEREAL = 2    # Wird am Rundenende erschöpft (Flüchtig)
    RETAIN = 3      # Bleibt am Rundenende auf der Hand (Beständig)

class CardTarget(Enum):
    SELF = 1          # Spieler selbst
    SINGLE_ENEMY = 2  # Ein gezielter Gegner
    ALL_ENEMIES = 3   # Alle aktiven Gegner (AoE)

class CardType(Enum):
    

class Card:
    def __init__(self, name, cost, card_type, value, description, 
                 target_type=CardTarget.SELF, effects=None, is_colorless=False, 
                 exhausts=False, persistence=CardPersistence.NORMAL, attacks_count=1):
        self.name = name
        self.cost = cost
        self.card_type = card_type  # "Angriff", "Fertigkeit", "Macht"
        self.value = value
        self.description = description
        self.target_type = target_type
        self.effects = effects if effects is not None else []
        self.is_colorless = is_colorless
        self.exhausts = exhausts
        self.persistence = persistence
        self.attacks_count = attacks_count

    def get_colored_string(self):
        color = COLOR_GREY
        if self.is_colorless:
            color = COLOR_GREY
        elif self.card_type == "Angriff":
            color = COLOR_RED
        elif self.card_type == "Fertigkeit":
            color = COLOR_BLUE
        elif self.card_type == "Macht":
            color = COLOR_YELLOW
        
        display_keywords = []
        if self.exhausts:
            display_keywords.append("Erschöpfend")
        if self.persistence == CardPersistence.ETHEREAL:
            display_keywords.append("Flüchtig")
        elif self.persistence == CardPersistence.RETAIN:
            display_keywords.append("Beständig")
        
        kw_str = f" ({', '.join(display_keywords)})" if display_keywords else ""
        return f"{color}[{self.name}]{COLOR_RESET}{kw_str} (Kosten: {self.cost}) - {self.description}"

    def __str__(self):
        return self.get_colored_string()