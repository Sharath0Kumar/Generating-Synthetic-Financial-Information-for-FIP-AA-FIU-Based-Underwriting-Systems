import random
import math
import json
from pathlib import Path


def generate_poisson_events(
    baseline_rate=0.5,
    duration_days=30,
    seed=42
):
    """
    Generate event times using a homogeneous Poisson process.

    baseline_rate:
        Average number of events per day.

    duration_days:
        Duration of simulation.

    seed:
        Random seed for reproducibility.
    """

    rng = random.Random(seed)

    events = []
    current_time = 0.0

    while current_time < duration_days:

        # Generate uniform random number
        u = rng.random()

        # Exponential inter-arrival time
        waiting_time = -math.log(u) / baseline_rate

        current_time += waiting_time

        if current_time >= duration_days:
            break

        events.append(round(current_time, 4))

    return events


def generate_100_poisson_datasets(
    num_datasets=100,
    baseline_rate=0.5,
    duration_days=30
):
    """
    Generate multiple independent Poisson datasets.
    """

    datasets = []

    for dataset_id in range(1, num_datasets + 1):

        # Different seed for every dataset
        seed = 1000 + dataset_id

        events = generate_poisson_events(
            baseline_rate=baseline_rate,
            duration_days=duration_days,
            seed=seed
        )

        dataset = {
            "dataset_id": dataset_id,
            "seed": seed,
            "baseline_rate": baseline_rate,
            "duration_days": duration_days,
            "number_of_events": len(events),
            "events": events
        }

        datasets.append(dataset)

    return datasets


def save_datasets(datasets, output_path):

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            datasets,
            file,
            indent=4
        )


if __name__ == "__main__":

    NUM_DATASETS = 100
    BASELINE_RATE = 0.5
    DURATION_DAYS = 30

    datasets = generate_100_poisson_datasets(
        num_datasets=NUM_DATASETS,
        baseline_rate=BASELINE_RATE,
        duration_days=DURATION_DAYS
    )

    output_path = (
        "data/generated/poisson_100_datasets.json"
    )

    save_datasets(
        datasets,
        output_path
    )

    print("=" * 60)
    print("POISSON DATASET GENERATION")
    print("=" * 60)

    print("Number of datasets:", len(datasets))
    print("Baseline rate:", BASELINE_RATE, "events/day")
    print("Duration:", DURATION_DAYS, "days")
    print("Saved to:", output_path)

    print("\nFirst 5 datasets:")

    for dataset in datasets[:5]:

        print(
            f"Dataset {dataset['dataset_id']}: "
            f"{dataset['number_of_events']} events"
        )