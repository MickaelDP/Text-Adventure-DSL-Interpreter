"""
 Nom ......... : game.py
 Rôle ........ :  Dionary structure containing the full game state and helper access functions.ict
 Auteur ...... : Mickaël D. Pernet
 Version ..... : 2026 Refactor (Original 2022)
 Licence ..... : Project-based
"""

"""
Note on DMAP:
    Matrix where each line represents a floor and each sub-list a room:
    [<room_number>, <key/name>, <Exits: North, East, South, West, Up, Down (0=no, 1=open, 2=special)>]
    Note: Use the character ’ instead of '.
"""
game = {
        "combine": {
            "logs": {
                       "broken ladder": "ladder"
            },
            "glass": {
                        "whiskey": "glass of whiskey"
            },
            "whiskey": {
                        "glass": "glass of whiskey"
            },
            "glass of whiskey": {
                        "bulldog": "sleeping bulldog"
            },
            "iron key": {
                        "iron door": "open door"
            },
            "silver key": {
                        "silver door": "open door"
            },
            "axe": {
                   "bushes": "logs"
            },
            "coded box": {
                   "codes": "silver key"
            } },
        "current": {
            "RUN": 1,
            "FLOOR": 1,
            "ROOM": 6, },
        "damage": {
            "sausages": 2 },
        "DMAP": [
            # --- Ground Floor (FLOOR 0) ---
            [
                [0, "the stairs going up", [0, 1, 0, 0, 1, 0]],
                [1, "northern dining room", [0, 2, 1, 1, 0, 0]],
                [2, "the kitchen", [0, 0, 0, 1, 0, 0]],
                [3, "north access", [0, 1, 1, 0, 0, 0]],
                [4, "southern dining room", [1, 0, 0, 1, 0, 0]],
                [5, "the north greenhouse", [0, 0, 1, 0, 0, 0]],
                [6, "south access", [1, 1, 0, 0, 0, 0]],
                [7, "entrance hall", [0, 1, 2, 1, 0, 0]],
                [8, "the south greenhouse", [1, 0, 0, 1, 0, 0]]
            ],
            # --- First Floor (FLOOR 1) ---
            [
                [0, "the stairs going down", [0, 1, 0, 0, 0, 1]],
                [1, "the first floor hall", [0, 2, 1, 2, 0, 0]],
                [2, "the master bedroom", [0, 0, 1, 1, 0, 0]],
                [3, "the office", [0, 1, 0, 0, 0, 0]],
                [4, "the north corridor", [1, 0, 1, 1, 2, 0]],
                [5, "the master bed", [1, 0, 0, 0, 0, 0]],
                [6, "the guest room", [0, 1, 0, 0, 0, 0]],
                [7, "the south corridor", [1, 1, 0, 1, 0, 0]],
                [8, "the storage room", [0, 0, 0, 1, 0, 0]]
            ],
            # --- Second Floor (FLOOR 2) ---
            [
                ['X'], ['X'], ['X'],
                ['X'], [4, "the observatory", [0, 0, 0, 0, 0, 1]], ['X'],
                ['X'], ['X'], ['X']
            ]
         ],
        "description": { # Using lambda for lazy evaluation
            # --- FLOOR 0 ---
            "the stairs going up": lambda: "A spiral staircase of white polished marble leading to the upper floor. It leads to a dining room to the east.",
            "northern dining room": lambda: "A dining room continuing to the south. This end of the table is reserved for the master of the house. There is a [buffet] against the wall. Stairs to the west and an [iron door] to the east.",
            "the kitchen": lambda: f"""You enter a room with a large extinguished [hearth] containing a huge pot, various kitchen utensils{', a [knife]' if 'knife' in room_inventory(position()[1]) else ''}{' and even an [axe]' if 'axe' in room_inventory(position()[1]) else ''}.""",
            "north access": lambda: "You enter a long corridor with a [bay window] replacing the west wall. [paintings] and a door adorn the east wall. It extends to the south.",
            "southern dining room": lambda: "You walk along a reception table several meters long, surrounded by heavy wooden chairs. To the north is the master's seat; a door on the west wall.",
            "the north greenhouse": lambda: "You reach the back of the greenhouse, much wilder than the southern part. Many small trees and [bushes] grow freely here.",
            "south access": lambda: "A long corridor with a [bay window] on the west wall and a door on the east wall. It continues to the north.",
            "entrance hall": lambda: "A stone-paved entrance hall, completely empty except for the east and west accesses, and a [silver door] to the south.",
            "the south greenhouse": lambda: "You are in a greenhouse connected to the entrance hall by a small door to the west. It extends north. [flowers] are arranged aesthetically in geometric shapes.",

            # --- FLOOR 1 ---
            "the stairs going down": lambda: "A spiral staircase of white polished marble leading to the lower floor. It leads to a hall to the east.",
            "the first floor hall": lambda: f"""{'A large [bulldog] stares at you insistently, blocking the way while lying on ' if pnj('the first floor hall', 'bulldog') else ' '}a faded, chewed-up rug in the middle of a hall. It leads to the marble stairs to the west, a corridor to the south, and a polished door to the east.""",
            "the master bedroom": lambda: "A large room divided by a semi-alcove. In your current area, a [bookshelf] and a fine leather [armchair] furnish the room. A door leads west, while the bed sits to the south.",
            "the office": lambda: "The only [window] is boarded up, letting in only a few rays of light onto a heavy [desk] with drawers and a chair facing the door.",
            "the north corridor": lambda: f"""A corridor adorned with a worn red [rug] connecting the hall to the north. {'A [broken ladder] with missing rungs' if 'broken ladder' in room_inventory(position()[1]) else 'A [ladder]'} is the east wall, leading to a ceiling hatch, while a door on the west wall leads to another room.""",
            "the master bed": lambda: "This part of the room is separated from the north. A large double [bed] occupies almost the entire space.",
            "the guest room": lambda:f"A small room containing a basic [bed] and a bedside [table]{' with an empty [glass] on it' if 'glass' in room_inventory(position()[1]) else ''}. Pale light filters through the curtains, giving the room a sad mood. A door is on the east wall.",
            "the south corridor": lambda: "A long corridor continuing north with a dusty [rug] that was once red. Light comes from a [window] on the south wall. Doors are to the east and west.",
            "the storage room": lambda: f"""This windowless room only has one entry to the west. You can see a [clutter] of junk{', notably a bottle of [whiskey]' if 'whiskey' in room_inventory(position()[1]) else ''}{' and some [sausages] hanging from the ceiling' if 'sausages' in room_inventory(position()[1]) else ''}.""",

            # --- FLOOR 2 ---
            "the observatory": lambda: "Using the ladder, you reach a small tower with a [telescope] pointed at a distant mountain." },                                                                                                              
        "hero": {
            "CHARACTER_HEALTH": 10,
            "INV_CHARACTER": [],
            "DAMAGE_CHARACTER": 1 },
        # {"room": [element, option] - 1 Collectible, 0 Static, 2 Static but Interaction Result in inventory, 3 NPC (Non-Player Character)}
        "inventory": {
                "the guest room": ["glass", 1, "bed", 0, "window", 0, "table", 0],
                "the storage room": ["whiskey", 1, "sausages", 1, "clutter", 0],
                "the south corridor": ["window", 0, "rug", 0],
                "the north corridor": ["broken ladder", 2, "rug", 0],
                "the office": ["coded box", 1, "window", 0, "desk", 0],
                "the first floor hall": ["bulldog", 3],
                "the master bedroom": ["bookshelf", 0, "armchair", 0],
                "the master bed": ["bed", 0, "iron key", 1],
                "northern dining room": ["buffet", 0, "iron door", 2],
                "the kitchen": ["hearth", 0, "knife", 1, "axe", 1],
                "north access": ["bay window", 0, "paintings", 0],
                "south access": ["bay window", 0],
                "entrance hall": ["silver door", 2],
                "the south greenhouse": ["flowers", 0],
                "the north greenhouse": ["bushes", 1],
                "the observatory": ["telescope", 0, "codes", 1]
        },
        "character": {    
                  "the first floor hall": {
                                                'bulldog': {
                                                               "life": 5,
                                                               "damage": 5,
                                                               "inv": [],
                                                               "weak": "glass of whiskey"
                                                }
                  } },
        "useCase": {
            "coded box": {
                        "telescope": lambda: "You look through the telescope and test the number sequences on the lock until it clicks open. It contains a silver key."
                     },
            "glass": {
                       "solo": lambda: "Although the glass is clean, it remains empty and useless for now.",
                       "whiskey": lambda: "You fill the glass with whiskey."
            },
            "whiskey": {
                       "solo": lambda: "You open the bottle and take a small sip. Better save some for later.",
                       "glass": lambda: "You fill the glass with whiskey."
            },
            "glass of whiskey": {
                        "solo": lambda: "You take a sip to enjoy the pleasant taste of the drink.",
                        "bulldog": lambda: "You present the glass to the bulldog. He quickly laps it up and falls into a deep sleep."
            },
            "logs": {
                        "broken ladder": lambda: f"You reinforce the ladder by inserting the logs into the missing rungs."
            },
            "iron key": {
                        "iron door": lambda: f"You insert the heavy iron key and turn it slowly. A click signals the door is now open."
            },
            "axe": {
                        "bushes": lambda: f"You chop the bushes with the axe and make a small pile of logs. Suddenly, the axe head flies off and sticks into the ceiling."
            },
            "silver key": {
                        "silver door": lambda: f"You insert the delicate silver key into the silver door!"
            },
            "coded box": {
                        "codes": lambda: f"You try different combinations on the box until one unlocks it. It contains a [silver key]."
            } },
        "special": {
            "the guest room": { 
                                 "inspect": {
                                        "bed": lambda: f"The bed you woke up in. The sheets are messy.",
                                        "window": lambda: f"Parting the curtains reveals a pastoral landscape under a rising dawn.",
                                        "table": lambda: f"A simple bedside table{'. An empty glass sits on it' if 'glass' in room_inventory(position()[1]) else ''}."
                                 },
                                 "use": {
                                        "bed": lambda: f"You just woke up and don't feel like sleeping again.",
                                        "window": lambda: f"No matter how hard you pull, the window won't open.",
                                        "table": lambda: f"You move the table, but there's nothing underneath or behind it."
                                 } }, 
            "the south corridor":  {
                                 "inspect": {
                                        "window": lambda: f"The pastoral landscape outside is slightly dazzling in the morning light.",
                                        "rug": lambda: f"This rug has seen better days; its color is faded and it's covered in dust."
                                 },
                                 "use": {
                                          "window": lambda: f"The window is stuck fast.",
                                          "rug": lambda: f"You shake the rug, dust rises slowly... but no, this rug definitely isn't magic."
                                 } },
            "the north corridor": {
                                 "inspect": {
                                        "rug": lambda: f"A dusty rug that once had a vibrant color."
                                 },
                                 "use": {
                                        "rug": lambda: f"You kick the rug, but nothing happens."
                                 },
                                 "special": lambda: f"To reach the upper level, you'll need the ladder, but its current state makes it unusable."
                              },
            "the storage room":      {
                                 "inspect": {
                                          "clutter": lambda: f"Sacks of flour and rice, broken tools, hay... basically a bunch of useless stuff."
                                 },
                                 "use": {
                                          "clutter": lambda: f"No way you're digging through all this junk; you'd probably be asked to tidy it up later."
                                 } },
            "the office":       {      
                                 "inspect": {
                                          "desk": lambda: f"The desk is tidy, with a stack of paper and a quill. {'Checking the drawers, one contains a [coded box] waiting for a six-digit combination.' if 'coded box' in room_inventory(position()[1]) else ''}",
                                          "window": lambda: f"This window has been strangely blocked by heavy planks. Why?"
                                 },
                                 "use": {
                                          "desk": lambda: f"Now is not the time to be doing paperwork.",
                                          "window": lambda: f"The planks prevent the window from opening."                                  
                                 } },
            "the first floor hall": {
                                 "special": lambda: f"You try to step forward, but as you approach, the [bulldog] growls, determined not to let you pass."
                                 },
            "the master bedroom": {
                                 "inspect":{
                                          "bookshelf": lambda: f"A collection of ancient leather-bound books. These are quite valuable!",
                                          "armchair": lambda: f"The armchair looks so comfortable that the shape of its owner is almost imprinted in it."
                                 },
                                 "use":{
                                          "bookshelf": lambda: f"You move several books, but no secret passage here.",
                                          "armchair": lambda: f"A well-deserved short break. Now, to find the exit."
                                 } },
            "the master bed":   {
                                 "inspect":{
                                          "bed": lambda: f"This bed is much softer and more luxurious than the one you woke up in."
                                 },
                                 "use":{
                                          "bed": lambda: f"You strip the blankets and flip the pillows. {'You find an [iron key] hidden among the sheets.' if 'iron key' in room_inventory(position()[1]) else ''}"
                                 } },
            "northern dining room":{
                                 "inspect":{
                                          "buffet": lambda: f"A beautiful piece of furniture filled with luxurious tableware."
                                 },
                                 "use":{
                                          "buffet": lambda: f"The buffet is far too heavy to move."
                                 },
                                 "special": lambda: f"The iron door is locked, preventing you from reaching the next room."
                                 },
            "the kitchen":         {
                                 "inspect": {
                                        "hearth": lambda: f"A large stone hearth holding a pot and lots of ash. Clearly hasn't been cleaned recently."
                                 },
                                 "use": {
                                        "hearth": lambda: f"No, it's not time to cook!"
                                 } },
            "north access":         {
                                 "inspect": {
                                        "bay window": lambda: f"The large bay window doesn't allow you to see very far, as a hedge at least two meters high stands only three meters away, not to mention the thick iron bars protecting it.",
                                        "paintings": lambda: f"A triptych of portraits depicting a man at three different ages."
                                 },
                                 "use": {
                                        "bay window": lambda: f"No, even if you managed to break the glass without hurting yourself, the bars would still prevent any exit.",
                                        "paintings": lambda: f"You swing the paintings, but they remain firmly attached; nothing seems to be hidden behind them."
                                 } },
            "south access":         {
                                 "inspect": {
                                        "bay window": lambda: f"The large bay window doesn't allow you to see very far, as a hedge at least two meters high stands only three meters away, not to mention the thick iron bars protecting it."
                                 },
                                 "use": {
                                        "bay window": lambda: f"No, even if you managed to break the glass without hurting yourself, the bars would still prevent any exit."
                                 } },
            "the south greenhouse":      {
                                 "inspect": {
                                        "flowers": lambda: f"Monkshood, bergenia, camellia, wandflower... mmm, clearly the master of the house has a passion for botany."
                                 },
                                 "use": {
                                        "fleurs": lambda: f"Flowers in a bouquet wither and never bloom again! Let them live."
                                 } },
            "the observatory":     {
                                 "inspect": {
                                        "telescope": lambda: f"It looks functional and is pointed in a very specific direction."
                                 },
                                 "use": {
                                        "telescope": lambda: f"Looking through it, you see the mountain closely. It seems adjusted to read wooden signs with [codes] written on them."
                                 } },
            "entrance hall":      {
                                 "special": lambda: f"The silver door is solid and its lock seems very secure!"
                                }
            },
            "welcome": """
 POSSIBLE ACTIONS HELP: 
Help                                    help
Move                                    go to <direction> (north, south, east, west)
Attack                                  attack <target>
                                        attack <target> with <object>
Take                                    take <object>
Use                                     use <object>
                                        use <object> with <element>
Look                                    look at <object>
Inventory                               inventory
Note: Objects with multiple words must be in quotes "".
"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'\n
You wake up in a place that is definitely not your bed. You stand up and find yourself in 
"""
}

