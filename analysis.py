# Author: DarwinRG

# This module provides functionality to create detailed analysis plots for the school cafeteria simulation.
# It generates multiple plots including a histogram of waiting times, a time series plot of waiting times,
# and textual information about the simulation configuration and statistics. The results are saved as a PNG file.


# Packages
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from config import *
import datetime


# Creates detailed analysis with multiple plots and configuration details
def create_detailed_analysis(waiting_times, filename_prefix="simulation"):
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 12))

    # Add title and developer info
    fig.text(
        0.2,
        0.98,
        "School Cafeteria Simulation",
        fontsize=16,
        fontweight="bold",
        ha="center",
    )
    fig.text(
        0.99,
        0.98,
        "Developed by Darwin Guillermo",
        ha="right",
        fontsize=10,
        fontweight="bold",
    )

    # Define grid layout with proper spacing
    gs = plt.GridSpec(3, 2, figure=fig)
    gs.update(top=0.93, bottom=0.05, left=0.1, right=0.95, hspace=0.3, wspace=0.2)

    # Histogram plot
    ax1 = fig.add_subplot(gs[0, :])
    waiting_times_minutes = [t / 60 for t in waiting_times]
    n, bins, patches = ax1.hist(
        waiting_times_minutes, bins=30, edgecolor="black", alpha=0.7, color="skyblue"
    )

    ax1.set_title("Distribution of Student Waiting Times", fontsize=12)
    ax1.set_xlabel("Waiting Time (minutes)")
    ax1.set_ylabel("Number of Students")
    ax1.grid(True, linestyle="--", alpha=0.7)

    # Time series plot
    ax2 = fig.add_subplot(gs[1, :])
    times = np.arange(len(waiting_times))
    ax2.plot(
        times,
        waiting_times_minutes,
        color="blue",
        alpha=0.5,
        label="Individual Waiting Times",
    )

    # Add moving average
    window = 10
    moving_avg = np.convolve(
        waiting_times_minutes, np.ones(window) / window, mode="valid"
    )
    ax2.plot(
        times[window - 1 :],
        moving_avg,
        "r-",
        linewidth=2,
        label=f"{window}-student Moving Average",
    )

    ax2.set_title("Waiting Times Throughout Service Period")
    ax2.set_xlabel("Student Number (Order of Arrival)")
    ax2.set_ylabel("Waiting Time (minutes)")
    ax2.grid(True, linestyle="--", alpha=0.7)
    ax2.legend()

    # Configuration and Statistics Text
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.axis("off")
    config_text = (
        "Simulation Configuration:\n"
        f"Time: {datetime.timedelta(seconds=SIMULATION_START_TIME)} - "
        f"{datetime.timedelta(seconds=SIMULATION_END_TIME)}\n"
        f"Stores: {STORES}\n"
        f"Servers per store: {SERVERS_PER_STORE}\n"
        f"Cashiers per store: {CASHIERS_PER_STORE}\n"
        f"Seating capacity: {SEATING_CAPACITY}\n"
        f"Students range: {MIN_STUDENTS}-{MAX_STUDENTS}\n"
        f"Queue strategy: {STORE_SELECTION_STRATEGY}\n\n"
        "Service Times (seconds):\n"
        f"Order time: {MIN_ORDER_TIME}-{MAX_ORDER_TIME}\n"
        f"Payment time: {MIN_PAYMENT_TIME}-{MAX_PAYMENT_TIME}\n"
        f"Eating time: {MIN_EATING_TIME}-{MAX_EATING_TIME}"
    )
    ax3.text(
        0, 1, config_text, verticalalignment="top", fontfamily="monospace", fontsize=10
    )

    # Statistics Text
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis("off")
    stats_text = (
        "Simulation Results:\n\n"
        f"Students served: {len(waiting_times)}\n"
        f"Average wait: {np.mean(waiting_times)/60:.1f} min "
        f"({np.mean(waiting_times):.0f} sec)\n"
        f"Median wait: {np.median(waiting_times)/60:.1f} min "
        f"({np.median(waiting_times):.0f} sec)\n"
        f"Std deviation: {np.std(waiting_times)/60:.1f} min "
        f"({np.std(waiting_times):.0f} sec)\n"
        f"Min wait: {np.min(waiting_times)/60:.1f} min "
        f"({np.min(waiting_times):.0f} sec)\n"
        f"Max wait: {np.max(waiting_times)/60:.1f} min "
        f"({np.max(waiting_times):.0f} sec)\n"
        f"95th percentile: {np.percentile(waiting_times, 95)/60:.1f} min "
        f"({np.percentile(waiting_times, 95):.0f} sec)\n\n"
        f"Service Rate: {len(waiting_times)/((SIMULATION_END_TIME-SIMULATION_START_TIME)/60):.2f} "
        "students/minute"
    )
    ax4.text(
        0, 1, stats_text, verticalalignment="top", fontfamily="monospace", fontsize=10
    )

    # Adjust subplot layout
    plt.subplots_adjust(top=0.93)

    # Create results directory if it doesn't exist
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Save the plot
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(results_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")

    # Print statistics to console
    print("\n=== Simulation Summary ===")
    print(config_text)
    print("\n" + stats_text)

    return filename


# If you want to test the analysis independently
if __name__ == "__main__":
    # Example usage with dummy data
    test_waiting_times = np.random.normal(
        1200, 300, 100
    )  # Generate dummy waiting times
    filename = create_detailed_analysis(test_waiting_times, "test_simulation")
    print(f"Analysis saved to: {filename}")
