import json
import math
from pathlib import Path


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

    mean_value = sum(inter_arrivals) / len(inter_arrivals)

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


def calculate_short_gap_ratio(events, threshold=1.0):
    inter_arrivals = calculate_interarrival_times(events)

    if not inter_arrivals:
        return 0.0

    short_gaps = sum(
        1
        for gap in inter_arrivals
        if gap <= threshold
    )

    return short_gaps / len(inter_arrivals)


def analyze_dataset(events):
    inter_arrivals = calculate_interarrival_times(events)

    result = {
        "number_of_events": len(events),
        "burstiness": calculate_burstiness(events),
        "short_gap_ratio": calculate_short_gap_ratio(events)
    }

    if inter_arrivals:
        result["mean_interarrival"] = (
            sum(inter_arrivals) / len(inter_arrivals)
        )

        result["min_interarrival"] = min(inter_arrivals)
        result["max_interarrival"] = max(inter_arrivals)

    else:
        result["mean_interarrival"] = 0.0
        result["min_interarrival"] = 0.0
        result["max_interarrival"] = 0.0

    return result


def calculate_mean(values):
    return sum(values) / len(values)


def calculate_standard_deviation(values):
    mean = calculate_mean(values)

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / len(values)

    return math.sqrt(variance)


def main():

    # Change this path when analyzing another dataset
    input_path = Path(
        "data/generated/hawkes_100_datasets.json"
    )

    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as file:

        datasets = json.load(file)

    results = []

    for dataset in datasets:

        analysis = analyze_dataset(
            dataset["events"]
        )

        analysis["dataset_id"] = dataset["dataset_id"]

        results.append(analysis)

    # -----------------------------------------
    # Extract metrics
    # -----------------------------------------

    event_counts = [
        result["number_of_events"]
        for result in results
    ]

    mean_interarrivals = [
        result["mean_interarrival"]
        for result in results
        if result["mean_interarrival"] > 0
    ]

    burstiness_values = [
        result["burstiness"]
        for result in results
    ]

    short_gap_ratios = [
        result["short_gap_ratio"]
        for result in results
    ]

    min_interarrivals = [
        result["min_interarrival"]
        for result in results
        if result["min_interarrival"] > 0
    ]

    max_interarrivals = [
        result["max_interarrival"]
        for result in results
        if result["max_interarrival"] > 0
    ]

    # -----------------------------------------
    # Print summary
    # -----------------------------------------

    print("=" * 70)
    print("HAWKES PROCESS ANALYSIS")
    print("=" * 70)

    print("\nNumber of datasets:", len(datasets))

    print("\n1. EVENT COUNT")
    print("-" * 40)
    print(
        "Mean:",
        round(calculate_mean(event_counts), 4)
    )
    print(
        "Standard deviation:",
        round(
            calculate_standard_deviation(event_counts),
            4
        )
    )
    print(
        "Minimum:",
        min(event_counts)
    )
    print(
        "Maximum:",
        max(event_counts)
    )

    print("\n2. INTER-ARRIVAL TIME")
    print("-" * 40)
    print(
        "Mean:",
        round(calculate_mean(mean_interarrivals), 4),
        "days"
    )
    print(
        "Standard deviation:",
        round(
            calculate_standard_deviation(
                mean_interarrivals
            ),
            4
        ),
        "days"
    )
    print(
        "Minimum:",
        round(min(min_interarrivals), 4),
        "days"
    )
    print(
        "Maximum:",
        round(max(max_interarrivals), 4),
        "days"
    )

    print("\n3. BURSTINESS")
    print("-" * 40)
    print(
        "Mean:",
        round(calculate_mean(burstiness_values), 4)
    )
    print(
        "Standard deviation:",
        round(
            calculate_standard_deviation(
                burstiness_values
            ),
            4
        )
    )

    print("\n4. SHORT-GAP RATIO (<= 1 DAY)")
    print("-" * 40)
    print(
        "Mean:",
        round(calculate_mean(short_gap_ratios), 4)
    )
    print(
        "Standard deviation:",
        round(
            calculate_standard_deviation(
                short_gap_ratios
            ),
            4
        )
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()