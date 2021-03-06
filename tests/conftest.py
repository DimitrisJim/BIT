import pytest
from sys import maxsize
from random import randrange, seed


def pytest_addoption(parser):
    parser.addoption(
        "--seed", action="store", default=randrange(maxsize),
        help="Seed to seed PRNG. A random default is used if not supplied."
    )


# don't care in what order this is called.
def pytest_configure(config):
    """ Simply sets the seed passed (or generated by default). """
    seed_value = config.getoption("--seed")
    seed(seed_value)


# print seed before tests run:
def pytest_report_header(config, startdir):
    seed_value = config.getoption('--seed')
    return "PRNG seeded with: {0}".format(seed_value)


# print seed on summary, trylast, want it to be as close to bottom
# as possible.
@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if exitstatus:
        seed_value = config.getoption('--seed')
        line = "Seed value used: {0}. " \
            "Use 'pytest --seed {0}' to reproduce run."
        terminalreporter.write_line(line.format(seed_value))
