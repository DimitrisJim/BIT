""" Perf for pop on BIT structure, should show O(1) for index == -1. """
from common import IMPORT_INIT
import pyperf

# todo: need to call perf with a value of loops <= size in
# current iteration.
sizes = [2 ** i for i in range(15, 20)]


def perf_pop():
    """ Continuously pop from Binary indexed tree.
    """
    runner = pyperf.Runner()
    for size in sizes:
        runner.timeit(
            "{0}".format(size),
            stmt="b.pop()",
            setup=IMPORT_INIT.format(size),
        )


if __name__ == "__main__":
    perf_pop()
