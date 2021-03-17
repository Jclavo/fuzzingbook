# print('Mutation Simple')


from urllib.parse import urlparse

from fuzzingbook.Fuzzer import *
from fuzzingbook.Coverage import *
from fuzzingbook.Timer import Timer

# Parse URl
# print(urlparse("http://www.google.com/search?q=fuzzing"))

# function to validate url
def http_program(url):
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")

    # Do something with the URL
    return True

# print(http_program("http://www.google.com/search?q=fuzzing"))
# print(http_program("www.google.com/search?q=fuzzing"))

# Use fuzzing
# print(fuzzer(char_start=32, char_range=96))
# for i in range(1000):
#     try:
#         url = fuzzer()
#         result = http_program(url)
#         print("Success!")
#     except ValueError:
#         pass

# Check how long time takes running
# trials = 1000
# with Timer() as t:
#     for i in range(trials):
#         try:
#             url = fuzzer()
#             result = http_program(url)
#             print("Success!")
#         except ValueError:
#             pass

# duration_per_run_in_seconds = t.elapsed_time() / trials
# print(duration_per_run_in_seconds)

# # Mutation inputs
# # function delete_random_character
def delete_random_character(s):
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]

# seed_input = "A quick brown fox"
# for i in range(10):
#     x = delete_random_character(seed_input)
#     print(repr(x))


# # function insert_random_character
def insert_random_character(s):
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

# seed_input = "A quick brown fox"
# for i in range(10):
#     print(repr(insert_random_character(seed_input)))

# # function flip_random_character

def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]

# seed_input = "A quick brown fox"
# for i in range(10):
#     print(repr(flip_random_character(seed_input)))

# # Random mutator that works with above functions
def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)

# for i in range(10):
#     print(repr(mutate("A quick brown fox")))

# # Mutation URL's

## Check is url is correct or not
def is_valid_url(url):
    try:
        result = http_program(url)
        return True
    except ValueError:
        return False

# print(is_valid_url("http://www.google.com/search?q=fuzzing"))
# print(is_valid_url("xyzzy"))

# # using mutation to test is_valid_url functions
# seed_input = "http://www.google.com/search?q=fuzzing"
# valid_inputs = set()
# trials = 20

# for i in range(trials):
#     inp = mutate(seed_input)
#     if is_valid_url(inp):
#         valid_inputs.add(inp)

# print(len(valid_inputs))

# # find how log time is taken when http is mutated to https

# seed_input = "http://www.google.com/search?q=fuzzing"
# trials = 0
# with Timer() as t:
#     while True:
#         trials += 1
#         inp = mutate(seed_input)
#         if inp.startswith("https://"):
#             print(
#                 "Success after",
#                 trials,
#                 "trials in",
#                 t.elapsed_time(),
#                 "seconds")
#             break

# # Multiples mutations
# seed_input = "http://www.google.com/search?q=fuzzing"
# mutations = 50
# inp = seed_input
# for i in range(mutations):
#     if i % 5 == 0:
#         print(i, "mutations:", repr(inp))
#     inp = mutate(inp)

# # implement MutationFuzzer class

class MutationFuzzer(Fuzzer):
    def __init__(self, seed, min_mutations=2, max_mutations=10):
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self):
        self.population = self.seed
        self.seed_index = 0

class MutationFuzzer(MutationFuzzer):
    def mutate(self, inp):
        return mutate(inp)

class MutationFuzzer(MutationFuzzer):
    def create_candidate(self):
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

class MutationFuzzer(MutationFuzzer):
    def fuzz(self):
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()
        return self.inp

# # Running class using fuzz method
# seed_input = "http://www.google.com/search?q=fuzzing"
# mutation_fuzzer = MutationFuzzer(seed=[seed_input])
# print(mutation_fuzzer.fuzz())
# print(mutation_fuzzer.fuzz())
# print(mutation_fuzzer.fuzz())

# # GUIDING BY COVERAGE

# # implement FunctionRunner class

class FunctionRunner(Runner):
    def __init__(self, function):
        """Initialize.  `function` is a function to be executed"""
        self.function = function

    def run_function(self, inp):
        return self.function(inp)

    def run(self, inp):
        try:
            result = self.run_function(inp)
            outcome = self.PASS
        except Exception:
            result = None
            outcome = self.FAIL

        return result, outcome

# http_runner = FunctionRunner(http_program)
# print(http_runner.run("https://foo.bar/"))

# Extend FunctionRunner class
class FunctionCoverageRunner(FunctionRunner):
    def run_function(self, inp):
        with Coverage() as cov:
            try:
                result = super().run_function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        return result

    def coverage(self):
        return self._coverage

# http_runner = FunctionCoverageRunner(http_program)
# print(http_runner.run_function("https://foo.bar/"))
# print(list(http_runner.coverage())[:5])

# Implement MutationCoverageFuzzer class
class MutationCoverageFuzzer(MutationFuzzer):
    def reset(self):
        super().reset()
        self.coverages_seen = set()
        # Now empty; we fill this with seed in the first fuzz runs
        self.population = []

    def run(self, runner):
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = super().run(runner)
        new_coverage = frozenset(runner.coverage())
        if outcome == Runner.PASS and new_coverage not in self.coverages_seen:
            # We have new coverage
            self.population.append(self.inp)
            self.coverages_seen.add(new_coverage)

        return result

seed_input = "http://www.google.com/search?q=fuzzing"
mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])

http_runner = FunctionCoverageRunner(http_program)

mutation_fuzzer.runs(http_runner, trials=10000)
# # valid input that were generated
# print(mutation_fuzzer.population)