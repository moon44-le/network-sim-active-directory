# cards_db.py
from card import CardTarget, CardPersistence
from effect import VulnerableEffect, ZuwachsEffect, StrengthEffect, BufferEffect

# ==========================================
# 1. CARD POOL: DER EISERNE (Klassen-Karten)
# ==========================================
card_pool_eiserner = {
    
    # ==========================================
    # ANGRIFFSKARTEN (Attacks)
    # ==========================================
    
    "schlag": {
        "name": "Schlag", 
        "cost": 1, 
        "card_type": "Angriff", 
        "value": 6, 
        "description": "Fügt 6 Schaden zu.", 
        "target_type": CardTarget.SINGLE_ENEMY
    },
    
    "zerschmettern": {
        "name": "Zerschmettern", 
        "cost": 1, 
        "card_type": "Angriff", 
        "value": 8, # Im Original unaufgewertet 8 Schaden
        "description": "Fügt 8 Schaden zu. Verursacht 2 Verwundbar.", 
        "target_type": CardTarget.SINGLE_ENEMY, 
        "effects": [VulnerableEffect(2)]
    },
    
    "rundumschlag": {
        "name": "Rundumschlag", 
        "cost": 1, 
        "card_type": "Angriff", 
        "value": 8, # Im Original unaufgewertet 8 AoE-Schaden
        "description": "Fügt allen Gegnern 8 Schaden zu.", 
        "target_type": CardTarget.ALL_ENEMIES
    },
    
    "zwillingsschlag": {
        "name": "Zwillingsschlag", 
        "cost": 1, 
        "card_type": "Angriff", 
        "value": 5, 
        "description": "Fügt 2-mal 5 Schaden zu.", 
        "target_type": CardTarget.SINGLE_ENEMY,
        "attacks_count": 2
    },
    
    "schwertbumerang": {
        "name": "Schwertbumerang", 
        "cost": 1, 
        "card_type": "Angriff", 
        "value": 3, 
        "description": "Trifft zufällige Gegner 3-mal für je 3 Schaden.", 
        # Da wir noch keine Zufallsziel-Logik haben, behandeln wir es als AoE oder Single-Target:
        "target_type": CardTarget.SINGLE_ENEMY, 
        "attacks_count": 3
    },
    
    "blutbad": {
        "name": "Blutbad", 
        "cost": 2, 
        "card_type": "Angriff", 
        "value": 20, 
        "description": "Flüchtig. Fügt 20 Schaden zu.", 
        "target_type": CardTarget.SINGLE_ENEMY,
        "persistence": CardPersistence.ETHEREAL
    },
    
    "aufwaertshaken": {
        "name": "Aufwärtshaken", 
        "cost": 2, 
        "card_type": "Angriff", 
        "value": 12, 
        "description": "Fügt 12 Schaden zu. Verursacht 1 Verwundbar.", 
        "target_type": CardTarget.SINGLE_ENEMY,
        "effects": [VulnerableEffect(1)] # Im echten Spiel auch noch "Schwach"
    },
    
    "vorschlaghammer": {
        "name": "Vorschlaghammer", 
        "cost": 3, 
        "card_type": "Angriff", 
        "value": 32, 
        "description": "Fügt gigantische 32 Schaden zu.", 
        "target_type": CardTarget.SINGLE_ENEMY
    },
    
    # ==========================================
    # FERTIGKEITSKARTEN (Skills)
    # ==========================================
    
    "verteidigung": {
        "name": "Verteidigung", 
        "cost": 1, 
        "card_type": "Fertigkeit", 
        "value": 5, 
        "description": "Erhält 5 Block.", 
        "target_type": CardTarget.SELF
    },
    
    "achselzucken": {
        "name": "Achselzucken", 
        "cost": 1, 
        "card_type": "Fertigkeit", 
        "value": 8, 
        "description": "Erhält 8 Block. (Zieht im Original 1 Karte).", 
        "target_type": CardTarget.SELF
    },
    
    "geisterruestung": {
        "name": "Geisterrüstung", 
        "cost": 1, 
        "card_type": "Fertigkeit", 
        "value": 10, 
        "description": "Flüchtig. Erhält 10 Block.", 
        "target_type": CardTarget.SELF,
        "persistence": CardPersistence.ETHEREAL
    },
    
    "unbezwingbar": {
        "name": "Unbezwingbar", 
        "cost": 2, 
        "card_type": "Fertigkeit", 
        "value": 30, 
        "description": "Erschöpfend. Erhält 30 Block.", 
        "target_type": CardTarget.SELF,
        "exhausts": True
    },
    
    "flammenbarriere": {
        "name": "Flammenbarriere", 
        "cost": 2, 
        "card_type": "Fertigkeit", 
        "value": 12, 
        "description": "Erhält 12 Block. Fügt Angreifern Schaden zu (hier: 1 Puffer).", 
        "target_type": CardTarget.SELF, 
        "effects": [BufferEffect(1)]
    },
    
    # ==========================================
    # MACHTKARTEN (Powers)
    # ==========================================
    
    "entflammen": {
        "name": "Entflammen", 
        "cost": 1, 
        "card_type": "Macht", 
        "value": 0, 
        "description": "Erhalte sofort +2 Stärke.", 
        "target_type": CardTarget.SELF,
        "effects": [StrengthEffect(2)] # Sofort-Effekt
    },
    
    "daemonenform": {
        "name": "Dämonenform", 
        "cost": 3, 
        "card_type": "Macht", 
        "value": 0, 
        "description": "Erhalte jede Runde dauerhaft 2 Stärke.", 
        "target_type": CardTarget.SELF, 
        "effects": [ZuwachsEffect("Stärke", 2)] # Rundenbasierter Zuwachs
    },
    
    "metallisieren": {
        "name": "Metallisieren", 
        "cost": 1, 
        "card_type": "Macht", 
        "value": 0, 
        "description": "Erhalte jede Runde dauerhaft 3 Block. (Noch zu implementieren)", 
        "target_type": CardTarget.SELF,
        "effects": [] # Benötigt später einen "BlockZuwachsEffect"
    }
}

