# print('Grammar Simple')
import re
import random


# # sample digit grammar
DIGIT_GRAMMAR = {
    "<start>": 
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

# # sample aritmetic expression grammar

EXPR_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["<factor>",
        #  "-<factor>",
         "(<expr>)",
         "<integer>.<integer>",
         "<integer>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

# # access symbol
# print(EXPR_GRAMMAR["<digit>"])

# # check if symbol is in grammar
# print("<identifier>" in EXPR_GRAMMAR)

# # some definitions

START_SYMBOL = "<start>"
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

# # get nonterminals from string or tuple
def nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_NONTERMINAL, expansion)

# print(nonterminals("<term> * <factor>"))
# print(nonterminals("1 < 3 > 2"))
# print(nonterminals("1 <3> 2"))
# print(nonterminals(("<1>", {'option': 'value'}))) #tuple

# check if the symbols is nonterminal
def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)

# assert is_nonterminal("<abc>")
# assert is_nonterminal("<symbol-1>")
# assert not is_nonterminal("+")

# # create simple_grammar_fuzzer

class ExpansionError(Exception):
    pass

def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL,
                          max_nonterminals=10, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(nonterminals(new_term)) < max_nonterminals:
            term = new_term
            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError("Cannot expand " + repr(term))

    return term

# simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=3, log=True)

# for i in range(10):
#     print(simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=5))

# # sample CGI grammar
CGI_GRAMMAR = {
    "<start>":
        ["<string>"],

    "<string>":
        ["<letter>", "<letter><string>"],

    "<letter>":
        ["<plus>", "<percent>", "<other>"],

    "<plus>":
        ["+"],

    "<percent>":
        ["%<hexdigit><hexdigit>"],

    "<hexdigit>":
        ["0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "a", "b", "c", "d", "e", "f"],

    "<other>":  # Actually, could be _all_ letters
        ["0", "1", "2", "3", "4", "5", "a", "b", "c", "d", "e", "-", "_"],
}

# for i in range(10):
#     print(simple_grammar_fuzzer(grammar=CGI_GRAMMAR, max_nonterminals=10))

# # sample URL grammar
URL_GRAMMAR = {
    "<start>":
        ["<url>"],
    "<url>":
        ["<scheme>://<authority><path><query>"],
    "<scheme>":
        ["http", "https", "ftp", "ftps"],
    "<authority>":
        ["<host>", "<host>:<port>", "<userinfo>@<host>", "<userinfo>@<host>:<port>"],
    "<host>":  # Just a few
        ["cispa.saarland", "www.google.com", "fuzzingbook.com"],
    "<port>":
        ["80", "8080", "<nat>"],
    "<nat>":
        ["<digit>", "<digit><digit>"],
    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<userinfo>":  # Just one
        ["user:password"],
    "<path>":  # Just a few
        ["", "/", "/<id>"],
    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],
    "<query>":
        ["", "?<params>"],
    "<params>":
        ["<param>", "<param>&<params>"],
    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<nat>"],
}

# for i in range(10):
#     print(simple_grammar_fuzzer(grammar=URL_GRAMMAR, max_nonterminals=10))


# # sample natural grammar
TITLE_GRAMMAR = {
    "<start>": ["<title>"],
    "<title>": ["<topic>: <subtopic>"],
    "<topic>": ["Generating Software Tests", "<fuzzing-prefix>Fuzzing", "The Fuzzing Book"],
    "<fuzzing-prefix>": ["", "The Art of ", "The Joy of "],
    "<subtopic>": ["<subtopic-main>",
                   "<subtopic-prefix><subtopic-main>",
                   "<subtopic-main><subtopic-suffix>"],
    "<subtopic-main>": ["Breaking Software",
                        "Generating Software Tests",
                        "Principles, Techniques and Tools"],
    "<subtopic-prefix>": ["", "Tools and Techniques for "],
    "<subtopic-suffix>": [" for <reader-property> and <reader-property>",
                          " for <software-property> and <software-property>"],
    "<reader-property>": ["Fun", "Profit"],
    "<software-property>": ["Robustness", "Reliability", "Security"],
}

# for i in range(10):
#     print(simple_grammar_fuzzer(grammar=TITLE_GRAMMAR, max_nonterminals=10))


# # Using Mutation
# from core.mutationFuzzer import MutationFuzzer

# number_of_seeds = 10
# seeds = [
#     simple_grammar_fuzzer(
#         grammar=URL_GRAMMAR,
#         max_nonterminals=10) for i in range(number_of_seeds)]
# # print(seeds)

# mutation_fuzzer = MutationFuzzer(seeds)

# for i in range(20):
#    print(mutation_fuzzer.fuzz())


# # A grammar toolboxk

# # using > and < symbols

simple_nonterminal_grammar = {
    "<start>": ["<nonterminal>"],
    "<nonterminal>": ["<left-angle><identifier><right-angle>"],
    "<left-angle>": ["<"],
    "<right-angle>": [">"],
    "<identifier>": ["id"]  # for now
}

# # extending grammars
import copy

# nonterminal_grammar = copy.deepcopy(simple_nonterminal_grammar)
# nonterminal_grammar["<identifier>"] = ["<idchar>", "<identifier><idchar>"]
# nonterminal_grammar["<idchar>"] = ['a', 'b', 'c', 'd']  # for now

# print(nonterminal_grammar)

# # function to extend grammar 

def extend_grammar(grammar, extension={}):
    new_grammar = copy.deepcopy(grammar)
    new_grammar.update(extension)
    return new_grammar

