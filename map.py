import random
import ui

class Node:
    def __init__(self, x, y):
        self.x = x  # Spalte (0 - 6)
        self.y = y  # Etage (0 - 14)
        self.room_type = None
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
        
        # 1. Leeres Grid initialisieren
        for y in range(self.height):
            for x in range(self.width):
                self.grid[(x, y)] = Node(x, y)

        # Phase 1: Wegenetz (Pathing) generieren
        self._generate_paths()
        
        # Sackgassen und ungenutzte Pfade vollständig entfernen
        self._prune_unused_nodes()

        # Phase 2 & 3: Raumtypen verteilen & Regeln anwenden
        self._assign_room_types()
        
        return self.grid

    def _generate_paths(self):
        # Exakt 3 Startknoten auf Etage 1 (x = 1, 3, 5)
        start_xs = [1, 3, 5]
        
        # Exakt 3 Zielknoten auf Etage 15 (x = 1, 3, 5)
        top_xs = [1, 3, 5]

        for path_idx in range(self.paths_count):
            # Startpunkte gleichmäßig auf die 3 Startknoten verteilen
            current_x = start_xs[path_idx % len(start_xs)]

            for y in range(self.height - 1):
                current_node = self.grid[(current_x, y)]

                # VORLETZTE ETAGE (y = 13 -> Etage 14):
                # Wir erzwingen, dass der NÄCHSTE Schritt (auf y = 14 -> Etage 15)
                # AUSSCHLIESSLICH auf einen der 3 Zielknoten (1, 3 oder 5) führt.
                if y == self.height - 2:
                    possible_next_xs = [x for x in [current_x - 1, current_x, current_x + 1] if x in top_xs]
                    
                    if not possible_next_xs:
                        possible_next_xs = [min(top_xs, key=lambda target_x: abs(target_x - current_x))]
                else:
                    possible_next_xs = [x for x in [current_x - 1, current_x, current_x + 1] if 0 <= x < self.width]

                # Überkreuzungsschutz
                valid_next_xs = []
                for next_x in possible_next_xs:
                    if next_x == current_x - 1:
                        neighbor_node = self.grid.get((current_x - 1, y))
                        target_node = self.grid.get((current_x, y + 1))
                        if neighbor_node and target_node in neighbor_node.children:
                            continue
                    
                    if next_x == current_x + 1:
                        neighbor_node = self.grid.get((current_x + 1, y))
                        target_node = self.grid.get((current_x, y + 1))
                        if neighbor_node and target_node in neighbor_node.children:
                            continue
                            
                    valid_next_xs.append(next_x)

                if not valid_next_xs:
                    next_x = current_x
                else:
                    next_x = random.choice(valid_next_xs)

                next_node = self.grid[(next_x, y + 1)]
                current_node.add_child(next_node)
                current_x = next_x

    def _prune_unused_nodes(self):
        """Entfernt Sackgassen rigoros durch Zwei-Wege-Erreichbarkeitsprüfung."""
        
        # 1. Vorwärts-Pass: Finde alle Knoten, die von Etage 1 (y=0) aus erreichbar sind
        reachable_from_bottom = set()
        queue = [self.grid[(x, 0)] for x in [1, 3, 5] if self.grid[(x, 0)].children]
        for n in queue:
            reachable_from_bottom.add((n.x, n.y))
            
        while queue:
            curr = queue.pop(0)
            for child in curr.children:
                if (child.x, child.y) not in reachable_from_bottom:
                    reachable_from_bottom.add((child.x, child.y))
                    queue.append(child)

        # 2. Rückwärts-Pass: Finde alle Knoten, die den Boss über Etage 15 (y=14) erreichen können
        reachable_from_top = set()
        top_nodes = [self.grid[(x, 14)] for x in [1, 3, 5] if (x, 14) in reachable_from_bottom]
        for n in top_nodes:
            reachable_from_top.add((n.x, n.y))

        queue = list(top_nodes)
        while queue:
            curr = queue.pop(0)
            for parent in curr.parents:
                if (parent.x, parent.y) not in reachable_from_top:
                    reachable_from_top.add((parent.x, parent.y))
                    queue.append(parent)

        # Nur Knoten behalten, die BEIDE Kriterien erfüllen (keine Sackgassen!)
        valid_keys = reachable_from_bottom.intersection(reachable_from_top)

        for key in list(self.grid.keys()):
            if key not in valid_keys:
                node = self.grid[key]
                for parent in list(node.parents):
                    parent.children.discard(node)
                for child in list(node.children):
                    child.parents.discard(node)
                del self.grid[key]

    def _assign_room_types(self):
        # Fixpunkte setzen
        for (x, y), node in self.grid.items():
            if y == 0:
                node.room_type = "Monster"      # 100% Monster auf Etage 1
            elif y == 8:
                node.room_type = "Treasure"     # 100% Schatz auf Etage 9
            elif y == 14:
                node.room_type = "Rest"         # 100% Lagerfeuer auf Etage 15 (3 Stück)

        unassigned_nodes = [node for node in self.grid.values() if node.room_type is None]
        total_unassigned = len(unassigned_nodes)

        pool_ratios = {
            "Shop": int(total_unassigned * 0.05),
            "Rest": int(total_unassigned * 0.12),
            "Event": int(total_unassigned * 0.22),
            "Elite": int(total_unassigned * 0.15),
        }
        
        assigned_count = sum(pool_ratios.values())
        pool_ratios["Monster"] = max(0, total_unassigned - assigned_count)

        room_pool = []
        for r_type, count in pool_ratios.items():
            room_pool.extend([r_type] * count)
        random.shuffle(room_pool)

        unassigned_nodes.sort(key=lambda n: n.y)

        for node in unassigned_nodes:
            assigned = False
            for r_type in list(room_pool):
                if self._is_valid_assignment(node, r_type):
                    node.room_type = r_type
                    room_pool.remove(r_type)
                    assigned = True
                    break
            
            if not assigned:
                node.room_type = "Monster"

    def _is_valid_assignment(self, node, r_type):
        # --- Etagen-Sperren ---
        # Keine Elites oder Lagerfeuer vor Etage 6 (y < 5)
        if r_type in ["Elite", "Rest"] and node.y < 5:
            return False

        # Kein Elite direkt vor dem Schatz (Etage 8 / y = 7)
        if r_type == "Elite" and node.y == 7:
            return False

        # Kein Lagerfeuer auf Etage 14 (y = 13)
        if r_type == "Rest" and node.y == 13:
            return False

        # --- Consecutive Rule (Keine doppelten Spezialräume hintereinander) ---
        if r_type in ["Elite", "Shop", "Rest"]:
            for parent in node.parents:
                if parent.room_type == r_type:
                    return False
            for child in node.children:
                if child.room_type == r_type:
                    return False

        # --- Sibling Rule (Keine doppelten Spezialräume an derselben Abzweigung) ---
        for parent in node.parents:
            siblings = parent.children
            for sib in siblings:
                if sib != node and sib.room_type == r_type:
                    if r_type in ["Shop", "Rest", "Elite"]:
                        return False

        # --- Pfad-Limitierung für Elites (Maximal 3 Elites pro Route) ---
        if r_type == "Elite":
            if self._get_max_elites_in_path(node) >= 3:
                return False

        return True

    def _get_max_elites_in_path(self, node):
        """Hilfsmethode: Prüft, wie viele Elites bisher auf dem Pfad zu diesem Knoten liegen."""
        if not node.parents:
            return 0
        
        max_parent_elites = 0
        for parent in node.parents:
            parent_elites = self._get_max_elites_in_path(parent)
            if parent.room_type == "Elite":
                parent_elites += 1
            if parent_elites > max_parent_elites:
                max_parent_elites = parent_elites
                
        return max_parent_elites

    def draw_ascii_map(self):
        """Gibt die Map mit Pfadstrichen in den tatsächlichen Zwischenräumen aus."""

        type_letters = {
            "Monster": "M",
            "Elite":   "E",
            "Event":   "?",
            "Shop":    "$",
            "Rest":    "R",
            "Treasure":"T"
        }

        print("\n=== SLAY THE SPIRE MAP ===")
        print(f"\03-7m\033[30m          [BOSS]   \033[0m")
        print("                 |   |   |")

        # Von oben nach unten rendern
        for y in range(self.height - 1, -1, -1):
            
            # 1. Knoten-Zeile (Muster: "[M] " -> 4 Zeichen pro Feld)
            node_row = f"           "
            for x in range(self.width):
                node = self.grid.get((x, y))
                if node:
                    code = type_letters.get(node.room_type, "O")
                    cell = f"[{code}] "
                else:
                    cell = "    "
                
                node_row += cell
            
            print(node_row)

            # 2. Verbindungs-Zeile nach unten zur Etage y-1
            if y > 0:
                # Zeichenpuffer initialisieren (7 x 4 = 28 Zeichen Breitenraster)
                line_chars = [" "] * (self.width * 4)

                for x in range(self.width):
                    current_node = self.grid.get((x, y))
                    if not current_node:
                        continue

                    node_center = x * 4 + 1

                    for parent in current_node.parents:
                        # Pfad nach LINKS-UNTEN
                        if parent.x == x - 1:
                            line_chars[node_center - 2] = "/"
                            
                        # Pfad GERADE-UNTEN
                        elif parent.x == x:
                            line_chars[node_center] = "|"
                            
                        # Pfad nach RECHTS-UNTEN
                        elif parent.x == x + 1:
                            line_chars[node_center + 2] = "\\"

                # Zeile mit Einrückung ausgeben
                print("           " + "".join(line_chars).rstrip())


if __name__ == "__main__":
    map_generator = Generator(width=7, height=15, paths_count=6)
    generated_grid = map_generator.generate()
    map_generator.draw_ascii_map()