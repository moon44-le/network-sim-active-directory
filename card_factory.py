# card_factory.py
import copy
from card import Card
import cards_db

def create_card(card_id):
    """Sucht in allen Pools der cards_db nach der ID und gibt eine frische Card-Instanz zurück."""
    card_key = card_id.lower().strip()
    if card_key in cards_db.ALL_CARDS:
        config = copy.deepcopy(cards_db.ALL_CARDS[card_key])
        return Card(**config)
    raise ValueError(f"Karte '{card_id}' existiert in keinem Karten-Pool!")

def get_starting_deck():
    """Erstellt das offizielle Startdeck für den Eisernen."""
    starting_ids = [
        "schlag", "schlag", "schlag", "schlag",
        "verteidigung", "verteidigung", "verteidigung", "verteidigung",
        "zerschmettern"
    ]
    return [create_card(cid) for cid in starting_ids]