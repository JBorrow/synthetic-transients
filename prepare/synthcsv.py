"""
Generates a synthetic tarnsient catalog.
"""

from prepare.synthtrans import Transient
import random
from datetime import timedelta


def synthcat(n: int, filename: str):
    """
    Generates a synthetic transient catalog.
    """

    obs_list = []

    for i in range(n):
        print(i)
        transient = Transient(
            source=f"source_{i}",
            ra=random.uniform(0, 360),
            dec=random.uniform(-90, 90),
            index=random.uniform(-2.0, 2.0),
            time=timedelta(days=random.uniform(-1000, 1000)),
            peak_flux_093=random.uniform(0.0, 3.0),
            noise_floor=random.uniform(0.1, 0.5),
            duration=timedelta(days=random.uniform(0, 20)),
        )

        obs_list += transient.get_observations()

    with open(filename, "w") as handle:
        handle.write(
            "source,time,flux_027,uncertainty_027,flux_039,uncertainty_039,flux_093,uncertainty_093,flux_145,uncertainty_145,flux_225,uncertainty_225,flux_280,uncertainty_280\n"
        )
        # Format the line.
        for obs in obs_list:
            handle.write(
                f"{obs.source},{obs.time.timestamp()},{obs.flux_027},{obs.uncertainty_027},{obs.flux_039},{obs.uncertainty_039},{obs.flux_093},{obs.uncertainty_093},{obs.flux_145},{obs.uncertainty_145},{obs.flux_225},{obs.uncertainty_225},{obs.flux_280},{obs.uncertainty_280}\n"
            )

    return


if __name__ == "__main__":
    cat = synthcat(10000, "../transients.csv")
