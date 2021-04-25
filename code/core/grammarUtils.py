import copy
import re

# function to extend grammar 
def extend_grammar(grammar, extension={}):
    new_grammar = copy.deepcopy(grammar)
    new_grammar.update(extension)
    return new_grammar

# function to construct a list with all characters in the string
def srange(characters):
    """Construct a list with all characters in the string"""
    return [c for c in characters]

# # function to eturns a list of all characters in the ASCII range of start to (including) end
def crange(character_start, character_end):
    return [chr(i)
            for i in range(ord(character_start), ord(character_end) + 1)]


# # some definitions
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

# # get nonterminals from string or tuple
def nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_NONTERMINAL, expansion)

# check if the symbols is nonterminal
def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)


# # Expanding Operators
RE_EXTENDED_NONTERMINAL = re.compile(r'(<[^<> ]*>[?+*])')

# # function to get nonterminals with operators
def extended_nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_EXTENDED_NONTERMINAL, expansion)

# # Expanding Parenthesized Expressions
RE_PARENTHESIZED_EXPR = re.compile(r'\([^()]*\)[?+*]')

def parenthesized_expressions(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_PARENTHESIZED_EXPR, expansion)

# # creating new symbols
def new_symbol(grammar, symbol_name="<symbol>"):
    """Return a new symbol for `grammar` based on `symbol_name`"""
    if symbol_name not in grammar:
        return symbol_name

    count = 1
    while True:
        tentative_symbol_name = symbol_name[:-1] + "-" + repr(count) + ">"
        if tentative_symbol_name not in grammar:
            return tentative_symbol_name
        count += 1
