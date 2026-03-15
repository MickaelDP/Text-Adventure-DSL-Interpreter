"""
 Name ......... : interpreter.py
 Role ......... : Interpretation layer connecting the user, the DSL parser, and the game state.
 Author ....... : Mickaël D. Pernet
 Version ...... : 2026 Refactor (Original 2022)
 License ...... : Project-based
"""

from sly import Lexer, Parser
from math import sqrt
from lexer import DLexer
from preprocessor import EN_Matrice, FR_Racinisation, PProcessor, Conform 
from game import game as imp_game
from game import (combine, description, hero_damage, hero_inventory, 
                  room_inventory, pnj, position, special, styleFormat, use)
from parser import DParser

game_state = imp_game.copy()

def run_engine(game_state):
    """
    Main REPL (Read-Eval-Print Loop) for the game engine.
    Handles the translation pipeline: Input -> Preprocessor -> Lexer -> Parser -> Executor.
    """
    lexer = DLexer()
    parser = DParser()

    introduction = game_state["welcome"][:-2] + description(position()[1])() + ("`-._,-'\"" * 15)
    print(introduction)
    
    while game_state["current"]["RUN"]:
        try:
            user_input = input('Manor > ')
        except EOFError:
            break

        if user_input:
            # Preprocessing & Normalization
            normalized_input = PProcessor(user_input, EN_Matrice, FR_Racinisation).replace("'", " ")

            try:
                # Tokenization & Parsing
                token_stream = lexer.tokenize(normalized_input)
                ast_tree = parser.parse(token_stream)
                # Logic Execution
                game_state = execute_command(ast_tree, game_state)           
            except Exception as e:
                print(f"Engine Error: {e}")
                
                
