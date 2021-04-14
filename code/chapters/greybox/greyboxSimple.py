# print('Greybox Simple')

from core.mutate import mutate
from core.mutator import Mutator
from core.seed import Seed
from core.powerSchedule import PowerSchedule
from core.functionCoverageRunner import FunctionCoverageRunner
from core.mutationFuzzerPlus import MutationFuzzerPlus
from core.population_coverage import population_coverage
from core.greyboxFuzzer import GreyboxFuzzer
from core.randomFuzzer import RandomFuzzer
from core.mutationCoverageFuzzer import MutationCoverageFuzzer
from .crashme import crashme

# print(mutate("good"))
# print(Mutator().mutate("micho"))

# # Testing power schedule
# population = [Seed("A"), Seed("B"), Seed("C")]
# schedule = PowerSchedule()
# hits = {
#     "A" : 0,
#     "B" : 0,
#     "C" : 0
# }

# for i in range(10000):
#     seed = schedule.choose(population)
#     hits[seed.data] += 1

# print(hits)

# # Coverage statements

# crashme_runner = FunctionCoverageRunner(crashme)
# crashme_runner.run("good")
# print(list(crashme_runner.coverage()))

# # Test Mutation Fuzzer Plus class
# seed_input = ["good"]
# seed_input = ["good","look"]
# mutation_fuzzer = MutationFuzzerPlus(seed_input, Mutator(), PowerSchedule())
# print(mutation_fuzzer.fuzz())
# print(mutation_fuzzer.fuzz())
# print(mutation_fuzzer.fuzz())

# # BLACKBOX MUTATION-BASED FUZZER
import time
n = 30000

seed_input = ["good"]
blackbox_fuzzer = MutationFuzzerPlus(seed_input, Mutator(), PowerSchedule())

start = time.time()
blackbox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
end = time.time()

print("It took the blackbox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n))

blackbox_cumulative, blackbox_coverage = population_coverage(blackbox_fuzzer.inputs, crashme)
bb_max_coverage = max(blackbox_coverage)

print("The blackbox mutation-based fuzzer achieved a maximum coverage of %d statements." % bb_max_coverage)

# # run greybox mutation-based fuzzer
# import time
# n = 30000
# seed_input = ["good"]
# greybox_fuzzer = GreyboxFuzzer(seed_input, Mutator(), PowerSchedule())

# start = time.time()
# greybox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
# end = time.time()

# print("It took the greybox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n))

# _, greybox_coverage = population_coverage(greybox_fuzzer.inputs, crashme)
# gb_max_coverage = max(greybox_coverage)

# # "Our greybox mutation-based fuzzer covers %d more statements" % (gb_max_coverage - bb_max_coverage)
# print("Our greybox mutation-based fuzzer covers %d more statements" % gb_max_coverage)
# print(greybox_fuzzer.population)

# # BLACKBOX GENERATION-BASED FUZZER
# import time
# n = 30000
# blackbox_gen_fuzzer = RandomFuzzer(min_length=4, max_length=4, char_start=32, char_range=96)

# start = time.time()
# blackbox_gen_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
# end = time.time()

# print("It took the blackbox generation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n))
