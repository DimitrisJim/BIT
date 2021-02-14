""" Should collect all perf_*.py files and execute them dumping their
.json benchmarking results in the data/ folder.
"""
from pathlib import Path
from subprocess import call

RES_FMT = "stats/results/{0}.json"
CMD_FMT = "python stats/perf_{0}.py -o {file}"
ops = [
    'create', 'layout', 'append',
    'getitem', 'setitem', 'update',
]


def rm_file(file_):
    """ Remove file if it exists. """
    Path(file_).unlink(missing_ok=True)


def run(operation):
    """ Build command, remove old json, run command. """
    result_file = RES_FMT.format(operation)
    rm_file(result_file)
    cmd = CMD_FMT.format(operation, file=result_file)
    print("Running:", cmd)
    call(cmd, shell=True)


def run_all(operations=ops):
    """ Convenience, run all ops in ops. """
    for operation in operations:
        run(operation)

if __name__ == "__main__":
    run_all(ops)

__all__ = ['run_all', 'run']