# ==========================================
# 2. CARD POOL: FARBLOS (Hilfskarten / Tränke)
# ==========================================
card_pool_farblos = {
    "heiltrank": {
        "name": "Heiltrank", 
        "cost": 0, 
        "card_type": "Fertigkeit", 
        "value": 0, 
        "description": "Heilt dich im Notfall um 2 HP.", 
        "target_type": CardTarget.SELF, 
        "is_colorless": True, 
        "exhausts": True, 
        "effects": [HealEffect(2)]
    }
}

# ==========================================
# 3. CARD POOL: STATUSKARTEN (Temporäre Plagen)
# ==========================================
card_pool_status = {
    "wunde": {
        "name": "Wunde",
        "cost": -1,  # Nicht spielbar!
        "card_type": "Status",
        "value": 0,
        "description": "Unspielbar. Verstopft deine Hand.",
        "target_type": CardTarget.SELF,
        "is_colorless": True
    },
    "schleim": {
        "name": "Schleim",
        "cost": 1,
        "card_type": "Status",
        "value": 0,
        "description": "Erschöpfend. Tut nichts.",
        "target_type": CardTarget.SELF,
        "is_colorless": True,
        "exhausts": True
    }
}

# ==========================================
# 4. CARD POOL: FLÜCHE (Permanente Schwächungen)
# ==========================================
card_pool_fluch = {
    "verletzung": {
        "name": "Verletzung",
        "cost": -1,  # Nicht spielbar
        "card_type": "Fluch",
        "value": 0,
        "description": "Unspielbar. Fluch.",
        "target_type": CardTarget.SELF,
        "is_colorless": True
    }
}

# ==========================================
# 5. DER ZENTRALE GESAMT-POOL (Such-Index)
# ==========================================
# Wir führen alle Dictionaries an einer Stelle zusammen, damit die 
# Suchfunktion 'create_card' blitzschnell überall fündig wird.
ALL_CARDS = {
    **card_pool_eiserner,
    **card_pool_farblos,
    **card_pool_status,
    **card_pool_fluch
}