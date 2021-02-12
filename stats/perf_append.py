""" Perf file for append operations, should show O(logN). """
from common import sizes
import pyperf


# note: currently checks best case only (append odd pos)
setup = """
from bit import BIT
from operator import add, sub

b = BIT(range({0}), add, sub)
"""


def perf_append():
    runner = pyperf.Runner()
    for size in sizes:
        runner.timeit(
            "{0}".format(size),
            stmt="b.append(0)",
            setup=setup.format(size)
        )


if __name__ == "__main__":
    perf_append()
