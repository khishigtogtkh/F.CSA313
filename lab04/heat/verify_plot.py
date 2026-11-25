"""Validate MPI output against a serial calculation and plot the two required runs."""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

POINTS = 4096


def serial_heat(steps):
    current = [100.0] + [0.0] * (POINTS - 1)
    for _ in range(steps):
        current = [100.0] + [
            current[i] + 0.25 * (current[i - 1] - 2.0 * current[i] + current[i + 1])
            for i in range(1, POINTS - 1)
        ] + [0.0]
    return current


def read_output(path):
    with path.open(newline="") as file:
        reader = csv.reader(file)
        if next(reader, None) != ["position", "temperature"]:
            raise ValueError(f"{path}: expected position,temperature header")
        rows = [(int(position), float(temperature)) for position, temperature in reader]
    if [position for position, _ in rows] != list(range(POINTS)):
        raise ValueError(f"{path}: expected 4096 positions in order")
    return [temperature for _, temperature in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("boundary_csv", type=Path)
    args = parser.parse_args()

    figure, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True, layout="constrained")
    for steps in (100, 1000):
        temperatures = read_output(args.results / f"heat-{steps}" / "Output.csv")
        errors = [abs(got - want) for got, want in zip(temperatures, serial_heat(steps))]
        if not all(error <= 1e-12 for error in errors):
            raise ValueError(f"{steps} steps: MPI and serial results differ")
        print(f"PASS {steps} steps: {POINTS} ordered points, max MPI/serial error {max(errors):.3g}")
        for axis in axes:
            axis.plot(range(POINTS), temperatures, label=f"{steps} steps")

    boundary = read_output(args.boundary_csv)
    if boundary[1024] != 25.0:
        raise ValueError("Rank 1 did not receive the heat pulse from Rank 0")
    print("PASS Rank 0 -> Rank 1: position 1024 is 25.0 after one step")

    figure.suptitle("Heat diffusion along a 4096-point rod")
    axes[0].set(xlim=(0, POINTS - 1), ylabel="Temperature", title="Full rod")
    axes[1].set(xlim=(0, 100), title="First 100 positions")
    for axis in axes:
        axis.set_xlabel("Position")
        axis.grid(alpha=0.25)
        axis.legend()
    figure.savefig(args.results / "temperature.png", dpi=160)
    plt.close(figure)


if __name__ == "__main__":
    main()
