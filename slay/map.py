import random

class Node:
    def __init__(self, x, y):
        self.x = x  # Spalte (0 - 6)
        self.y = y  # Etage (0 - 14)
        self.room_type = None  # Wird in Phase 2/3 zugewiesen
        self.children = set()  # Verbindungen nach oben (y + 1)
        self.parents = set()   # Verbindungen nach unten (y - 1)

    def add_child(self, child_node):
        self.children.add(child_node)
        child_node.parents.add(self)

    def __repr__(self):
        return f"Node({self.x}, {self.y})[{self.room_type or 'LEER'}]"


class Generator:
    def __init__(self, width=7, height=15, paths_count=6):
        self.width = width
        self.height = height
        self.paths_count = paths_count
        self.grid = {}  # Key: (x, y), Value: Node-Objekt

    def generate(self):
        self.grid.clear()
        
        # 1. Leeres Grid mit Knoten initialisieren
        for y in range(self.height):
            for x in range(self.width):
                self.grid[(x, y)] = Node(x, y)

        # Phase 1: Wegenetz (Pathing) generieren
        self._generate_paths()
        
        # Nicht verwendete Knoten aus dem Grid entfernen
        self._prune_unused_nodes()

        # Phase 2 & 3: Raumtypen verteilen & Regeln anwenden
        self._assign_room_types()
        
        return self.grid

    def _generate_paths(self):
        # Erste beide Pfade MÜSSEN auf unterschiedlichen x-Startpunkten beginnen
        starting_xs = list(range(self.width))
        random.shuffle(starting_xs)
        
        for path_idx in range(self.paths_count):
            if path_idx < 2:
                # Erzwinge unterschiedliche Startknoten für die ersten 2 Pfade
                current_x = starting_xs[path_idx]
            else:
                current_x = random.randint(0, self.width - 1)

            for y in range(self.height - 1):
                current_node = self.grid[(current_x, y)]
                
                # Mögliche nächste Spalten (x-1, x, x+1) im Grid-Bereich
                possible_next_xs = [x for x in [current_x - 1, current_x, current_x + 1] if 0 <= x < self.width]
                
                # Filter, um Überkreuzungen zu verhindern
                valid_next_xs = []
                for next_x in possible_next_xs:
                    # Ein Kreuz entsteht, wenn wir diagonal gehen wollen (z.B. von x -> x-1)
                    # und es bereits eine Verbindung von x-1 -> x gibt.
                    if next_x == current_x - 1:
                        neighbor_node = self.grid.get((current_x - 1, y))
                        target_node = self.grid.get((current_x, y + 1))
                        if neighbor_node and target_node in neighbor_node.children:
                            continue  # Überspringen, da es sich kreuzen würde
                    
                    if next_x == current_x + 1:
                        neighbor_node = self.grid.get((current_x + 1, y))
                        target_node = self.grid.get((current_x, y + 1))
                        if neighbor_node and target_node in neighbor_node.children:
                            continue  # Überspringen, da es sich kreuzen würde
                            
                    valid_next_xs.append(next_x)

                # Falls kein Pfad ohne Kreuzung möglich ist (selten), nimm den direkten Weg nach oben (x)
                if not valid_next_xs:
                    next_x = current_x
                else:
                    next_x = random.choice(valid_next_xs)

                next_node = self.grid[(next_x, y + 1)]
                current_node.add_child(next_node)
                current_x = next_x

    def _prune_unused_nodes(self):
        """Entfernt alle Knoten, die am Ende keine Eltern (außer Etage 1) oder keine Kinder haben."""
        active_keys = set()
        
        # Finde alle erreichbaren Knoten von unten nach oben
        for y in range(self.height):
            for x in range(self.width):
                node = self.grid[(x, y)]
                # Etage 0 braucht keine Eltern, muss aber Kinder haben
                if y == 0 and node.children:
                    active_keys.add((x, y))
                # Höhere Etagen müssen Eltern haben (also erreichbar sein)
                elif y > 0 and node.parents:
                    active_keys.add((x, y))

        # Bereinige Grid
        for key in list(self.grid.keys()):
            if key not in active_keys:
                # Löse rückwirkend Verbindungen
                node = self.grid[key]
                for parent in list(node.parents):
                    parent.children.discard(node)
                for child in list(node.children):
                    child.parents.discard(node)
                del self.grid[key]

    def _assign_room_types(self):
        # 1. Schritt: Fixpunkte garantieren
        for (x, y), node in self.grid.items():
            if y == 0:
                node.room_type = "Monster"      # 100% Monster auf Etage 1
            elif y == 8:
                node.room_type = "Treasure"     # Schatz auf Etage 9
            elif y == 14:
                node.room_type = "Rest"         # Lagerfeuer auf Etage 15

        # 2. Schritt: Pool für den Rest vorbereiten (Eimer-System)
        unassigned_nodes = [node for node in self.grid.values() if node.room_type is None]
        total_unassigned = len(unassigned_nodes)

        # Prozentuale Verteilung (nach den realen Spielwerten)
        pool_ratios = {
            "Shop": int(total_unassigned * 0.05),
            "Rest": int(total_unassigned * 0.12),
            "Event": int(total_unassigned * 0.22),
            "Elite": int(total_unassigned * 0.15),  # Angelehnt an Ascension 1+
        }
        
        # Der Rest wird mit normalen Monstern aufgefüllt
        assigned_count = sum(pool_ratios.values())
        pool_ratios["Monster"] = max(0, total_unassigned - assigned_count)

        # Erzeuge den flachen, durchmischten Pool
        room_pool = []
        for r_type, count in pool_ratios.items():
            room_pool.extend([r_type] * count)
        random.shuffle(room_pool)

        # 3. Schritt: Zuweisung mit Constraint-Prüfung (Regeln)
        # Wir sortieren von Etage 1 nach 15, um hängende Abhängigkeiten sauber zu prüfen
        unassigned_nodes.sort(key=lambda n: n.y)

        for node in unassigned_nodes:
            assigned = False
            # Versuche einen passenden Typ aus dem Pool zu finden
            for r_type in list(room_pool):
                if self._is_valid_assignment(node, r_type):
                    node.room_type = r_type
                    room_pool.remove(r_type)
                    assigned = True
                    break
            
            # Fallback: Falls kein Typ im Pool die harten Regeln erfüllt, wird es ein Standard-Monster
            if not assigned:
                node.room_type = "Monster"

    def _is_valid_assignment(self, node, r_type):
        """Prüft die harten Spieldesign-Regeln für einen bestimmten Raumtyp."""
        # Regel: Keine Elites oder Lagerfeuer vor Etage 6 (y < 5)
        if r_type in ["Elite", "Rest"] and node.y < 5:
            return False

        # Regel: Kein Lagerfeuer auf Etage 14 (y = 13), da Etage 15 bereits ein Lagerfeuer ist
        if r_type == "Rest" and node.y == 13:
            return False

        # Regel (Consecutive): Keine aufeinanderfolgenden Elites, Shops oder Lagerfeuer auf dem Pfad
        if r_type in ["Elite", "Shop", "Rest"]:
            # Prüfe Eltern-Knoten (Verbindung nach unten)
            for parent in node.parents:
                if parent.room_type == r_type:
                    return False
            # Prüfe Kinder-Knoten (Verbindung nach oben, falls bereits zugewiesen)
            for child in node.children:
                if child.room_type == r_type:
                    return False

        # Regel (Sibling/Geschwister): Gabelungs-Zielwege dürfen nicht denselben Typ haben
        for parent in node.parents:
            # Hol dir alle Geschwister (Knoten, die denselben Parent haben)
            siblings = parent.children
            for sib in siblings:
                if sib != node and sib.room_type == r_type:
                    # Verhindert z.B. zwei Händler an einer Abzweigung
                    if r_type in ["Shop", "Rest", "Elite"]:
                        return False

        return True

    def draw_ascii_map(self):
        """Gibt eine schicke, textbasierte Darstellung der Karte im Terminal aus."""
        # Icons für die Räume
        icons = {
            "Monster": "🔴 Kampf ",
            "Elite":   "👿 Elite ",
            "Event":   "❓ Event ",
            "Shop":    "🪙 Shop  ",
            "Rest":    "🔥 Rast  ",
            "Treasure":"📦 Schatz"
        }
        
        print("\n=== SLAY THE SPIRE MAP ===")
        print(" [Etage 16] 👑 BOSS")
        print("     |")
        
        # Von oben (Etage 15) nach unten (Etage 1) zeichnen
        for y in range(self.height - 1, -1, -1):
            row_str = f" [Etage {y+1:02d}] "
            for x in range(self.width):
                node = self.grid.get((x, y))
                if node:
                    row_str += f"({x}){icons[node.room_type]}  "
                else:
                    row_str += " .             "
            print(row_str)