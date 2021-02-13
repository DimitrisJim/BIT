""" Perf for __delitem__ on BIT structure. Should show O(N). """
from common import IMPORT_INIT
import pyperf

# todo: need to call perf with number of loops <= size
# so we don't remove from empty list.
sizes = [2 ** i for i in range(7, 15)]


def perf_delitem():
    """ Continuously delete an item from a BIT. """
    runner = pyperf.Runner()
    for size in sizes:
        runner.timeit(
            "{0}".format(size),
            stmt="del b[0]",
            setup=IMPORT_INIT.format(size),
        )


if __name__ == "__main__":
    perf_delitem()
