# print("coverage advanced")

# import matplotlib.pyplot as plt
from fuzzingbook.Coverage import *

from .coverage import Coverage
from .cgiDecode import cgi_decode

from core.randomFuzzer import RandomFuzzer

# # Coverage class

with Coverage() as cov:
    cgi_decode("a+b")

# print(cov.trace())
# print(cov.coverage())

# # Comparig coverage
with Coverage() as cov_plus:
    cgi_decode("a+b")
with Coverage() as cov_standard:
    cgi_decode("abc")

# print(cov_plus.coverage() - cov_standard.coverage())

# # Maximum coverage
with Coverage() as cov_max:
    cgi_decode('+')
    cgi_decode('%20')
    cgi_decode('abc')
    try:
        cgi_decode('%?a')
    except:
        pass

# print(cov_max.coverage() - cov_plus.coverage())

# # Coverage basic fuzzing

random_fuzzer = RandomFuzzer()

sample = random_fuzzer.fuzz()

# print(sample)

with Coverage() as cov_fuzz:
    try:
        cgi_decode(sample)
    except:
        pass

# print(cov_fuzz.coverage())
# print(cov_max.coverage() - cov_fuzz.coverage())

# # Coverage basic fuzzing with trial = 100

trials = 100

random_fuzzer = RandomFuzzer()

def population_coverage(population, function):
    cumulative_coverage = []
    all_coverage = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except:
                pass
        all_coverage |= cov.coverage()
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage

def hundred_inputs():
    population = []
    for i in range(trials):
        population.append(random_fuzzer.fuzz())
    return population

all_coverage, cumulative_coverage = population_coverage(hundred_inputs(), cgi_decode)

# print(all_coverage)
# print(cumulative_coverage)

# # Plot the coverage

# # plt.plot(cumulative_coverage)
# # plt.title('Coverage of cgi_decode() with random inputs')
# # plt.xlabel('# of inputs')
# # plt.ylabel('lines covered')


## Using basic fuzzing

# random_fuzzer = RandomFuzzer()
# with ExpectError():
#     for i in range(trials):
#         try:
#             s = random_fuzzer.fuzz()
#             cgi_decode(s)
#         except ValueError:
#             pass