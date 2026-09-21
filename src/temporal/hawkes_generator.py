import random
import math


class HawkesGenerator:
    """
    Exponential Hawkes process simulator using
    Ogata's thinning algorithm.

    Intensity:

        lambda(t) = mu + sum(alpha * exp(-beta * (t - ti)))

    where:

        mu    = baseline intensity
        alpha = excitation strength
        beta  = decay rate
    """

    def __init__(
        self,
        baseline_rate=0.5,
        alpha=0.8,
        beta=1.5,
        seed=42
    ):

        if baseline_rate <= 0:
            raise ValueError(
                "baseline_rate must be greater than 0."
            )

        if alpha < 0:
            raise ValueError(
                "alpha must be non-negative."
            )

        if beta <= 0:
            raise ValueError(
                "beta must be greater than 0."
            )

        # Stability condition for exponential Hawkes process
        if alpha / beta >= 1:
            raise ValueError(
                "Unstable Hawkes process: alpha / beta "
                "must be less than 1."
            )

        self.baseline_rate = baseline_rate
        self.alpha = alpha
        self.beta = beta
        self.random = random.Random(seed)

    def generate_events(
        self,
        duration_days=30,
        max_events=100
    ):
        """
        Generate Hawkes event times using
        Ogata's thinning algorithm.
        """

        events = []

        current_time = 0.0

        # Excitation contributed by all previous events
        excitation = 0.0

        while current_time < duration_days:

            # Current intensity is an upper bound because
            # excitation decays between events.
            current_intensity = (
                self.baseline_rate
                + excitation
            )

            # Generate candidate waiting time
            u = self.random.random()

            while u <= 0:
                u = self.random.random()

            waiting_time = (
                -math.log(u)
                / current_intensity
            )

            candidate_time = (
                current_time
                + waiting_time
            )

            if candidate_time >= duration_days:
                break

            # Excitation decays during waiting time
            excitation *= math.exp(
                -self.beta * waiting_time
            )

            # Intensity at candidate time
            candidate_intensity = (
                self.baseline_rate
                + excitation
            )

            # Thinning step
            acceptance_probability = (
                candidate_intensity
                / current_intensity
            )

            u_accept = self.random.random()

            if u_accept <= acceptance_probability:

                # Accept event
                current_time = candidate_time

                events.append(
                    round(current_time, 6)
                )

                # New event increases excitation
                excitation += self.alpha

                if len(events) >= max_events:
                    break

            else:

                # Reject candidate but move time forward
                current_time = candidate_time

        return events