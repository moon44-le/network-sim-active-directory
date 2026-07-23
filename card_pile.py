import random

class CardPile:
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def shuffle(self):
        """Mischt die Karten im Stapel."""
        random.shuffle(self.cards)

    def clear(self):
        """Leert den Stapel komplett."""
        self.cards.clear()

    def add(self, card, position: int = None):
        """Fügt eine Karte hinzu (Standard: am Ende / oben auf dem Stapel)."""
        if position is not None:
            self.cards.insert(position, card)
        else:
            self.cards.append(card)

    def remove(self, card):
        """Entfernt eine bestimmte Karte aus dem Stapel."""
        if card not in self.cards:
            raise ValueError(f"Karte '{card.name}' ist nicht im Stapel '{self.name}'!")
        self.cards.remove(card)

    def pop_top(self):
        """Zieht die oberste Karte (vom Ende der Liste) und gibt sie zurück."""
        if not self.cards:
            raise IndexError(f"Stapel '{self.name}' ist leer!")
        return self.cards.pop()

    def transfer_card(self, target_pile: "CardPile", card, target_position: int = None):
        """Transferiert eine spezifische Karte in einen anderen Stapel."""
        self.remove(card)
        target_pile.add(card, position=target_position)

    def transfer_all_to(self, target_pile: "CardPile"):
        """Transferiert alle Karten dieses Stapels in das Ziel (z.B. Hand -> Ablagestapel)."""
        # Kopie erstellen, um Schleifen-Probleme beim Entfernen zu vermeiden
        for card in list(self.cards):
            self.transfer_card(target_pile, card)

    def __str__(self):
        return f"{self.name} ({len(self.cards)} Karten)"