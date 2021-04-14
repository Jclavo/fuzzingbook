# print('Mutation Advance')
from core.mutationFuzzer import MutationFuzzer
from core.functionRunner import FunctionRunner
from core.functionCoverageRunner import FunctionCoverageRunner
from core.mutationCoverageFuzzer import MutationCoverageFuzzer

from .httpProgram import http_program

# # Running MutationFuzzer class using fuzz method
# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# print(mutation_fuzzer.fuzz())
# print(mutation_fuzzer.fuzz())
# print(mutation_fuzzer.fuzz())

# #  Running FunctionRunner class
# http_runner = FunctionRunner(http_program)
# print(http_runner.run("https://foo.bar/"))
# print(http_runner.run("foo.bar/"))

# #  Running FunctionCoverageRunner class
# http_runner = FunctionCoverageRunner(http_program)
# print(http_runner.run_function("https://foo.bar/"))
# print(list(http_runner.coverage())[:5])


# #  Running MutationCoverageFuzzer class
seed_input = "http://www.google.com/search?q=fuzzing"
mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])

http_runner = FunctionCoverageRunner(http_program)

mutation_fuzzer.runs(http_runner, trials=10000)
# # valid input that were generated
# print(mutation_fuzzer.population)
print(len(mutation_fuzzer.population))
for result in mutation_fuzzer.population:
    print(result)
# print(len(mutation_fuzzer.coverages_seen))
# for coverage_seen in mutation_fuzzer.coverages_seen:
#     print(coverage_seen)