# --- Fonctions Auxiliaires ---
def combine(E1, E2):
    """
    combine:
        Returns the value for the combination of E1 and E2.

    Args:
        E1 (str): An object.
        E2 (str): An object.

    Returns:
        str: The result of the combination.
    """
    return game.get("combine", {"empty": 0}).get(str(E1), {"empty": 0}).get(str(E2), 0)

def RUN():
    """
    RUN: 
        Returns the current value of RUN within the structure.

    Returns:
        int: 0 or 1.
    """
    return game.get("current", {"empty", 0}).get("RUN", -1)

def position():
    """
    position: 
        Returns the current position within the DMAP matrix.

    Returns:
        str: The resulting position.
    """
    return game.get("DMAP", 0)[game.get("current").get("FLOOR")][game.get("current").get("ROOM")]

def description(room_key):
    """
    description: 
        Returns the description for E1 from the structure.

    Args:
        E1 (str): The room name.

    Returns:
        str: The resulting description.
    """
    return game.get("description", {"vide": 0}).get(room_key,lambda: 0)

def hero_inventory():
    """
    hero_inventory: 
        Retrieves the inventory from the "hero" structure.

    Returns:
        list: The inventory list.
    """
    return game.get("hero", {"empty": 0}).get("INV_CHARACTER", 0)

