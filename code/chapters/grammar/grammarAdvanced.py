# print('Grammar Advanced')

from core.grammars import *
from core.simpleGrammarFuzzer import simple_grammar_fuzzer
from core.convertOperatorsEBNF import convert_ebnf_grammar
from core.mutationFuzzer import MutationFuzzer

# # use simple_grammar_fuzzer
for i in range(10):
    print(simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=5))


# # Using Mutation
# number_of_seeds = 10
# seeds = [
#     simple_grammar_fuzzer(
#         grammar=URL_GRAMMAR,
#         max_nonterminals=10) for i in range(number_of_seeds)]
# # print(seeds)

# mutation_fuzzer = MutationFuzzer(seeds)

# for i in range(20):
#    print(mutation_fuzzer.fuzz())


# # convert EBNF to BNF
# print(convert_ebnf_grammar({"<authority>": ["(<userinfo>@)?<host>(:<port>)?"]}))
# EXPR_BNF_GRAMMAR = convert_ebnf_grammar(EXPR_EBNF_GRAMMAR)

# for expr in EXPR_BNF_GRAMMAR:
#     print(expr , ':' , EXPR_BNF_GRAMMAR[expr])
