from fuzzingbook.Fuzzer import *

#Using Fuzzer class
# random_fuzzer = RandomFuzzer()
# print(random_fuzzer.fuzz())

##Using Fuzzer class with constructor parameter
# random_fuzzer = RandomFuzzer(min_length=10, max_length=20, char_start=65, char_range=26)
# print(random_fuzzer.fuzz())

##Using PrintRunner class
# random_fuzzer = RandomFuzzer()
# print_runner = PrintRunner()
# print(random_fuzzer.run(print_runner))

##Using ProgramRunner class
cat = ProgramRunner('cat')
random_fuzzer = RandomFuzzer()
print(random_fuzzer.run(cat))