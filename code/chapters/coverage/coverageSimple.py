import sys
import inspect

from fuzzingbook.Coverage import print_content, print_file
# import fuzzingbook_utils

from .cgiDecode import cgi_decode


# Testing function cgi_decode
# print(cgi_decode("Hello+world"))

# # Testing function cgi_decode using blackbox

# assert cgi_decode('+') == ' '
# assert cgi_decode('%20') == ' '
# assert cgi_decode('abc') == 'abc'

# try:
#     cgi_decode('%?a')
#     assert False
# except ValueError:
#     pass

# # Tracing executions
# print(cgi_decode("a+b"))

coverage = []

def traceit(frame, event, arg):
    if event == "line":
        global coverage
        function_name = frame.f_code.co_name
        lineno = frame.f_lineno
        coverage.append(lineno)
    return traceit

def cgi_decode_traced(s):
    global coverage
    coverage = []
    sys.settrace(traceit)  # Turn on
    cgi_decode(s)
    sys.settrace(None)    # Turn off

# cgi_decode_traced("a+b")
# print(coverage)

# # Getting source code
cgi_decode_code = inspect.getsource(cgi_decode)
# print_content(cgi_decode_code[:300] + "...", ".py")
cgi_decode_lines = [""] + cgi_decode_code.splitlines()
# print(cgi_decode_lines[9:13])
# print(cgi_decode_lines[9])

cgi_decode_traced("a+b")
covered_lines = set(coverage)
# print(covered_lines)

for lineno in range(1, len(cgi_decode_lines)):
    if lineno not in covered_lines:
        print("# ", end="")
    else:
        print("  ", end="")
    print("%2d  " % lineno, end="")
    print_content(cgi_decode_lines[lineno], '.py')
    print("")