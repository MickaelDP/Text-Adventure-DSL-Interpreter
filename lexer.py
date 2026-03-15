"""
 Name ......... : lexer.py
 Role ......... : Tokenizer class for the Manor DSL - Handles command tokenization.
 Author ....... : Based on SLY library instructions: https://sly.readthedocs.io/en/latest/
                  Mickaël D. Pernet
 Version ...... : 2026 Refactor (Original 2022)
 License ...... : Project-based
"""

from sly import Lexer

class DLexer(Lexer):
    """
    Lexer class to tokenize commands.
    The preprocessor handles translation, allowing the lexer to focus on the core DSL.

    Args:
        Lexer (lexer): Lexer from the SLY library.

    Returns:
        list: A list of token objects determined by the input parameters.
    """

    # --- Token List ---
    tokens = { 
        HELP, GO, ATTACK, WITH, DESCEND, EAST, INVENTORY, ASCEND, 
        NORTH, WEST, TAKE, SOUTH, USE, INSPECT,
        NEW_GAME, GENERATE, SHOW, ADD, DESTROY, COMBINE, 
        DAMAGE_TABLE, SET_DESCRIPTION, SET_DMAP, SET_FLOOR, SET_INV, 
        SET_ROOM, SET_CHARACTER, SET_SPECIAL, SET_USECASE, SET_WELCOME, 
        QUIT, WORD, NUMBER, STRING
    }
    
    ignore = '\t '
    # --- Token Definitions ---
    # Standard Actions
    HELP    = r'HELP'
    GO      = r'GO'
    ATTACK  = r'ATTACK'
    WITH    = r'WITH'
    DESCEND = r'DESCEND'
    EAST    = r'EAST'
    INVENTORY = r'INVENTORY'
    ASCEND  = r'ASCEND'
    NORTH   = r'NORTH'
    WEST    = r'WEST'
    TAKE    = r'TAKE'
    SOUTH   = r'SOUTH'
    USE     = r'USE'
    INSPECT = r'INSPECT'

    # Editor / DSL Commands
    NEW_GAME        = r'NEW_GAME'
    GENERATE        = r'GENERATE'
    SHOW            = r'SHOW'
    ADD             = r'ADD'
    DESTROY         = r'DESTROY'
    COMBINE         = r'COMBINER'
    DAMAGE_TABLE    = r'DAMAGE_TABLE'
    SET_DESCRIPTION = r'SET_DESCRIPTION'
    SET_DMAP        = r'SET_DMAP'
    SET_FLOOR       = r'SET_FLOOR'
    SET_INV         = r'SET_INV'
    SET_ROOM        = r'SET_ROOM'
    SET_CHARACTER   = r'SET_CHARACTER'
    SET_SPECIAL     = r'SET_SPECIAL'
    SET_USECASE     = r'SET_USECASE'
    SET_WELCOME     = r'SET_WELCOME'
    QUIT            = r'QUIT'

    # Basic Types
    WORD    = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING  = r'\".*?\"'

    # --- Type Definitions & Special Handling ---
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
        
    # Error handling
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


"""
Test section to verify tokenization:
"""
if __name__ == '__main__':
    lexer = DLexer()
    while True:
        try:
            text = input('Lexer Debug > ')
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)
            for token in tokens:
                print(token)
