import json
from pathlib import Path

from src.temporal.hawkes_generator import HawkesGenerator


def generate_100_hawkes_datasets(
    num_datasets=100,
    baseline_rate=0.5,
    alpha=0.8,
    beta=1.5,
    duration_days=30
):
    """
    Generate 100 independent Hawkes process datasets.
    """

    datasets = []

    for dataset_id in range(1, num_datasets + 1):

        # Different seed for every dataset
        seed = 2000 + dataset_id

        hawkes = HawkesGenerator(
            baseline_rate=baseline_rate,
            alpha=alpha,
            beta=beta,
            seed=seed
        )

        events = hawkes.generate_events(
            duration_days=duration_days,
            max_events=100
        )

        dataset = {
            "dataset_id": dataset_id,
            "seed": seed,
            "baseline_rate": baseline_rate,
            "alpha": alpha,
            "beta": beta,
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
    ALPHA = 0.8
    BETA = 1.5
    DURATION_DAYS = 30

    datasets = generate_100_hawkes_datasets(
        num_datasets=NUM_DATASETS,
        baseline_rate=BASELINE_RATE,
        alpha=ALPHA,
        beta=BETA,
        duration_days=DURATION_DAYS
    )

    output_path = (
        "data/generated/hawkes_100_datasets.json"
    )

    save_datasets(
        datasets,
        output_path
    )

    print("=" * 60)
    print("HAWKES DATASET GENERATION")
    print("=" * 60)

    print("Number of datasets:", len(datasets))
    print("Baseline rate:", BASELINE_RATE, "events/day")
    print("Alpha:", ALPHA)
    print("Beta:", BETA)
    print("Duration:", DURATION_DAYS, "days")
    print("Saved to:", output_path)

    print("\nFirst 5 datasets:")

    for dataset in datasets[:5]:

        print(
            f"Dataset {dataset['dataset_id']}: "
            f"{dataset['number_of_events']} events"
        )