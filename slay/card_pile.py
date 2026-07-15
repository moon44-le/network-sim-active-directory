import random

class CardPile:
    def __init__(self, name: str, cards=None):
        self.name = name
        # Erstellt eine leere Liste, falls keine Karten übergeben wurden
        self.cards = list(cards) if cards else []

    def size(self) -> int:
        return len(self.cards)

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def add_to_bottom(self, card):
        """Fügt eine Karte unten am Stapel hinzu (z. B. für bestimmte Effekte)."""
        self.cards.insert(0, card)

    def add_to_top(self, card):
        """Fügt eine Karte oben auf dem Stapel hinzu."""
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_cards(self, num):

        for _ in range(num):
            if not self.draw_pile:
                if not self.discard_pile:
                    break  # Keine Karten mehr im Spiel
                
                self.draw_pile = self.discard_pile.copy()
                random.shuffle(self.draw_pile)
                self.discard_pile = []
            
            card_to_draw = self.draw_pile[0]
            self.transfer_card(self.draw_pile, self.hand_pile, card_to_draw)
    

    def transfer_card_to(self, target_pile, card, target_position):
        """
        Transferiert eine Karte von diesem Stapel auf einen Zielstapel.
        
        Mögliche Werte für target_position:
        - 'top': Legt die Karte ganz nach oben (Index 0).
        - 'bottom': Legt die Karte ganz nach unten (Ende der Liste).
        - 'random': Mischt die Karte an eine zufällige Position im Zielstapel.
        - int: Fügt die Karte an einem exakten Index ein.
        """
        # 1. Karte aus dem aktuellen Stapel entfernen
        if card not in self.cards:
            raise ValueError(f"Karte '{card.name}' ist nicht im Stapel '{self.name}'!")
        self.card.remove()

        # 2. Position auf dem Zielstapel bestimmen und einfügen
        match target_position:
            case "top":
                target_pile.cards.insert(0, card)
            case "bottom":
                target_pile.cards.append(card)
            case "random":
                insert_idx = random.randint(0, len(target_pile.cards))
                target_pile.cards.insert(insert_idx, card)
            case int() as idx:
                safe_idx = max(0, min(idx, len(target_pile.cards)))
                target_pile.cards.insert(safe_idx, card)
            case _:
                target_pile.cards.append(card)

        print(f"🔄 [{card.name}] transferiert: {self.name} ➡️ {target_pile.name} ({target_position})")

    def clear(self):
        """Leert den Stapel vollständig."""
        self.cards.clear()

    def __str__(self):
        return f"{self.name} ({self.size()} Karten)"