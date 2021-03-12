import random

import os
import tempfile

import subprocess

# # Fuzzer class
def fuzzer(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

# print(fuzzer()) #simple fuzzer
# print(fuzzer(1000, ord('a'), 26))# fuzzer with parameters


# #Creating a temporal file
basename = "input.txt"
tempdir = tempfile.mkdtemp()
FILE = os.path.join(tempdir, basename)
# # print(FILE) #show file path

# # Writing fuzz data in the file
data = fuzzer()
with open(FILE, "w") as f:
    f.write(data)

# # Checking if the data was written correctly
contents = open(FILE).read()
print(contents)
# assert(contents == data)

# # delete the temp files
# # os.remove(FILE)
# # os.removedirs(tempdir)

# # Invoking external program
# program = "bc"
# with open(FILE, "w") as f:
#     f.write("2 + 2\n")
# result = subprocess.run([program, FILE],
#                         stdin=subprocess.DEVNULL,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE,
#                         universal_newlines=True)  # Will be "text" in Python 3.7

# print(result)
# print(result.stdout)
# print(result.returncode) # 0 = ok
# print(result.stderr)


#Long-Running Fuzzing
trials = 100
program = "bc"

runs = []

for i in range(trials):
    data = fuzzer()
    with open(FILE, "w") as f:
        f.write(data)
    result = subprocess.run([program, FILE],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    runs.append((data, result))

# for (data, result) in runs:
#     print(result)
#     # if  result.stderr == "":
#     #     print(result)
#     if  result.stderr != "":
#         print(result)

# print(sum(1 for (data, result) in runs if result.stderr == ""))

# errors = [(data, result) for (data, result) in runs if result.stderr != ""]
# (first_data, first_result) = errors[0]

# print(repr(first_data))
# print(first_result.stderr)
