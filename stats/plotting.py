""" Plot results obtained from running perf on operations. """
import matplotlib.pyplot as plt
from pyperf import BenchmarkSuite
from common import RES_FMT, OPS, PLOTS_PATH


def get_benchmark(op):
    return BenchmarkSuite.load(RES_FMT.format(op))


def plot_single(op, benches):
    sizes = [int(b.get_name()) for b in benches]
    time = [b.mean() for b in benches]
    
    figure, axes = plt.subplots()  # Create a figure and an axes.
    axes.plot(sizes, time, label=f'{op}')  # Plot some data on the axes.
    axes.set_xlabel('Size')  # Add an x-label to the axes.
    axes.set_ylabel('Time')  # Add a y-label to the axes.
    axes.set_title("")  # Add a title to the axes.
    axes.legend()  # Add a legend.
    figure.savefig(f'{PLOTS_PATH}{op}.png')


def plot_all(ops=OPS):
    for op in ops:
        plot_single(op, get_benchmark(op))


if __name__ == "__main__":
    plot_all(OPS)
