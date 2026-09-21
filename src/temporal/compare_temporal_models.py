import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

POISSON_PATH = Path(
    "data/generated/poisson_100_datasets.json"
)

HAWKES_PATH = Path(
    "data/generated/hawkes_100_datasets.json"
)


def load_datasets(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# --------------------------------------------------
# Metric calculations
# --------------------------------------------------

def calculate_interarrival_times(events):

    if len(events) < 2:
        return []

    return [
        events[i] - events[i - 1]
        for i in range(1, len(events))
    ]


def calculate_burstiness(events):

    inter_arrivals = calculate_interarrival_times(events)

    if len(inter_arrivals) < 2:
        return 0.0

    mean_value = (
        sum(inter_arrivals)
        / len(inter_arrivals)
    )

    variance = sum(
        (x - mean_value) ** 2
        for x in inter_arrivals
    ) / len(inter_arrivals)

    standard_deviation = math.sqrt(variance)

    if standard_deviation + mean_value == 0:
        return 0.0

    return (
        standard_deviation - mean_value
    ) / (
        standard_deviation + mean_value
    )


def calculate_short_gap_ratio(
    events,
    threshold=1.0
):

    inter_arrivals = calculate_interarrival_times(events)

    if not inter_arrivals:
        return 0.0

    short_gaps = sum(
        1
        for gap in inter_arrivals
        if gap <= threshold
    )

    return short_gaps / len(inter_arrivals)


def calculate_metrics(datasets):

    event_counts = []
    mean_interarrivals = []
    burstiness_values = []
    short_gap_ratios = []

    for dataset in datasets:

        events = dataset["events"]

        event_counts.append(
            len(events)
        )

        inter_arrivals = (
            calculate_interarrival_times(events)
        )

        if inter_arrivals:

            mean_interarrivals.append(
                sum(inter_arrivals)
                / len(inter_arrivals)
            )

        burstiness_values.append(
            calculate_burstiness(events)
        )

        short_gap_ratios.append(
            calculate_short_gap_ratio(events)
        )

    return {
        "event_counts": event_counts,
        "mean_interarrivals": mean_interarrivals,
        "burstiness": burstiness_values,
        "short_gap_ratio": short_gap_ratios
    }


# --------------------------------------------------
# Plot helper
# --------------------------------------------------

def plot_comparison(
    poisson_values,
    hawkes_values,
    title,
    xlabel,
    output_filename
):

    plt.figure(figsize=(8, 5))

    plt.hist(
        poisson_values,
        bins=15,
        alpha=0.6,
        label="Poisson"
    )

    plt.hist(
        hawkes_values,
        bins=15,
        alpha=0.6,
        label="Hawkes"
    )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of datasets")

    plt.legend()
    plt.grid(alpha=0.3)

    output_path = Path(
        "data/generated"
    ) / output_filename

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(
        "Saved:",
        output_path
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 70)
    print("POISSON VS HAWKES TEMPORAL COMPARISON")
    print("=" * 70)

    poisson_datasets = load_datasets(
        POISSON_PATH
    )

    hawkes_datasets = load_datasets(
        HAWKES_PATH
    )

    poisson_metrics = calculate_metrics(
        poisson_datasets
    )

    hawkes_metrics = calculate_metrics(
        hawkes_datasets
    )

    print("\nDatasets loaded:")
    print(
        "Poisson:",
        len(poisson_datasets)
    )
    print(
        "Hawkes:",
        len(hawkes_datasets)
    )

    # --------------------------------------------------
    # Print means
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("MEAN VALUES")
    print("=" * 70)

    print(
        "\nEvent count:"
    )

    print(
        "Poisson:",
        round(
            sum(poisson_metrics["event_counts"])
            / len(poisson_metrics["event_counts"]),
            4
        )
    )

    print(
        "Hawkes:",
        round(
            sum(hawkes_metrics["event_counts"])
            / len(hawkes_metrics["event_counts"]),
            4
        )
    )

    print(
        "\nMean inter-arrival time:"
    )

    print(
        "Poisson:",
        round(
            sum(
                poisson_metrics["mean_interarrivals"]
            )
            / len(
                poisson_metrics["mean_interarrivals"]
            ),
            4
        )
    )

    print(
        "Hawkes:",
        round(
            sum(
                hawkes_metrics["mean_interarrivals"]
            )
            / len(
                hawkes_metrics["mean_interarrivals"]
            ),
            4
        )
    )

    print(
        "\nBurstiness:"
    )

    print(
        "Poisson:",
        round(
            sum(
                poisson_metrics["burstiness"]
            )
            / len(
                poisson_metrics["burstiness"]
            ),
            4
        )
    )

    print(
        "Hawkes:",
        round(
            sum(
                hawkes_metrics["burstiness"]
            )
            / len(
                hawkes_metrics["burstiness"]
            ),
            4
        )
    )

    print(
        "\nShort-gap ratio:"
    )

    print(
        "Poisson:",
        round(
            sum(
                poisson_metrics["short_gap_ratio"]
            )
            / len(
                poisson_metrics["short_gap_ratio"]
            ),
            4
        )
    )

    print(
        "Hawkes:",
        round(
            sum(
                hawkes_metrics["short_gap_ratio"]
            )
            / len(
                hawkes_metrics["short_gap_ratio"]
            ),
            4
        )
    )

    # --------------------------------------------------
    # Generate plots
    # --------------------------------------------------

    plot_comparison(
        poisson_metrics["event_counts"],
        hawkes_metrics["event_counts"],
        "Event Count Distribution",
        "Number of Events",
        "event_count_comparison.png"
    )

    plot_comparison(
        poisson_metrics["mean_interarrivals"],
        hawkes_metrics["mean_interarrivals"],
        "Mean Inter-Arrival Time Distribution",
        "Mean Inter-Arrival Time (days)",
        "interarrival_comparison.png"
    )

    plot_comparison(
        poisson_metrics["burstiness"],
        hawkes_metrics["burstiness"],
        "Burstiness Distribution",
        "Burstiness",
        "burstiness_comparison.png"
    )

    plot_comparison(
        poisson_metrics["short_gap_ratio"],
        hawkes_metrics["short_gap_ratio"],
        "Short-Gap Ratio Distribution",
        "Ratio of Gaps <= 1 Day",
        "short_gap_comparison.png"
    )


if __name__ == "__main__":
    main()