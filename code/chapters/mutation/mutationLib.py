# print('Mutation Lib')
from fuzzingbook.MutationFuzzer import *
from .httpProgram import http_program

# # Run MutationFuzzer class
# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# for i in range(10):
#     print(mutation_fuzzer.fuzz())


# # Run MutationCoverageFuzzer class
seed_input = "http://www.google.com/search?q=fuzzing"
mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])

http_runner = FunctionCoverageRunner(http_program)

mutation_fuzzer.runs(http_runner, trials=10000)
print(mutation_fuzzer.population[:5])
