from random import randint
from templates import binop_only_meths, inverse_req_meths

rand_int_list = """
def gl(length, start=0, end=1_000_000):
    # Use random numbers from 0, 1_000_000.
    return [randint(start, end) for _ in range(length)]
"""
int_sub = """
ibf = int.__sub__
"""
int_add = """
bf = int.__add__
"""

rand_set_list = """
def gl(length, start=0, end=1_000_000):
    return [{randint(start, end)} for _ in range(length)]
"""
set_union = """
bf = set.union
"""

imports = """
import pytest
from random import randint, shuffle
from test_support import bit_dummy, intensities, timeouts
from bit import BIT
""".strip()
ts_fmt_bf = "from test_support import {0} as bf"
ts_fmt_ibf = "from test_support import {0} as ibf"
ts_fmt_gl = "from test_support import {0} as gl"

test_files = {
    'binop': [
        {
            'name': 'tests/test_set_union.py',
            'binop': ts_fmt_bf.format('set_union'),
            'gen_list': ts_fmt_gl.format('rand_set_list'),
            'intensity': 'quick',
        }
    ],
    'inverse': [
        {
            'name': 'tests/test_num_add_sub.py',
            'binop': ts_fmt_bf.format('int_add'),
            'inverse': ts_fmt_ibf.format('int_sub'),
            'gen_list': ts_fmt_gl.format('rand_int_list'),
            'intensity': 'quick',
        }
    ]
}


def generate_tests(test_files):
    for case in test_files:
        for test in test_files[case]:
            name = test.pop('name')
            with open(name, 'w') as f:
                f.write(imports)
                f.write(binop_only_meths.format(**test))
                if case == 'inverse':
                    f.write(inverse_req_meths.format(**test))


if __name__ == "__main__":
    generate_tests(test_files)
