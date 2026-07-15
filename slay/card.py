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
    ETHEREAL = 2    # Flüchtig
    RETAIN = 3      # Beständig

class CardTarget(Enum):
    SELF = 1          # Spieler selbst
    SINGLE_ENEMY = 2  # Ein gezielter Gegner
    ALL_ENEMIES = 3   # Alle aktiven Gegner (AoE)

class CardType(Enum):
    ATTACK = 1      # Angriff
    SKILL = 2       # Fertigkeit
    POWER = 3       # Macht
    STATUS = 4      # Status
    CURSE = 5       # Fluch
    TRUNK = 6       # Tränke

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

    def get_card_color(self):
        match self.card_type:
            case CardType.ATTACK:   return COLOR_RED
            case CardType.SKILL:    return COLOR_BLUE
            case CardType.POWER:    return COLOR_YELLOW
            case CardType.POWER:    return COLOR_GREY
            case _:                 return COLOR_GREY

    def get_colored_string(self):
        display_keywords = []
        kw_str = f" ({', '.join(display_keywords)})" if display_keywords else ""   
        return f"{self.get_card_color()}[{self.name}]{COLOR_RESET}{kw_str} (Kosten: {self.cost}) - {self.description}"

    def __str__(self):
        return self.get_colored_string()