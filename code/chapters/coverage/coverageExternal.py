# print("Coverage external")

import tempfile
import os

## Set program in C

cgi_c_code = """
/* CGI decoding as C program */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int hex_values[256];

void init_hex_values() {
    for (int i = 0; i < sizeof(hex_values) / sizeof(int); i++) {
        hex_values[i] = -1;
    }
    hex_values['0'] = 0; hex_values['1'] = 1; hex_values['2'] = 2; hex_values['3'] = 3;
    hex_values['4'] = 4; hex_values['5'] = 5; hex_values['6'] = 6; hex_values['7'] = 7;
    hex_values['8'] = 8; hex_values['9'] = 9;

    hex_values['a'] = 10; hex_values['b'] = 11; hex_values['c'] = 12; hex_values['d'] = 13;
    hex_values['e'] = 14; hex_values['f'] = 15;

    hex_values['A'] = 10; hex_values['B'] = 11; hex_values['C'] = 12; hex_values['D'] = 13;
    hex_values['E'] = 14; hex_values['F'] = 15;
}

int cgi_decode(char *s, char *t) {
    while (*s != '\\0') {
        if (*s == '+')
            *t++ = ' ';
        else if (*s == '%') {
            int digit_high = *++s;
            int digit_low = *++s;
            if (hex_values[digit_high] >= 0 && hex_values[digit_low] >= 0) {
                *t++ = hex_values[digit_high] * 16 + hex_values[digit_low];
            }
            else
                return -1;
        }
        else
            *t++ = *s;
        s++;
    }
    *t = '\\0';
    return 0;
}

int main(int argc, char *argv[]) {
    init_hex_values();

    if (argc >= 2) {
        char *s = argv[1];
        char *t = malloc(strlen(s) + 1); /* output is at most as long as input */
        int ret = cgi_decode(s, t);
        printf("%s\\n", t);
        return ret;
    }
    else
    {
        printf("cgi_decode: usage: cgi_decode STRING\\n");
        return 1;
    }
}
"""

# print(cgi_c_code)

filename = "cgi_decode"
c_filename = filename + ".c"
dirname =  "c_files"

currentdir = os.path.dirname(os.path.realpath(__file__))
dirpath = os.path.join(currentdir, dirname) 

FILE = os.path.join(dirpath , c_filename)

with open(FILE, "w") as f:
    f.write(cgi_c_code)

# print(currentdir)

# # Compile C into an executable
# # !cc --coverage -o cgi_decode cgi_decode.c
os.system(f'cd {dirpath}; cc --coverage -o {filename} {c_filename}')

# Run C program 
# # !./cgi_decode 'Send+mail+to+me%40fuzzingbook.org'
os.system(f'cd {dirpath}; ./{filename} {"Send+mail+to+me%40fuzzingbook.org"}')

## Collect coverage information
# # !gcov cgi_decode.c
os.system(f'cd {dirpath}; gcov {c_filename}')

## Open coverage file
# In the .gcov file, each line is prefixed with the number of times it was called 
# (- stands for a non-executable line,
# ##### stands for zero) as well as the line number.

# lines = open(FILE + '.gcov').readlines()
# print(lines)
# for i in range(30, 50):
#     print(lines[i], end='')


def read_gcov_coverage(c_file):
    gcov_file = c_file + ".gcov"
    coverage = set()
    with open(gcov_file) as file:
        for line in file.readlines():
            elems = line.split(':')
            covered = elems[0].strip()
            line_number = int(elems[1].strip())
            if covered.startswith('-') or covered.startswith('#'):
                continue
            coverage.add((os.path.basename(c_file), line_number))
    return coverage


coverage = read_gcov_coverage(FILE)
print(list(coverage))


