""" Perf for __getitem__ on BIT structure. Should show O(logn). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_getitem():
    """
    Note: based on sizes that are powers of 2.
    Worse place to index for is an index whose bit representation
    will consist of only 1's (a power of two minus 1). 

    I used size-2 here since this __getitem__ counts prefix sums
    *including* a given index, so it adds one to the index passed
    in. (pow_of_2 - 2 + 1 => pow_of_2 - 1 => '1' * log(pow_of_2)
    representation)
    """
    runner = pyperf.Runner()
    for size in SIZES:
        runner.timeit(
            "{0}".format(size),
            stmt="b[{0}]".format(size-2),
            setup=IMPORT_INIT.format(size)
        )


if __name__ == "__main__":
    perf_getitem()
