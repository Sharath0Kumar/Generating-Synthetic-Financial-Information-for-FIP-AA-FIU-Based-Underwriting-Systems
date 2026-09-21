from src.temporal.hawkes_generator import HawkesGenerator


hawkes = HawkesGenerator(
    baseline_rate=0.5,
    alpha=0.8,
    beta=1.5,
    seed=42
)

events = hawkes.generate_events(
    duration_days=30,
    max_events=100
)

print("=" * 60)
print("HAWKES TEST")
print("=" * 60)

print("Number of events:", len(events))

print("\nEvent times:")

for event in events:
    print(event)