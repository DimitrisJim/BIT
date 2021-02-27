from os import environ
from random import randint
from templates import binop_only_meths, inverse_req_meths

imports = """
import pytest
from random import randint, shuffle
from support import bit_dummy, intensities, timeouts
from bit import BIT
""".strip()
ts_fmt_bf = "from support import {0} as bf"
ts_fmt_ibf = "from support import {0} as ibf"
ts_fmt_gl = "from support import {0} as gl"

test_files = [
    # Sets: union, intersection, symmetric_difference
    {
        'name': 'tests/test_set_union.py',
        'binop': ts_fmt_bf.format('set_union'),
        'gen_list': ts_fmt_gl.format('rand_set_list'),
        'intensity': 'quick',
    },
    {
        'name': 'tests/test_set_intersection.py',
        'binop': ts_fmt_bf.format('set_intersection'),
        'gen_list': ts_fmt_gl.format('rand_set_list'),
        'intensity': 'quick',
    },
    {
        'name': 'tests/test_set_symmetric_difference.py',
        'binop': ts_fmt_bf.format('set_symmetric_difference'),
        'gen_list': ts_fmt_gl.format('rand_set_list'),
        'intensity': 'quick',
    },
    # Multiset: add/sub. (union/intersection)
    {
        'name': 'tests/test_multiset_add_sub.py',
        'binop': ts_fmt_bf.format('multiset_add'),
        'inverse': ts_fmt_ibf.format('multiset_sub'),
        'gen_list': ts_fmt_gl.format('rand_multiset_list'),
        'intensity': 'quick',
    },
    # Ints: add/sub, and, or, xor/xor (xor is inverse of itself!
    #       mul,
    {
        'name': 'tests/test_int_add_sub.py',
        'binop': ts_fmt_bf.format('int_add'),
        'inverse': ts_fmt_ibf.format('int_sub'),
        'gen_list': ts_fmt_gl.format('rand_int_list'),
        'intensity': 'quick',
    },
    {
        'name': 'tests/test_int_mul.py',
        'binop': ts_fmt_bf.format('int_mul'),
        'gen_list': ts_fmt_gl.format('rand_int_list'),
        'intensity': 'quick',
    },
    {
        'name': 'tests/test_int_and.py',
        'binop': ts_fmt_bf.format('int_and'),
        'gen_list': ts_fmt_gl.format('rand_int_list'),
        'intensity': 'quick',
    },
    {
        'name': 'tests/test_int_or.py',
        'binop': ts_fmt_bf.format('int_or'),
        'gen_list': ts_fmt_gl.format('rand_int_list'),
        'intensity': 'quick',
    },
    {
        'name': 'tests/test_int_xor.py',
        'binop': ts_fmt_bf.format('int_xor'),
        'inverse': ts_fmt_ibf.format('int_xor'),
        'gen_list': ts_fmt_gl.format('rand_int_list'),
        'intensity': 'quick',
    },
    # Decimal: add/sub, todo: mul/div
    {
        'name': 'tests/test_dec_add_sub.py',
        'binop': ts_fmt_bf.format('dec_add'),
        'inverse': ts_fmt_ibf.format('dec_sub'),
        'gen_list': ts_fmt_gl.format('rand_decimal_list'),
        'intensity': 'quick',
    },
]


def generate_tests(tests):
    """ Go through each test dict and write file. """
    for test in tests:
        name = test.pop('name')
        with open(name, 'w') as file_:
            file_.write(imports)
            file_.write(binop_only_meths.format(**test))
            if 'inverse' in test:
                file_.write(inverse_req_meths.format(**test))


if __name__ == "__main__":
    # only generate locally, not when running on GitHub.
    if environ.get('ON_GH') is None:
        generate_tests(test_files)
