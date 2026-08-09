# -*- coding: utf-8 -*-

"""
Main entry point for the experimental evaluation.

This script provides a unified interface for reproducing the experiments,
figures, and tables reported in the paper.

Usage
-----
Interactive mode:
    python main.py

Command-line mode:
    python main.py <ID>

Examples:
    python main.py 1      # Run Experiment E1
    python main.py 345    # Generate Figures 3, 4, and 5
    python main.py 100    # Generate Table 1
"""

import sys
import time

from Experiments import EXP_Mix



# =============================================================================
# Artifact targets
# =============================================================================

TARGETS = {
    # Experiments
    1: "Experiment E1",
    2: "Experiment E2",

    # Figures
    345: "Figures 3, 4, and 5",
    3: "Figure 3",
    4: "Figure 4",
    5: "Figure 5",
    8: "Figure 8",
    9: "Figure 9",
    11: "Figure 11",
    12: "Figure 12",

    # Tables
    100: "Table 1",
    200: "Table 2",
    300: "Table 3",
}


def print_menu():
    """Display the available artifact-reproduction targets."""

    print(
        """
===============================================================================
                         NDSS ARTIFACT EVALUATION
===============================================================================

Select the experiment, figure, or table you would like to reproduce.

Experiments
-----------
  1     Experiment E1
  2     Experiment E2

Figures
-------
  345   Figures 3, 4, and 5
  3     Figure 3
  4     Figure 4
  5     Figure 5
  8     Figure 8
  9     Figure 9
  11    Figure 11
  12    Figure 12

Tables
------
  100   Table 1
  200   Table 2
  300   Table 3

===============================================================================
"""
    )


def get_target_id():
    """Return the requested target ID from the command line or user input."""

    if len(sys.argv) > 2:
        print("Error: too many command-line arguments.")
        print("Usage: python main.py [ID]")
        sys.exit(1)

    if len(sys.argv) == 2:
        value = sys.argv[1]
    else:
        print_menu()
        value = input("Enter target ID: ").strip()

    try:
        target_id = int(value)
    except ValueError:
        print(f"\nError: '{value}' is not a valid numeric ID.")
        sys.exit(1)

    if target_id not in TARGETS:
        print(f"\nError: target ID {target_id} is not available.")
        print("Run 'python main.py' to see the list of supported targets.")
        sys.exit(1)

    return target_id



def format_elapsed_time(seconds):
    """Return a human-readable representation of an elapsed runtime."""

    if seconds < 60:
        return f"{seconds:.2f} seconds"

    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)} min {seconds:.2f} s"

    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)} h {int(minutes)} min {seconds:.2f} s"

def main():
    """Run the selected artifact-reproduction target and report its runtime."""

    target_id = get_target_id()
    target_name = TARGETS[target_id]

    print("\n" + "=" * 79)
    print(f"Running: {target_name}")
    print(f"Target ID: {target_id}")
    print("=" * 79 + "\n")

    start_time = time.perf_counter()
    EXP_Mix(target_id)
    elapsed = time.perf_counter() - start_time

    print("\n" + "=" * 79)
    print(f"Completed: {target_name}")
    print(f"Elapsed time: {format_elapsed_time(elapsed)}")
    print("=" * 79)


if __name__ == "__main__":
    main()
