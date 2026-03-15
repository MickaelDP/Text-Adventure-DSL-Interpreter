"""
 Nom ......... : preprocessor.py
 Rôle ........ : Data and functions for the preprocessing layer, providing flexibility 
                 in command expression (multi-language and stemming).
 Auteur ...... : Mickaël D. Pernet
 Version ..... : 2026 Refactor (Original 2022)
 Licence ..... : Project-based
"""

from sly import Lexer
from lexer import DLexer
import re


"""
Correspondence table for English translation.
Maps various English synonyms to the core Engine Tokens.
"""
EN_Matrice = [
              ['HELP', 'HELP', 'AIDE'],
              ['GO', 'GO', 'GO TO', 'WALK', 'ALL'],
              ['ATTACK', 'ATTACK', 'HIT', 'ATT'],
              ['WITH', 'WITH', 'AVEC'],
              ['DESCEND', 'GO DOWN', 'DESC'],
              ['EQUIP', 'PUT', 'EQUIP'],
              ['EAST', 'EAST', 'EST'],
              ['INVENTORY', 'INVENTORY', 'BAG', 'INV'],
              ['ASCEND', 'GO UPSTAIRS', 'ASCEND', 'MONT'],
              ['NORTH', 'NORTH', 'NORD'],
              ['WEST', 'WEST', 'OUEST'],
              ['TAKE', 'TAKE', 'TO TAKE', 'PICK UP', 'PREN'],
              ['QUIT', 'EXIT', 'QUIT'],
              ['SOUTH', 'SOUTH', 'SUD'],
              ['USE', 'USE', 'UTILIZE', 'UTIL'],
              ['INSPECT', 'LOOK', 'LOOK AT', 'EXAMINE', 'VOIR']
            ]

"""
Correspondence table for French expressions, conjugations, and synonyms.
Maps them to the final Engine Tokens.
"""

FR_Racinisation = [ 
                    ["HELP", "AIDE", "AIDES", "HELP"],

                    ["GO", "ALL", "ALLEZ", "ALLEZ A", "VA", "VA A", "ALLER", "ALLER A", "GO"],
                    ["ATTACK", "ATT", "ATTAQUE", "ATTAQUER", "FRAPPE", "TAPE", "FRAPPER", "TAPER", "ATTACK"],
                    ["DESCEND", "DESC", "DESCENDRE", "DESCEND"],
                    ["EQUIP", "EQUIPE", "EQUIPES", "EQUIPER"],
                    ["EAST", "EST", "L'EST", "LEST", "L’EST", "EAST"],
                    ["INVENTORY", "INV", "INVENTAIRE", "SAC", "INVENTORY"],
                    ["ASCEND", "MONT", "MONTE", "MONTER", "ASCEND"],
                    ["NORTH", "NORD", "LE NORD", "AU NORD", "NORTH"],
                    ["WEST", "OUEST", "L'OUEST", "LOUEST", "L’OUEST", "WEST"],
                    ["TAKE", "PREN", "PREND", "PRENDS", "PRENDRE", "RAMASSE", "RAMASSER", "TAKE"],
                    ["QUIT", "QUIT", "QUITTER", "EXIT"],
                    ["SOUTH", "SUD", "LE SUD", "AU SUD", "SOUTH"],
                    ["USE", "UTIL", "UTILISE", "UTILISES", "UTILISER", "USE"],
                    ["INSPECT", "VOIR", "REGARDE", "REGARDES", "REGARDER", "REGARDEZ", "INSPECT"],
                  ] 

def PProcessor(string, lexique, racine):
    """
    Acts as a pre-processor by replacing French or english expressions 
    with their equivalents in the language grammar.

    Args:
        string (str): Instruction line (raw input).
        lexique (matrix): Multi-language mapping matrix.
        racine (matrix): Stemmed token mapping matrix.

    Returns:
        str: Instructions formatted for the parser.
    """
    # 1. REPLACE WITH BASE ENGLISH/FRENCH TERMS
    result = Conform(string, lexique)
    # 2. REPLACE WITH CORE ENGINE TOKENS
    result = Conform(result, racine)
    return result

def Conform(string, lexique):
    """    
    Parses a string to replace specific expressions with desired tokens.
    Args:
        string (_type_): _description_
        lexique (_type_): _description_
    Returns:
        _type_: _description_
    """
    result = ""
    c = string.split(" ")
    p = len(c)
    offset = 0
    while(p > 0):
        # Maximum words to check (sliding window)
        MAX = 8
        if((len(c)-offset) < 8):
            MAX = len(c) - offset

        wRange = MAX
        if wRange > 0:
            while wRange > 0:
                test = ""
                for i in range(wRange):
                    if len(test) == 0:
                        test = c[-1-i-offset] 
                    else:
                        test = c[-1-i-offset] + " " + test     
                for line in lexique:
                    if test.upper() in line:
                        p -= wRange
                        offset += wRange
                        result = line[0] + " " + result
                        wRange = 0
                if wRange == 1:
                    p -= 1
                    offset += 1
                    result = test + " " + result
                    wRange = 0
                else:
                    wRange -= 1
        else:
            result = c[-1-offset] + " " + result
            p -= 1
            offset += 1
    return noAccent(result[:-1])

def noAccent(string):
    """
    Removes accents and handles illegal characters for the parser.
    """
    raw = re.sub(u"[àáâãäå]", 'a', string)
    raw = re.sub(u"[èéêë]", 'e', raw)
    raw = re.sub(u"[ìíîï]", 'i', raw)
    raw = re.sub(u"[òóôõö]", 'o', raw)
    raw = re.sub(u"[ùúûü]", 'u', raw)
    # on retire illegal char    
    raw = re.sub(u"^'", "", raw)
    # Replace single quotes to avoid DSL syntax breakage
    raw.replace("'",'’')
    # Security: Ensure balanced double quotes to prevent parser crashes
    if raw.count('"') % 2 != 0:
        raw = (' ').join(raw.rspplit('"', 1))
    return raw
        

"""
Debug Test Section
"""
if __name__ == '__main__':
    lexer = DLexer()
    while True:
        try:
            text = input('PProcessor Debug > ')
        except EOFError:
            break
        if text:
            processed = PProcessor(text, EN_Matrice, FR_Racinisation)
            print(f"Processed: {processed}")
            try:
                tokens = lexer.tokenize(processed)
                for token in tokens:
                    print(token)
            except Exception as e:
                print(f"Lexer Error: {e}")