def execute_command(tree, game_state):
    """
    Dispatches the parsed command to the corresponding game logic.
    Renamed from 'Exec' as per SuiviMajLang.txt
    """
    if not tree:
        return game_state

    # The first element of the tree is the action tag (e.g., 'deplacement', 'utiliser')
    result = None
    action_type = tree[0]

    # --- Help ---
    if action_type == 'help':
        result = styleFormat("""
 POSSIBLE ACTIONS HELP: 
Help                                    help
Move                                    go to <direction> (north, south, east, west)
Attack                                  attack <target>
                                        attack <target> with <object>
Take                                    take <object> / pick up <object>
Use                                     use <object>
                                        use <object> with <element>
Look                                    look at <object> / examine <object>
Inventory                               inventory
Exit                                    exit / quit
Note: Objects with multiple words must be in quotes "".
""")
    
    # --- Standard Attack ---
    elif action_type == 'attack':
        target = str(tree[1].replace('"', ''))
        current_loc = position()[1]
        if pnj(current_loc, target):
            game_state["character"][current_loc][target]["life"] -= hero_damage()
            if game_state["character"][current_loc][target]["life"] > 0:
                riposte = game_state["character"][current_loc][target]["damage"]
                game_state["hero"]["CHARACTER_HEALTH"] -= riposte

            msg = f"\nYou attack {tree[1]} and deal {hero_damage()} damage"
            msg += (f' and {tree[1]} falls unconscious.' if game_state["character"][current_loc][target][
                                                                "life"] <= 0 else '.')
            msg += (
                f'\n{tree[1]} retaliates and deals {riposte} damage' if game_state["character"][current_loc][target][
                                                                            "life"] > 0 else '')
            msg += (f'\nYou have {game_state["hero"]["CHARACTER_HEALTH"]} HP left.' if game_state["hero"][
                                                                                         "CHARACTER_HEALTH"] > 0 else ' and you are dead')
            result = styleFormat(msg + ".\n")

            if game_state["character"][current_loc][target]["life"] <= 0:
                del game_state['character'][current_loc][target]
                position()[2] = [1 if e == 2 else e for e in position()[2]]
            # endgame
            if game_state["hero"]["CHARACTER_HEALTH"] <= 0:
                game_state["current"]["RUN"] = 0
        else:
            result = styleFormat(f"\n{tree[1]} is not in {current_loc}\n")

    # --- Attack with Weapon ---
    elif action_type == 'attack_with':
        weapon = str(tree[2].replace('"', ''))
        target = str(tree[1].replace('"', ''))
        current_loc = position()[1]
        if game_state["damage"].get(weapon, 0) > 0:
            if pnj(current_loc, target):
                dmg = game_state["damage"][weapon]
                game_state["character"][current_loc][target]["life"] -= dmg
                if game_state["character"][current_loc][target]["life"] > 0:
                    riposte = game_state["character"][current_loc][target]["damage"]
                    game_state["hero"]["CHARACTER_HEALTH"] -= riposte

                msg = f"\nYou attack {tree[1]} and deal {dmg} damage"
                msg += (f' and {tree[1]} falls unconscious.' if game_state["character"][current_loc][target][
                                                                    "life"] <= 0 else '.')
                msg += (f'\n{tree[1]} retaliates and deals {riposte} damage' if
                        game_state["character"][current_loc][target]["life"] > 0 else '')
                msg += (f'\nYou have {game_state["hero"]["CHARACTER_HEALTH"]} HP left.' if game_state["hero"][
                                                                                             "CHARACTER_HEALTH"] > 0 else ' and you are dead')
                result = styleFormat(msg + ".\n")

                if game_state["character"][current_loc][target]["life"] <= 0:
                    del game_state['character'][current_loc][target]
                    position()[2] = [1 if e == 2 else e for e in position()[2]]

                if game_state["hero"]["CHARACTER_HEALTH"] <= 0:
                    game_state["current"]["RUN"] = 0
            else:
                result = styleFormat(f"\n{tree[1]} is not in {current_loc}\n")
        else:
            result = styleFormat(f"\nIt is not possible to use {tree[2]} for this action.\n")

    # --- Movement ---
    elif action_type == 'movement':
        if position()[2][tree[3]] == 0:
            result = styleFormat(f"\nNo exit in this direction from {position()[1]}\n")
        elif position()[2][tree[3]] == 1: 
            if (game_state['current']['FLOOR'] + tree[1] < 0 or game_state['current']['FLOOR'] + tree[1] >= len(game_state['current'])) or \
               (game_state["current"]["ROOM"] + tree[2] < 0 or game_state["current"]["ROOM"] + tree[2] >= len(game_state["DMAP"][game_state["current"]["FLOOR"]])):
                game_state["current"]["RUN"] = 0
                result = styleFormat("\nYou escaped from the manor!\n")
            else: 
                game_state["current"]["FLOOR"] += tree[1]
                game_state["current"]["ROOM"] += tree[2]
                result = styleFormat(f"\n{description(position()[1])()}\n")
        else: 
            result = styleFormat(f"\n{game_state['special'][position()[1]]['special']()}\n")
     
    # --- Inventory ---
    elif action_type == 'inventory':
        inv = hero_inventory()
        if len(inv) == 0:
            result = styleFormat("\nInventory empty\n")
        else:
            res_str = "Inventory:\n"
            for e in inv:
                res_str += f" - {e}\n"
            result = styleFormat(f"\n{res_str}\n")
    # --- functionnal ---
    elif tree[0] == 'pha' or tree[0] == 'var':
        result = None
    # --- Take Item ---
    elif action_type == 'take':
        item = str(tree[1].replace('"', ''))
        loc_inv = room_inventory(position()[1])
        if item in loc_inv and loc_inv[loc_inv.index(item) + 1] == 1:
            hero_inventory().append(item)    
            idx = loc_inv.index(item)
            del loc_inv[idx + 1]
            del loc_inv[idx]
            result = styleFormat(f"\nYou pick up {tree[1]}!\n")
        elif item in loc_inv:
            result = styleFormat(f"\nImpossible to take {item}!\n")
        else:
            result = styleFormat(f"\nThere is no {tree[1]} here.\n")

    # --- Use Item ---
    elif action_type == 'use':
        item = str(tree[1].replace('"', ''))
        res_use = ""
        if item in hero_inventory():
            res_use = use(item, "solo")()
        elif item in room_inventory(position()[1]):
            res_use = special(position()[1], "use", item)()
        if res_use:
            result = styleFormat(f"\n{res_use}\n")
        else:
            result = styleFormat(f"\nYou don't have {tree[1]}\n")

    # --- Use With ---
    elif action_type == 'use_with':
        item1 = str(tree[1].replace('"', ''))
        item2 = str(tree[2].replace('"', ''))
        hero_inv = hero_inventory()
        room_inv = room_inventory(position()[1])

        if item1 in hero_inv and (
                item2 in hero_inv or (item2 in room_inv and room_inv[room_inv.index(item2) + 1] == 1)):
            new_item = combine(item1, item2)
            if new_item:
                hero_inv.remove(item1)
                if item2 in hero_inv:
                    hero_inv.remove(item2)
                else:
                    room_inv.remove(item2)
                hero_inv.append(new_item)
                result = styleFormat(f"\n{use(item1, item2)()}\n")
            else:
                result = styleFormat(f"\nImpossible to use {tree[1]} and {tree[2]} together.\n")

        elif item1 in hero_inv and (item2 in room_inv and room_inv[room_inv.index(item2) + 1] == 2):
            new_item = combine(item1, item2)
            if new_item:
                hero_inv.remove(item1)
                idx = room_inv.index(item2)
                del room_inv[idx + 1];
                del room_inv[idx]
                room_inv.append(new_item);
                room_inv.append(0)
                position()[2] = [1 if e == 2 else e for e in position()[2]]
                result = styleFormat(f"\n{use(item1, item2)()}\n")
            else:
                result = styleFormat(f"\nImpossible to use {tree[1]} and {tree[2]} together.\n")

        elif item1 in hero_inv and (item2 in room_inv and room_inv[room_inv.index(item2) + 1] == 3):
            if pnj(position()[1], item2)["weak"] == item1.replace("'", "’"):
                new_item = combine(item1, item2)
                idx = room_inv.index(item2)
                del room_inv[idx + 1];
                del room_inv[idx]
                del game_state['character'][position()[1]][item2]
                hero_inv.remove(item1)
                room_inv.append(new_item);
                room_inv.append(0)
                position()[2] = [1 if e == 2 else e for e in position()[2]]
                result = styleFormat(f"\n{use(item1, item2)()}\n")
            else:
                result = styleFormat(f"\nImpossible to use {tree[1]} and {tree[2]} together.\n")
        else:
            result = styleFormat(f"\nYou don't have {tree[1]} or {tree[2]} is not here.\n")

    # --- Inspect ---
    elif action_type == 'inspect':
        res_insp = special(position()[1], "inspect", str(tree[1].replace('"','').strip().lower()))()
        if res_insp:
            result = styleFormat(f"\n{res_insp}\n")
        else:
            result = styleFormat(f"\nNothing special about {tree[1]}\n")

    # --- Editor Mode Logic ---
    elif tree[0] == 'new':
        game_state = {
                "current": {"RUN": 1, "FLOOR": 0, "ROOM": 0},
                "hero": {"CHARACTER_HEALTH": 10, "INV_CHARACTER": [], "DAMAGE_CHARACTER": 1},
                "mode": 1
        }
        result = styleFormat("\nEditor Mode:\n")
    elif tree[0] == 'set_floor':
        game_state["current"]["FLOOR"] = tree[1]
        result = game_state["current"]["FLOOR"]
    elif tree[0] == 'set_room':
        game_state["current"]["ROOM"] = tree[1] 
        result = game_state["current"]["ROOM"] 
    elif tree[0] == 'dmap_create':
        game_state["DMAP"] = [[x for x in range(tree[2])] for y in range(tree[1])]
        result = game_state["DMAP"]
    elif tree[0] == 'dmap_add':
        game_state["DMAP"][tree[1]][tree[2]] =[tree[2], str(tree[3].replace('"','')), [tree[4],tree[5],tree[6],tree[7],tree[8],tree[9]]]
        result = game_state["DMAP"][tree[1]][tree[2]]
    elif tree[0] == 'dmap_show':
        result = game_state["DMAP"][tree[1]][tree[2]]
    elif tree[0] == 'combine_create':
        game_state["combine"] = {str(tree[1].replace('"','')): {str(tree[2].replace('"','')): str(tree[3].replace('"',''))}}
        result = game_state["combine"]
    elif tree[0] == 'combine_add':
        game_state["combine"][str(tree[1].replace('"',''))] = {str(tree[2].replace('"','')): str(tree[3].replace('"',''))}
        result = game_state["combine"]
    elif tree[0] == 'combine_del':
        del game_state["combine"][str(tree[1].replace('"',''))]
        result = game_state["combine"]
    elif tree[0] == 'damage_create':
        game_state["damage"] = {str(tree[1].replace('"','')): tree[2]}
        result = game_state["damage"]
    elif tree[0] == 'damage_add':
        game_state["damage"][str(tree[1].replace('"',''))] = tree[2]
        result = game_state["damage"]
    elif tree[0] == 'damage_del':
        del game_state["damage"][str(tree[1].replace('"',''))]
        result = game_state["damage"]
    elif tree[0] == 'description_create':
        game_state["description"] = {str(tree[1].replace('"','')): eval(str(tree[2].replace('"','')))}
        result = game_state["description"]
    elif tree[0] == 'description_add':
        game_state["description"][str(tree[1].replace('"',''))] = eval(str(tree[2].replace('"','')))
        result = game_state["description"]
    elif tree[0] == 'description_del':
        del game_state["description"][str(tree[1].replace('"',''))]
        result = game_state["description"]
    elif tree[0] == 'inv_create':
        game_state["inventory"] = {str(tree[1].replace('"','')): [str(tree[2].replace('"','')), tree[3]]}
        result = game_state["inventory"]
    elif tree[0] == 'inv_add':
        item_key = str(tree[1].replace('"',''))
        if game_state["inventory"].get(item_key, 0):
            game_state["inventory"][item_key].append(str(tree[2].replace('"',''))) 
            game_state["inventory"][item_key].append(tree[3]) 
        else:
            game_state["inventory"][item_key] = [str(tree[2].replace('"','')), tree[3]]
        result = game_state["inventory"]
    elif tree[0] == 'inv_del':
        item_key = str(tree[1].replace('"',''))
        if game_state["inventory"].get(item_key, 0) and type(game_state["inventory"][item_key]) == list:  
            target_item = str(tree[2].replace('"',''))
            index = game_state["inventory"][item_key].index(target_item)
            del game_state["inventory"][item_key][index+1]
            del game_state["inventory"][item_key][index]
            result = game_state["inventory"]
        else:
            result = f"{item_key} is not in inventory."
    elif tree[0] == 'character_create':
        game_state["character"] = {str(tree[1].replace('"','')): {str(tree[2].replace('"','')): {"life":tree[3], "damage":tree[4], "inv": [str(tree[5].replace('"',''))], "weak": str(tree[6].replace('"',''))}}}
        result = game_state["character"]
    elif tree[0] == 'character_add':
        room_key = str(tree[1].replace('"',''))
        pnj_key = str(tree[2].replace('"',''))
        if game_state["character"].get(room_key, 0):
            game_state["character"][room_key][pnj_key] = {"life":tree[3], "damage":tree[4], "inv": [str(tree[5].replace('"',''))], "weak": str(tree[6].replace('"',''))}
        else: 
            game_state["character"][room_key] = {pnj_key: {"life":tree[3], "damage":tree[4], "inv": [str(tree[5].replace('"',''))], "weak": str(tree[6].replace('"',''))}}
        result = game_state["character"]
    elif tree[0] == 'character_del':
        room_key = str(tree[1].replace('"', ''))
        pnj_key = str(tree[2].replace('"',''))
        if game_state["character"].get(room_key, {"empty": 0}).get(pnj_key, 0):
            del game_state["character"][room_key][pnj_key]
            result = game_state["character"]
        else:
            result = f"There is no NPC {pnj_key} in {room_key}."
    elif tree[0] == 'usecase_create':
        game_state["useCase"] = {str(tree[1].replace('"','')): {str(tree[2].replace('"','')): eval(str(tree[3].replace('"','')))}}
        result = game_state["useCase"]
    elif tree[0] == 'usecase_add':
        game_state["useCase"][str(tree[1].replace('"',''))] = {str(tree[2].replace('"','')): eval(str(tree[3].replace('"','')))}
        result = game_state["useCase"]
    elif tree[0] == 'usecase_del':
        del game_state["useCase"][str(tree[1].replace('"',''))]
        result = game_state["useCase"]
    elif tree[0] == 'special_create':
        game_state["special"] = {str(tree[1].replace('"','')): {str(tree[2].replace('"','')): {str(tree[3].replace('"','')): eval(str(tree[4].replace('"','')))}}}
        result = game_state["special"]
    elif tree[0] == 'special_add':
        game_state["special"][str(tree[1].replace('"',''))] = {str(tree[2].replace('"','')): {str(tree[3].replace('"','')): eval(str(tree[4].replace('"','')))}}
        result = game_state["special"]
    elif tree[0] == 'special_del':
        del game_state["special"][str(tree[1].replace('"',''))]
        result = game_state["special"]
    elif tree[0] == 'welcome':
        game_state["welcome"] = str(tree[1].replace('"',''))
        result = game_state["welcome"]
    elif tree[0] == 'exit':
        game_state["current"]["RUN"] = 0
        result = "See you soon!"
    elif isinstance(tree, str):
        result = tree

    # Final logic
    if not result:
        result = None   
    if result is not None:
        print(result)

    return game_state

if __name__ == '__main__':
    # On lance le moteur avec le dictionnaire game_state déjà créé plus haut
    run_engine(game_state)