nonterminal_grammar = extend_grammar(simple_nonterminal_grammar,
                                     {
                                         "<identifier>": ["<idchar>", "<identifier><idchar>"],
                                         # for now
                                         "<idchar>": ['a', 'b', 'c', 'd']
                                     }
                                     )

# print(nonterminal_grammar)

# # character class
import string

# function to construct a list with all characters in the string
def srange(characters):
    """Construct a list with all characters in the string"""
    return [c for c in characters]

# print(srange(string.ascii_letters))

nonterminal_grammar = extend_grammar(nonterminal_grammar,
                                     {
                                         "<idchar>": srange(string.ascii_letters) + srange(string.digits) + srange("-_")
                                     }
                                     )

# for i in range(10):
#     print(simple_grammar_fuzzer(nonterminal_grammar, "<identifier>") )

# # function to eturns a list of all characters in the ASCII range of start to (including) end
def crange(character_start, character_end):
    return [chr(i)
            for i in range(ord(character_start), ord(character_end) + 1)]

# print(crange('0', '9'))
# print(crange('a', 'z'))

# # grammar shortcuts

nonterminal_ebnf_grammar = extend_grammar(nonterminal_grammar,
                                          {
                                              "<identifier>": ["<idchar>+"]
                                          }
                                          )

# print(nonterminal_ebnf_grammar)

# # sample aritmetic expression in EBNF grammar

EXPR_EBNF_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["<sign>?<factor>", "(<expr>)", "<integer>(.<integer>)?"],

    "<sign>":
        ["+", "-"],

    "<integer>":
        ["<digit>+"],

    "<digit>":
        srange(string.digits)
}


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

# print(new_symbol(EXPR_EBNF_GRAMMAR, '<expr>'))

# # Expanding Parenthesized Expressions

RE_PARENTHESIZED_EXPR = re.compile(r'\([^()]*\)[?+*]')

def parenthesized_expressions(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_PARENTHESIZED_EXPR, expansion)

# print(parenthesized_expressions("(<foo>)* (<foo><bar>)+ (+<foo>)? <integer>(.<integer>)?"))
# print(parenthesized_expressions("((<foo>)?)+"))

# # function to convert_ebnf_parentheses

def convert_ebnf_parentheses(ebnf_grammar):
    """Convert a grammar in extended BNF to BNF"""
    grammar = extend_grammar(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]

            while True:
                parenthesized_exprs = parenthesized_expressions(expansion)
                if len(parenthesized_exprs) == 0:
                    break

                for expr in parenthesized_exprs:
                    operator = expr[-1:]
                    contents = expr[1:-2]

                    new_sym = new_symbol(grammar)
                    expansion = grammar[nonterminal][i].replace(
                        expr, new_sym + operator, 1)
                    grammar[nonterminal][i] = expansion
                    grammar[new_sym] = [contents]

    return grammar

# print(convert_ebnf_parentheses({"<number>": ["<integer>(.<integer>)?"]}))
# print(convert_ebnf_parentheses({"<foo>": ["((<foo>)?)+"]}))

# # Expanding Operators

RE_EXTENDED_NONTERMINAL = re.compile(r'(<[^<> ]*>[?+*])')

# # function to get nonterminals with operators
def extended_nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_EXTENDED_NONTERMINAL, expansion)

# print(extended_nonterminals("<foo>* <bar>+ <elem>? <none>"))

# # function to convert_ebnf_operators
def convert_ebnf_operators(ebnf_grammar):
    """Convert a grammar in extended BNF to BNF"""
    grammar = extend_grammar(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]
            extended_symbols = extended_nonterminals(expansion)

            for extended_symbol in extended_symbols:
                operator = extended_symbol[-1:]
                original_symbol = extended_symbol[:-1]

                new_sym = new_symbol(grammar, original_symbol)
                grammar[nonterminal][i] = grammar[nonterminal][i].replace(
                    extended_symbol, new_sym, 1)

                if operator == '?':
                    grammar[new_sym] = ["", original_symbol]
                elif operator == '*':
                    grammar[new_sym] = ["", original_symbol + new_sym]
                elif operator == '+':
                    grammar[new_sym] = [
                        original_symbol, original_symbol + new_sym]

    return grammar

# print(convert_ebnf_operators({"<integer>": ["<digit>+"]}))

# # All together

def convert_ebnf_grammar(ebnf_grammar):
    return convert_ebnf_operators(convert_ebnf_parentheses(ebnf_grammar))

# print(convert_ebnf_grammar({"<authority>": ["(<userinfo>@)?<host>(:<port>)?"]}))
# print(convert_ebnf_grammar(EXPR_EBNF_GRAMMAR))

# # GRAMMAR EXTENSIONS

def opts(**kwargs):
    return kwargs

# print(opts(min_depth=10))

def exp_string(expansion):
    """Return the string to be expanded"""
    if isinstance(expansion, str):
        return expansion
    return expansion[0]

# print(exp_string(("<term> + <expr>", opts(min_depth=10))))


def exp_opts(expansion):
    """Return the options of an expansion.  If options are not defined, return {}"""
    if isinstance(expansion, str):
        return {}
    return expansion[1]

def exp_opt(expansion, attribute):
    """Return the given attribution of an expansion.
    If attribute is not defined, return None"""
    return exp_opts(expansion).get(attribute, None)

# print(exp_opts(("<term> + <expr>", opts(min_depth=10))))
# print(exp_opt(("<term> - <expr>", opts(max_depth=2)), 'max_depth'))