def hero_health():
    """
    hero_health 
        Returns the hero's health value from the "hero" structure.

    Returns:
        int: Health points (HP).
    """
    return game.get("hero", {"empty": 0}).get("CHARACTER_HEALTH", 0)

def hero_damage():
    """
    hero_damage: 
        Returns the damage amount from the "hero" structure.

    Returns:
        int: Damage points.
    """
    return game.get("hero", {"empty": 0}).get("DAMAGE_CHARACTER", 0)

def room_inventory(room_key):
    return game.get("inventory", {"empty":0}).get(room_key, 0)

def pnj(room_key, name):
    """
    pnj: 
        Retrieves the data structure for a specific character.

    Args:
        room_key: The room name.
        name: The NPC name.

    Returns:
        dict: The character's data structure.
    """
    return game.get("character", {"empty": 0}).get(room_key, {"empty": 0}).get(name, 0)

def use(E1, E2):
    """
    use: 
    Returns the result of using E1 with E2.

    Args:
        E1 (str): The first object ("object1").
        E2 (str): The second object ("object2").

    Returns:
        str: The resulting interaction or outcome.
    """
    return game.get("useCase", {"empty": 0}).get(str(E1), {"empty": 0}).get(str(E2), lambda: 0)

def special(room_key, action, item):
    """
        special: 
            Returns the result of a specific action performed on an item within a room.

        Args:
            room_key (str): The name or ID of the room.
            action (str): The action to be performed (e.g., "look", "push").
            item (str): The object the action is applied to.

        Returns:
            str/int: The result of the special action, or 0 if not found.
    """
    return game.get("special", {"empty": 0}).get(room_key, {"empty": 0}).get(action, {"empty": 0}).get(item, lambda: 0)

def styleFormat(text):
    border = "\"`-._,-'\"" * 15
    return f"\n{border}\n\n{text}\n\n{border}\n"
