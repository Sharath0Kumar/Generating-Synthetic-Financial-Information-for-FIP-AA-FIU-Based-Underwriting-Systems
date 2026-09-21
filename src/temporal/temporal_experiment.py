import random
import math

from src.temporal.hawkes_generator import HawkesGenerator


# ============================================================
# Generate Poisson event times
# ============================================================

def generate_poisson_events(
    baseline_rate=0.5,
    duration_days=30,
    seed=42
):
    """
    Generate events using a homogeneous Poisson process.

    Unlike Hawkes, previous events do not affect
    the probability of future events.
    """

    rng = random.Random(seed)

    events = []
    current_time = 0.0

    while current_time < duration_days:

        u = rng.random()

        waiting_time = -math.log(u) / baseline_rate

        current_time += waiting_time

        if current_time >= duration_days:
            break

        events.append(current_time)

    return events


# ============================================================
# Calculate inter-arrival times
# ============================================================

def calculate_interarrival_times(events):

    if len(events) < 2:
        return []

    return [
        events[i] - events[i - 1]
        for i in range(1, len(events))
    ]


# ============================================================
# Calculate burstiness
# ============================================================

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

    burstiness = (
        standard_deviation - mean_value
    ) / (
        standard_deviation + mean_value
    )

    return burstiness


# ============================================================
# Calculate clustering indicator
# ============================================================

def calculate_short_gap_ratio(
    events,
    threshold=1.0
):
    """
    Percentage of inter-arrival times that are
    shorter than the specified threshold.

    Example:
        threshold = 1 day

    A higher value indicates more short gaps
    between events.
    """

    inter_arrivals = calculate_interarrival_times(events)

    if not inter_arrivals:
        return 0.0

    short_gaps = sum(
        1
        for gap in inter_arrivals
        if gap <= threshold
    )

    return short_gaps / len(inter_arrivals)


# ============================================================
# Print experiment results
# ============================================================

def print_results(
    name,
    events
):

    inter_arrivals = calculate_interarrival_times(events)

    burstiness = calculate_burstiness(events)

    short_gap_ratio = calculate_short_gap_ratio(
        events,
        threshold=1.0
    )

    print("\n" + "=" * 60)

    print(name)

    print("=" * 60)

    print(
        "Number of events:",
        len(events)
    )

    if inter_arrivals:

        mean_interarrival = (
            sum(inter_arrivals)
            / len(inter_arrivals)
        )

        print(
            "Mean inter-arrival time:",
            round(mean_interarrival, 4),
            "days"
        )

        print(
            "Minimum inter-arrival time:",
            round(min(inter_arrivals), 4),
            "days"
        )

        print(
            "Maximum inter-arrival time:",
            round(max(inter_arrivals), 4),
            "days"
        )

    print(
        "Burstiness:",
        round(burstiness, 4)
    )

    print(
        "Short-gap ratio (<= 1 day):",
        round(short_gap_ratio, 4)
    )

    print("\nEvent times:")

    for event in events:

        print(
            round(event, 4)
        )


# ============================================================
# Main experiment
# ============================================================

if __name__ == "__main__":

    duration_days = 30

    baseline_rate = 0.5

    # --------------------------------------------------------
    # Poisson baseline
    # --------------------------------------------------------

    poisson_events = generate_poisson_events(
        baseline_rate=baseline_rate,
        duration_days=duration_days,
        seed=42
    )

    # --------------------------------------------------------
    # Hawkes process
    # --------------------------------------------------------

    hawkes_generator = HawkesGenerator(
        baseline_rate=baseline_rate,
        alpha=0.8,
        beta=1.5,
        seed=42
    )

    hawkes_events = hawkes_generator.generate_events(
        duration_days=duration_days,
        max_events=100
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print_results(
        "POISSON BASELINE",
        poisson_events
    )

    print_results(
        "HAWKES PROCESS",
        hawkes_events
    )