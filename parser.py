"""
 Name ......... : parser.py
 Role ......... : Grammar rules and AST construction for the Manor DSL.
 Author ....... : Based on SLY library instructions: https://sly.readthedocs.io/en/latest/
                  Mickaël D. Pernet
 Version ...... : 2026 Refactor (Original 2022)
 License ...... : Project-based
"""

from sly import Lexer, Parser
from math import sqrt
from lexer import DLexer
from preprocessor import EN_Matrice, FR_Racinisation, PProcessor, Conform 
from game import game as game_data


class DParser(Parser):
    # Connect to the refactored Lexer tokens
    tokens = DLexer.tokens

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    # --- Help System ---
    @_('HELP')
    def statement(self, p):
        return ('help', 0)
    @_('expr HELP')
    def statement(self, p):
        return ('help', 0)
    @_('HELP expr')
    def statement(self, p):
        return ('help', 0)
    @_('expr HELP expr')
    def statement(self, p):
        return('help', 0)

    # --- Movement (Logic: action, floor_offset, room_offset, direction_index) ---
    @_('GO NORTH')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, -grid_size, 0)
    @_('GO NORTH expr')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, -grid_size, 0)
    @_('expr GO NORTH')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, -grid_size, 0)
    @_('expr GO NORTH expr')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, -grid_size, 0)
    
    @_('GO SOUTH')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, grid_size, 2)
    @_('GO SOUTH expr')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, grid_size, 2)
    @_('expr GO SOUTH')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, grid_size, 2)
    @_('expr GO SOUTH expr')
    def statement(self, p):
        grid_size = int(sqrt(len(game_data.get("DMAP", [[0]])[0])))
        return ('movement', 0, grid_size, 2)
    
    @_('GO EAST')
    def statement(self, p):
        return ('movement', 0, 1, 1)
    @_('GO EAST expr')
    def statement(self, p):
        return('movement', 0, 1, 1)
    @_('expr GO EAST')
    def statement(self, p):
        return('movement', 0, 1, 1)    
    @_('expr GO EAST expr')
    def statement(self, p):
        return('movement', 0, 1, 1) 
    
    @_('GO WEST')
    def statement(self, p):
        return ('movement', 0, -1, 3)
    @_('GO WEST expr')
    def statement(self, p):
        return('movement', 0, -1, 3)
    @_('expr GO WEST')
    def statement(self, p):
        return('movement', 0, -1, 3)
    @_('expr GO WEST expr')
    def statement(self, p):
        return('movement', 0, -1, 3)
    
    @_('DESCEND')
    def statement(self, p):
        return ('movement', -1, 0, 5)
    @_('DESCEND expr')
    def statement(self, p):
        return('movement', -1, 0, 5)
    @_('expr DESCEND')
    def statement(self, p):
        return('movement', -1, 0, 5)
    @_('expr DESCEND expr')
    def statement(self, p):
        return('movement', -1, 0, 5)
    
    @_('ASCEND')
    def statement(self, p):
        return ('movement', 1, 0, 4)
    @_('ASCEND expr')
    def statement(self, p):
        return('movement', 1, 0, 4)
    @_('expr ASCEND')
    def statement(self, p):
        return('movement', 1, 0, 4)
    @_('expr ASCEND expr')
    def statement(self, p):
        return('movement', 1, 0, 4)
    
    # --- Interaction & Combat ---
    @_('ATTACK STRING')
    def statement(self, p):
        return ('attack', p.STRING)
    @_('expr ATTACK STRING')
    def statement(self, p):
        return ('attack', p.STRING)
    @_('expr ATTACK STRING expr')
    def statement(self, p):
        return ('attack', p.STRING)
    
    @_('ATTACK WORD')
    def statement(self, p):
        return ('attack', p.WORD) 
    @_('ATTACK WORD expr')
    def statement(self, p):
        return ('attack', p.WORD)
    @_('expr ATTACK WORD')
    def statement(self, p):
        return ('attack', p.WORD)  
    @_('expr ATTACK WORD expr')
    def statement(self, p):
        return ('attack', p.WORD)  
    
    @_('ATTACK STRING WITH STRING')
    def statement(self, p):
        return ('attack_with', p.STRING0, p.STRING1)
    @_('ATTACK STRING WITH STRING expr')
    def statement(self, p):
        return ('attack_with', p.STRING0, p.STRING1) 
    @_('expr ATTACK STRING WITH STRING')
    def statement(self, p):
        return ('attack_with', p.STRING0, p.STRING1) 
    @_('expr ATTACK STRING WITH STRING expr')
    def statement(self, p):
        return ('attack_with', p.STRING0, p.STRING1) 
    
    @_('ATTACK WORD WITH WORD')
    def statement(self, p):
        return ('attack_with', p.WORD0, p.WORD1)
    @_('ATTACK WORD WITH WORD expr')
    def statement(self, p):
        return ('attack_with', p.WORD0, p.WORD1)
    @_('expr ATTACK WORD WITH WORD')
    def statement(self, p):
        return ('attack_with', p.WORD0, p.WORD1)
    @_('expr ATTACK WORD WITH WORD expr')
    def statement(self, p):
        return ('attack_with', p.WORD0, p.WORD1)
    
    @_('ATTACK STRING WITH WORD')
    def statement(self, p):
        return ('attack_with', p.STRING, p.WORD)
    @_('ATTACK STRING WITH WORD expr')
    def statement(self, p):
        return ('attack_with', p.STRING, p.WORD)
    @_('expr ATTACK STRING WITH WORD')
    def statement(self, p):
        return ('attack_with', p.STRING, p.WORD)
    @_('expr ATTACK STRING WITH WORD expr')
    def statement(self, p):
        return ('attack_with', p.STRING, p.WORD)
    
    @_('ATTACK WORD WITH STRING')
    def statement(self, p):
        return ('attack_with', p.WORD, p.STRING)
    @_('ATTACK WORD WITH STRING expr')
    def statement(self, p):
        return ('attack_with', p.WORD, p.STRING)
    @_('expr ATTACK WORD WITH STRING')
    def statement(self, p):
        return ('attack_with', p.WORD, p.STRING)
    @_('expr ATTACK WORD WITH STRING expr')
    def statement(self, p):
        return ('attack_with', p.WORD, p.STRING)
    
    
    # --- Inventory Actions ---
    @_('INVENTORY')
    def statement(self, p):
        return ('inventory', 0) 
    @_('INVENTORY expr')
    def statement(self, p):
        return ('inventory', 0)
    @_('expr INVENTORY')
    def statement(self, p):
        return ('inventory', 0) 
    @_('expr INVENTORY expr')
    def statement(self, p):
        return ('inventory', 0) 
    
    @_('INSPECT INVENTORY')
    def statement(self, p):
        return ('inventory', 0)
    @_('INSPECT INVENTORY expr')
    def statement(self, p):
        return ('inventory', 0)
    @_('expr INSPECT INVENTORY')
    def statement(self, p):
        return ('inventory', 0)
    @_('expr INSPECT INVENTORY expr')
    def statement(self, p):
        return ('inventory', 0)

    # --- Inspection / Inspect ---
    @_('INSPECT STRING')
    def statement(self, p):
        return ('inspect', p.STRING)
    @_('INSPECT STRING expr')
    def statement(self, p):
        return ('inspect', p.STRING) 
    @_('expr INSPECT STRING')
    def statement(self, p):
        return ('inspect', p.STRING) 
    @_('expr INSPECT STRING expr')
    def statement(self, p):
        return ('inspect', p.STRING) 
    
    @_('INSPECT WORD')
    def statement(self, p):
        return ('inspect', p.WORD)
    @_('INSPECT WORD expr')
    def statement(self, p):
        return ('inspect', p.WORD)
    @_('expr INSPECT WORD')
    def statement(self, p):
        return ('inspect', p.WORD)  
    @_('expr INSPECT WORD expr')
    def statement(self, p):
        return ('inspect', p.WORD) 

    # --- Object Use ---
    @_('USE STRING')
    def statement(self, p):
        return ('use', p.STRING)
    @_('USE STRING expr')
    def statement(self, p):
        return ('use', p.STRING)
    @_('expr USE STRING')
    def statement(self, p):
        return ('use', p.STRING)
    @_('expr USE STRING expr')
    def statement(self, p):
        return ('use', p.STRING)

    @_('USE WORD')
    def statement(self, p):
        return ('use', p.WORD)
    @_('USE WORD expr')
    def statement(self, p):
        return ('use', p.WORD)
    @_('expr USE WORD')
    def statement(self, p):
        return ('use', p.WORD)
    @_('expr USE WORD expr')
    def statement(self, p):
        return ('use', p.WORD) 
   
    @_('USE STRING WITH STRING')
    def statement(self, p):
        return ('use_with', p.STRING0, p.STRING1)
    @_('USE STRING WITH STRING expr')
    def statement(self, p):
        return ('use_with', p.STRING0, p.STRING1)
    @_('expr USE STRING WITH STRING')
    def statement(self, p):
        return ('use_with', p.STRING0, p.STRING1)
    @_('expr USE STRING WITH STRING expr')
    def statement(self, p):
        return ('use_with', p.STRING0, p.STRING1)
    
    @_('USE STRING WITH WORD')
    def statement(self, p):
        return ('use_with', p.STRING, p.WORD)
    @_('USE STRING WITH WORD expr')
    def statement(self, p):
        return ('use_with', p.STRING, p.WORD)
    @_('expr USE STRING WITH WORD')
    def statement(self, p):
        return ('use_with', p.STRING, p.WORD)
    @_('expr USE STRING WITH WORD expr')
    def statement(self, p):
        return ('use_with', p.STRING, p.WORD)
 
    @_('USE WORD WITH WORD')
    def statement(self, p):
        return ('use_with', p.WORD0, p.WORD1)
    @_('USE WORD WITH WORD expr')
    def statement(self, p):
        return ('use_with', p.WORD0, p.WORD1)   
    @_('expr USE WORD WITH WORD')
    def statement(self, p):
        return ('use_with', p.WORD0, p.WORD1)   
    @_('expr USE WORD WITH WORD expr')
    def statement(self, p):
        return ('use_with', p.WORD0, p.WORD1) 
 
    @_('USE WORD WITH STRING')
    def statement(self, p):
        return ('use_with', p.WORD, p.STRING)   
    @_('USE WORD WITH STRING expr')
    def statement(self, p):
        return ('use_with', p.WORD, p.STRING)  
    @_('expr USE WORD WITH STRING')
    def statement(self, p):
        return ('use_with', p.WORD, p.STRING) 
    @_('expr USE WORD WITH STRING expr')
    def statement(self, p):
        return ('use_with', p.WORD, p.STRING)   
 
    # --- Picking up items ---
    @_('TAKE STRING')
    def statement(self, p):
        return ('take', p.STRING)
    @_('TAKE STRING expr')
    def statement(self, p):
        return ('take', p.STRING) 
    @_('expr TAKE STRING')
    def statement(self, p):
        return ('take', p.STRING)
    @_('expr TAKE STRING expr')
    def statement(self, p):
        return ('take', p.STRING) 
              
    @_('TAKE WORD')
    def statement(self, p):
        return ('take', p.WORD)
    @_('TAKE WORD expr')
    def statement(self, p):
        return ('take', p.WORD)  
    @_('expr TAKE WORD')
    def statement(self, p):
        return ('take', p.WORD)  
    @_('expr TAKE WORD expr') 
    def statement(self, p):
        return ('take', p.WORD)

    # --- Editor Mode Commands ---
    @_('NEW_GAME')
    def statement(self, p):
        return ('new', 0)
    @_('SET_FLOOR NUMBER')
    def statement(self, p):
        return ('set_floor', p.NUMBER)  
    @_('SET_ROOM NUMBER')
    def statement(self, p):
        return ('set_room', p.NUMBER)

    # DMAP: {game: {"DMAP": [[x, "name", [0,0,0,0,0,0]]]}
    @_('GENERATE SET_DMAP NUMBER NUMBER')
    def statement(self, p):
        return ('dmap_create', p.NUMBER0, p.NUMBER1)
    @_('SET_DMAP NUMBER NUMBER STRING NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER')
    def statement(self, p):
        return ('dmap_add', p.NUMBER0, p.NUMBER1, p.STRING, p.NUMBER2, p.NUMBER3, p.NUMBER4, p.NUMBER5, p.NUMBER6,
                    p.NUMBER7)
    @_('SHOW SET_DMAP NUMBER NUMBER')
    def statement(self, p):
        return ('dmap_show', p.NUMBER0, p.NUMBER1)

    ## Combination combine: {game: {"combine": {"element1": {"element2": "element3"}}}} 
    @_('GENERATE COMBINE WORD WORD WORD')
    def statement(self, p):
        return ('combine_create', p.WORD0, p.WORD1, p.WORD2)
    @_('GENERATE COMBINE STRING WORD WORD')
    def statement(self, p):
        return ('combine_create', p.STRING, p.WORD0, p.WORD1)
    @_('GENERATE COMBINE WORD STRING WORD')
    def statement(self, p):
        return ('combine_create', p.WORD0, p.STRING, p.WORD1)
    @_('GENERATE COMBINE WORD WORD STRING')
    def statement(self, p):
        return ('combine_create', p.WORD0, p.WORD1, p.STRING)
    @_('GENERATE COMBINE STRING STRING WORD')
    def statement(self, p):
        return ('combine_create', p.STRING0, p.STRING1, p.WORD)
    @_('GENERATE COMBINE STRING WORD STRING')
    def statement(self, p):
        return ('combine_create', p.STRING0, p.WORD, p.STRING1)
    @_('GENERATE COMBINE WORD STRING STRING')
    def statement(self, p):
        return ('combine_create', p.WORD, p.STRING0, p.STRING1)
    @_('GENERATE COMBINE STRING STRING STRING')
    def statement(self, p):
        return ('combine_create', p.STRING0, p.STRING1, p.STRING2)

    @_('ADD COMBINE WORD WORD WORD')
    def statement(self, p):
        return ('combine_add', p.WORD0, p.WORD1, p.WORD2)
    @_('ADD COMBINE STRING WORD WORD')
    def statement(self, p):
        return ('combine_add', p.STRING, p.WORD0, p.WORD1)
    @_('ADD COMBINE WORD STRING WORD')
    def statement(self, p):
        return ('combine_add', p.WORD0, p.STRING, p.WORD1)
    @_('ADD COMBINE WORD WORD STRING')
    def statement(self, p):
        return ('combine_add', p.WORD0, p.WORD1, p.STRING)
    @_('ADD COMBINE STRING STRING WORD')
    def statement(self, p):
        return ('combine_add', p.STRING0, p.STRING1, p.WORD)
    @_('ADD COMBINE STRING WORD STRING')
    def statement(self, p):
        return ('combine_add', p.STRING0, p.WORD, p.STRING1)
    @_('ADD COMBINE WORD STRING STRING')
    def statement(self, p):
        return ('combine_add', p.WORD, p.STRING0, p.STRING1)
    @_('ADD COMBINE STRING STRING STRING')
    def statement(self, p):
        return ('combine_add', p.STRING0, p.STRING1, p.STRING2)
    
    @_('DESTROY COMBINE WORD')
    def statement(self, p):
        return ('combine_del', p.WORD)
    @_('DESTROY COMBINE STRING')
    def statement(self, p):
        return ('combine_del', p.STRING)
    
    # Combination damage: {game: {"damage": {"element1": "element2"}}}
    @_('GENERATE DAMAGE_TABLE WORD NUMBER')
    def statement(self, p):
        return ('damage_create', p.WORD, p.NUMBER)
    @_('GENERATE DAMAGE_TABLE STRING NUMBER')
    def statement(self, p):
        return ('damage_create', p.STRING, p.NUMBER)
    @_('ADD DAMAGE_TABLE WORD NUMBER')
    def statement(self, p):
        return ('damage_add', p.WORD, p.NUMBER)
    @_('ADD DAMAGE_TABLE STRING NUMBER')
    def statement(self, p):
        return ('damage_add', p.STRING, p.NUMBER)
    @_('DESTROY DAMAGE_TABLE WORD')
    def statement(self, p):
        return ('damage_del', p.WORD)
    @_('DESTROY DAMAGE_TABLE STRING')
    def statement(self, p):
        return ('damage_del', p.STRING)
    
    # description: {game: {"description": {"E1", "lambda: E2"}}}
    @_('GENERATE SET_DESCRIPTION WORD STRING')
    def statement(self, p):
        return ('description_create', p.WORD, p.STRING)
    @_('ADD SET_DESCRIPTION WORD STRING')
    def statement(self, p):
        return ('description_add', p.WORD, p.STRING)
    @_('DESTROY SET_DESCRIPTION WORD')
    def statement(self, p):
        return ('description_del', p.WORD)
    
    # inventory per room: {"inventory": {"room": [object, ind]}}
    @_('GENERATE SET_INV WORD WORD NUMBER')
    def statement(self, p):
        return ('inv_create', p.WORD0, p.WORD1, p.NUMBER)
    @_('GENERATE SET_INV STRING WORD NUMBER')
    def statement(self, p):
        return ('inv_create', p.STRING, p.WORD, p.NUMBER)
    @_('GENERATE SET_INV WORD STRING NUMBER')
    def statement(self, p):
        return ('inv_create', p.WORD, p.STRING, p.NUMBER)
    @_('GENERATE SET_INV STRING STRING NUMBER')
    def statement(self, p):
        return ('inv_create', p.STRING0, p.STRING1, p.NUMBER)
    
    @_('ADD SET_INV WORD WORD NUMBER') 
    def statement(self, p):
        return ('inv_add', p.WORD0, p.WORD1, p.NUMBER)
    @_('ADD SET_INV WORD STRING NUMBER') 
    def statement(self, p):
        return ('inv_add', p.WORD, p.STRING, p.NUMBER)
    @_('ADD SET_INV STRING WORD NUMBER') 
    def statement(self, p):
        return ('inv_add', p.STRING, p.WORD, p.NUMBER)
    @_('ADD SET_INV STRING STRING NUMBER') 
    def statement(self, p):
        return ('inv_add', p.STRING0, p.STRING1, p.NUMBER)
    
    @_('DESTROY SET_INV WORD WORD') 
    def statement(self, p):
        return ('inv_del', p.WORD0, p.WORD1)
    @_('DESTROY SET_INV STRING WORD') 
    def statement(self, p):
        return ('inv_del', p.STRING, p.WORD)
    @_('DESTROY SET_INV WORD STRING') 
    def statement(self, p):
        return ('inv_del', p.WORD, p.STRING)
    @_('DESTROY SET_INV STRING STRING') 
    def statement(self, p):
        return ('inv_del', p.STRING0, p.STRING1)
    
    # Character: {game: {"character": {"room": {"name":{"life":5, "damage":5, "inv":[], "weak": "faiblesse"}}}}}
    @_('GENERATE SET_CHARACTER WORD WORD NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_create', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.WORD2, p.WORD3)
    @_('GENERATE SET_CHARACTER STRING WORD NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_create', p.STRING, p.WORD0, p.NUMBER0, p.NUMBER1, p.WORD1, p.WORD2)
    @_('GENERATE SET_CHARACTER WORD STRING NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_create', p.WORD0, p.STRING, p.NUMBER0, p.NUMBER1, p.WORD1, p.WORD2)
    @_('GENERATE SET_CHARACTER WORD WORD NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_create', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.STRING, p.WORD2)
    @_('GENERATE SET_CHARACTER WORD WORD NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_create', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.WORD2, p.STRING)
    @_('GENERATE SET_CHARACTER STRING STRING NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_create', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.WORD1, p.WORD2)
    @_('GENERATE SET_CHARACTER STRING WORD NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_create', p.STRING0, p.WORD0, p.NUMBER0, p.NUMBER1, p.STRING1, p.WORD1)
    @_('GENERATE SET_CHARACTER STRING WORD NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_create', p.STRING0, p.WORD0, p.NUMBER0, p.NUMBER1, p.WORD1, p.STRING1)
    @_('GENERATE SET_CHARACTER WORD STRING NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_create', p.WORD0, p.STRING0, p.NUMBER0, p.NUMBER1, p.STRING1, p.WORD1)
    @_('GENERATE SET_CHARACTER WORD STRING NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_create', p.WORD0, p.STRING0, p.NUMBER0, p.NUMBER1, p.WORD1, p.STRING1)
    @_('GENERATE SET_CHARACTER WORD WORD NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_create', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.STRING0, p.STRING1)
    @_('GENERATE SET_CHARACTER STRING STRING NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_create', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.STRING2, p.WORD)
    @_('GENERATE SET_CHARACTER STRING STRING NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_create', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.WORD, p.STRING2)
    @_('GENERATE SET_CHARACTER STRING WORD NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_create', p.STRING0, p.WORD, p.NUMBER0, p.NUMBER1, p.STRING1, p.STRING2)
    @_('GENERATE SET_CHARACTER WORD STRING NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_create', p.WORD, p.STRING0, p.NUMBER0, p.NUMBER1, p.STRING1, p.STRING2)
    @_('GENERATE SET_CHARACTER STRING STRING NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_create', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.STRING2, p.STRING3)

    #Add
    @_('ADD SET_CHARACTER WORD WORD NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_add', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.WORD2, p.WORD3)
    @_('ADD SET_CHARACTER STRING WORD NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_add', p.STRING, p.WORD0, p.NUMBER0, p.NUMBER1, p.WORD1, p.WORD2)
    @_('ADD SET_CHARACTER WORD STRING NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_add', p.WORD0, p.STRING, p.NUMBER0, p.NUMBER1, p.WORD1, p.WORD2)
    @_('ADD SET_CHARACTER WORD WORD NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_add', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.STRING, p.WORD2)
    @_('ADD SET_CHARACTER WORD WORD NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_add', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.WORD2, p.STRING)
    @_('ADD SET_CHARACTER STRING STRING NUMBER NUMBER WORD WORD')
    def statement(self, p):
        return ('character_add', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.WORD1, p.WORD2)
    @_('ADD SET_CHARACTER STRING WORD NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_add', p.STRING0, p.WORD0, p.NUMBER0, p.STRING1, p.STRING1, p.WORD1)
    @_('ADD SET_CHARACTER STRING WORD NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_add', p.STRING0, p.WORD0, p.NUMBER0, p.NUMBER1, p.WORD1, p.STRING1)
    @_('ADD SET_CHARACTER WORD STRING NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_add', p.WORD0, p.STRING0, p.NUMBER0, p.NUMBER1, p.STRING1, p.WORD1)
    @_('ADD SET_CHARACTER WORD STRING NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_add', p.WORD0, p.STRING0, p.NUMBER0, p.NUMBER1, p.WORD1, p.STRING1)
    @_('ADD SET_CHARACTER WORD WORD NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_add', p.WORD0, p.WORD1, p.NUMBER0, p.NUMBER1, p.STRING0, p.STRING1)
    @_('ADD SET_CHARACTER STRING STRING NUMBER NUMBER STRING WORD')
    def statement(self, p):
        return ('character_add', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.STRING2, p.WORD)
    @_('ADD SET_CHARACTER STRING STRING NUMBER NUMBER WORD STRING')
    def statement(self, p):
        return ('character_add', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.WORD, p.STRING2)
    @_('ADD SET_CHARACTER STRING WORD NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_add', p.STRING0, p.WORD, p.NUMBER0, p.NUMBER1, p.STRING1, p.STRING2)
    @_('ADD SET_CHARACTER WORD STRING NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_add', p.WORD, p.STRING0, p.NUMBER0, p.NUMBER1, p.STRING1, p.STRING2)
    @_('ADD SET_CHARACTER STRING STRING NUMBER NUMBER STRING STRING')
    def statement(self, p):
        return ('character_add', p.STRING0, p.STRING1, p.NUMBER0, p.NUMBER1, p.STRING2, p.STRING3)

    @_('DESTROY SET_CHARACTER WORD WORD')
    def statement(self, p):
        return ('character_del', p.WORD0, p.WORD1)
    @_('DESTROY SET_CHARACTER STRING WORD')
    def statement(self, p):
        return ('character_del', p.STRING, p.WORD)
    @_('DESTROY SET_CHARACTER WORD STRING')
    def statement(self, p):
        return ('character_del', p.WORD, p.STRING)
    @_('DESTROY SET_CHARACTER STRING STRING')
    def statement(self, p):
        return ('character_del', p.STRING0, p.STRING1)

    #useCase {"game": {"useCase": {E1: {E2: "lambda: E3"}}}}
    @_('GENERATE SET_USECASE WORD WORD STRING')
    def statement(self, p):
        return ('usecase_create', p.WORD0, p.WORD1, p.STRING)
    @_('GENERATE SET_USECASE STRING WORD STRING')
    def statement(self, p):
        return ('usecase_create', p.STRING0, p.WORD, p.STRING1)
    @_('GENERATE SET_USECASE WORD STRING STRING')
    def statement(self, p):
        return ('usecase_create', p.WORD, p.STRING0, p.STRING1)
    @_('GENERATE SET_USECASE STRING STRING STRING')
    def statement(self, p):
        return ('usecase_create', p.STRING0, p.STRING1, p.STRING2)

    @_('ADD SET_USECASE WORD WORD STRING')
    def statement(self, p):
        return ('usecase_add', p.WORD0, p.WORD1, p.STRING)
    @_('ADD SET_USECASE STRING WORD STRING')
    def statement(self, p):
        return ('usecase_add', p.STRING0, p.WORD, p.STRING1)
    @_('ADD SET_USECASE WORD STRING STRING')
    def statement(self, p):
        return ('usecase_add', p.WORD, p.STRING0, p.STRING1)
    @_('ADD SET_USECASE STRING STRING STRING')
    def statement(self, p):
        return ('usecase_add', p.STRING0, p.STRING1, p.STRING2)
  
    @_('DESTROY SET_USECASE WORD')
    def statement(self, p):
        return ('usecase_del', p.WORD)
    @_('DESTROY SET_USECASE STRING')
    def statement(self, p):
        return ('usecase_del', p.STRING)

    # Special: {"game": {"special": {E1: {E2: {E3: "lambda: E4"}}}}}
    @_('GENERATE SET_SPECIAL WORD WORD WORD STRING')
    def statement(self, p):
        return ('special_create', p.WORD0, p.WORD1, p.WORD2, p.STRING)
    @_('GENERATE SET_SPECIAL STRING WORD WORD STRING')
    def statement(self, p):
        return ('special_create', p.STRING0, p.WORD0, p.WORD1, p.STRING1)
    @_('GENERATE SET_SPECIAL WORD STRING WORD STRING')
    def statement(self, p):
        return ('special_create', p.WORD0, p.STRING0, p.WORD1, p.STRING1)
    @_('GENERATE SET_SPECIAL WORD WORD STRING STRING')
    def statement(self, p):
        return ('special_create', p.WORD0, p.WORD1, p.STRING0, p.STRING1)
    @_('GENERATE SET_SPECIAL STRING STRING WORD STRING')
    def statement(self, p):
        return ('special_create', p.STRING0, p.STRING1, p.WORD, p.STRING2)
    @_('GENERATE SET_SPECIAL STRING WORD STRING STRING')
    def statement(self, p):
        return ('special_create', p.STRING0, p.WORD, p.STRING1, p.STRING2)
    @_('GENERATE SET_SPECIAL WORD STRING STRING STRING')
    def statement(self, p):
        return ('special_create', p.WORD, p.STRING0, p.STRING1, p.STRING2)
    @_('GENERATE SET_SPECIAL STRING STRING STRING STRING')
    def statement(self, p):
        return ('special_create', p.STRING0, p.STRING1, p.STRING2, p.STRING3)
    
    # add
    @_('ADD SET_SPECIAL WORD WORD WORD STRING')
    def statement(self, p):
        return ('special_add', p.WORD0, p.WORD1, p.WORD2, p.STRING)
    @_('ADD SET_SPECIAL STRING WORD WORD STRING')
    def statement(self, p):
        return ('special_add', p.STRING0, p.WORD0, p.WORD1, p.STRING1)
    @_('ADD SET_SPECIAL WORD STRING WORD STRING')
    def statement(self, p):
        return ('special_add', p.WORD0, p.STRING0, p.WORD1, p.STRING1)
    @_('ADD SET_SPECIAL WORD WORD STRING STRING')
    def statement(self, p):
        return ('special_add', p.WORD0, p.WORD1, p.STRING0, p.STRING1)
    @_('ADD SET_SPECIAL STRING STRING WORD STRING')
    def statement(self, p):
        return ('special_add', p.STRING0, p.STRING1, p.WORD, p.STRING2)
    @_('ADD SET_SPECIAL STRING WORD STRING STRING')
    def statement(self, p):
        return ('special_add', p.STRING0, p.WORD, p.STRING1, p.STRING2)
    @_('ADD SET_SPECIAL WORD STRING STRING STRING')
    def statement(self, p):
        return ('special_add', p.WORD, p.STRING0, p.STRING1, p.STRING2)
    @_('ADD SET_SPECIAL STRING STRING STRING STRING')
    def statement(self, p):
        return ('special_add', p.STRING0, p.STRING1, p.STRING2, p.STRING3)
    
    # del
    @_('DESTROY SET_SPECIAL WORD')
    def statement(self, p):
        return ('special_del', p.WORD)
    @_('DESTROY SET_SPECIAL STRING')
    def statement(self, p):
        return ('special_del', p.STRING)
    
    @_('GENERATE SET_WELCOME STRING')
    def statement(self, p):
        return ('welcome', p.STRING)

    @_('QUIT')
    def statement(self, p):
        return ('exit', 0)

    # --- Low-level Expressions (Handling multi-word or quoted strings) ---
    @_('WORD')
    def expr(self, p):
        return ('var', p.WORD)
    @_('STRING')
    def expr(self, p):
        return ('pha', p.STRING)
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
    
    # STRING Construction rules for flexibility
    @_('expr')
    def statement(self, p):
        return (p.expr)
    @_('WORD STRING')
    def expr(self, p):
        return ('pha', p.WORD + " " + p.STRING)
    @_('STRING WORD')
    def expr(self, p):
        return ('pha', p.STRING + " " + p.WORD)
    @_('STRING STRING')
    def expr(self, p):
        return ('pha', p.STRING0 + " " + p.STRING1)
    @_('STRING STRING STRING')
    def expr(self, p):
        return ('pha', p.STRING0 + " " + p.STRING1 + " " + p.STRING2)
    @_('WORD WORD')
    def expr(self, p):
        return ('pha', p.WORD0 + " " + p.WORD1)
    @_('WORD WORD WORD')
    def expr(self, p):
        return ('pha', p.WORD0 + " " + p.WORD1 +  " " + p.WORD2)
    @_('STRING WORD WORD')
    def expr(self, p):
        return ('pha', p.STRING + " " + p.WORD0 +  " " + p.WORD1)
    @_('WORD STRING WORD')
    def expr(self, p):
        return ('pha', p.WORD0 + " " + p.STRING +  " " + p.WORD1)
    @_('WORD WORD STRING')
    def expr(self, p):
        return ('pha', p.WORD0 + " " + p.WORD1 +  " " + p.STRING)
    @_('STRING STRING WORD')
    def expr(self, p):
        return ('pha', p.STRING0 + " " + p.STRING1 +  " " + p.WORD)
    @_('STRING WORD STRING')
    def expr(self, p):
        return ('pha', p.STRING0 + " " + p.WORD +  " " + p.STRING1)
    @_('WORD STRING STRING')
    def expr(self, p):
        return ('pha', p.WORD + " " + p.STRING0 +  " " + p.STRING1)

    # Error handling for the parser
    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} ('{p.value}')")
        else:
            print("Syntax error at EOF")
"""
TEST Section (Debug)
"""
if __name__ == '__main__':
    from preprocessor import EN_Matrice, FR_Racinisation, PProcessor
    lexer = DLexer()
    parser = DParser()
    while True:
        try:
            text = input('Parser > ') + " "
        except EOFError:
            break
        if text.strip():
            tokens = lexer.tokenize(PProcessor(text, EN_Matrice, FR_Racinisation).replace("'", " "))
            tree = parser.parse(tokens)
            print(tree)