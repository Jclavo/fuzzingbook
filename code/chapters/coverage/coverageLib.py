from fuzzingbook.Coverage import *

# Running coverage class
with Coverage() as cov:
    cgi_decode("a+b")

# The trace() method returns the coverage as a list of locations covered. Each location comes as a pair (function name, line).
# print(cov.trace())

# The coverage() method returns the set of locations executed at least once:
print(cov.coverage())