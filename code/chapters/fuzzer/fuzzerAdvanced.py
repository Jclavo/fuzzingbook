from core.runner import Runner
from core.printRunner import PrintRunner
from core.programRunner import ProgramRunner
from core.randomFuzzer import RandomFuzzer

# # Running PrintRunner class
# p = PrintRunner()
# (result, outcome) = p.run("Some input")

# print(outcome)


# #Running ProgramRunner class
cat = ProgramRunner(program="cat")
result = cat.run("hello")
print(result)


# #Running Fuzzer class
# random_fuzzer = RandomFuzzer(min_length=20, max_length=20)
# for i in range(10):
#     print(random_fuzzer.fuzz())


# # Running Fuzzer && ProgramRunner class

random_fuzzer = RandomFuzzer(min_length=20, max_length=20)
cat = ProgramRunner(program="cat")

# # Using boths
for i in range(10):
    inp = random_fuzzer.fuzz()
    result, outcome = cat.run(inp)
    assert result.stdout == inp
    assert outcome == Runner.PASS

# # Using only RandomFuzzer class, its method run
# for i in range(10):
#     result, outcome = random_fuzzer.run(cat)
#     # print(result.stdout)
#     assert outcome == Runner.PASS

# # Using only RandomFuzzer class, its method run
results = random_fuzzer.runs(cat, 10)

for result in results:
    print(result)
#     # if  result.stderr == "":
#     #     print(result)
#     # if  result.stderr != "":
#     #     print(result)