"""
Creates a synthetic transient.
"""

from pydantic import BaseModel
import random
import numpy as np
import math
from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, Field

FREQUENCIES = [27, 39, 93, 145, 225, 280]


class Observation(SQLModel, table=True):
    """
    Observation parameters.
    """

    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(index=True)
    ra: float
    dec: float
    time: datetime = Field(index=True)

    flux_027: float
    uncertainty_027: float

    flux_039: float
    uncertainty_039: float

    flux_093: float
    uncertainty_093: float

    flux_145: float
    uncertainty_145: float

    flux_225: float
    uncertainty_225: float

    flux_280: float
    uncertainty_280: float


class Transient(BaseModel):
    """
    Helper container for the transient.
    """

    source: str
    ra: float
    dec: float

    # Index for frequency-dependence of flux
    index: float

    # Time since peak flux
    time: timedelta

    # Peak flux
    peak_flux_093: float

    # Typical noise floor
    noise_floor: float

    # Duration of transient
    duration: timedelta

    def get_flux(self, frequency: int, flux_093: float) -> float:
        """
        Returns the flux at a given frequency.
        """

        return (
            (flux_093 * (frequency / 93) ** self.index)
            + self.get_uncertainty()
            + self.noise_floor
        )

    def get_uncertainty(self) -> float:
        """
        Returns the uncertainty at a given frequency.
        """

        return random.random() * math.sqrt(self.noise_floor)

    def get_observations(self, n: int = 365) -> list[Observation]:
        """
        Generates a list of daily observations for the transient.
        """

        START_TIME = datetime.now(timezone.utc)
        TRANSIENT_TIME = START_TIME - self.time

        datetimes = [
            START_TIME - timedelta(days=i) + timedelta(hours=6) * random.random()
            for i in range(n)
        ]

        time_offsets = [(t - TRANSIENT_TIME) / self.duration for t in datetimes]

        # The transients are assumed to just have a single peak which
        # is modelled as a gaussian.

        fluxes_093 = [
            self.peak_flux_093 * np.exp(-time_offset * time_offset)
            for time_offset in time_offsets
        ]

        observations = []

        for t, flux_093 in zip(datetimes, fluxes_093):
            observations.append(
                Observation(
                    source=self.source,
                    ra=self.ra,
                    dec=self.dec,
                    time=t,
                    flux_027=self.get_flux(27, flux_093),
                    uncertainty_027=self.get_uncertainty(),
                    flux_039=self.get_flux(39, flux_093),
                    uncertainty_039=self.get_uncertainty(),
                    flux_093=self.get_flux(93, flux_093),
                    uncertainty_093=self.get_uncertainty(),
                    flux_145=self.get_flux(145, flux_093),
                    uncertainty_145=self.get_uncertainty(),
                    flux_225=self.get_flux(225, flux_093),
                    uncertainty_225=self.get_uncertainty(),
                    flux_280=self.get_flux(280, flux_093),
                    uncertainty_280=self.get_uncertainty(),
                )
            )

        return observations


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    transient = Transient(
        source="test",
        ra=0,
        dec=0,
        index=0.21,
        time=timedelta(days=99),
        peak_flux_093=5.0,
        noise_floor=0.1,
        duration=timedelta(days=10),
    )

    observations = transient.get_observations()

    times = [observation.time for observation in observations]
    fluxes = [observation.flux_093 for observation in observations]
    uncertainties = [observation.uncertainty_093 for observation in observations]

    fluxes_225 = [observation.flux_225 for observation in observations]
    uncertainties_225 = [observation.uncertainty_225 for observation in observations]

    plt.errorbar(times, fluxes, yerr=uncertainties, fmt="o")
    plt.errorbar(times, fluxes_225, yerr=uncertainties_225, fmt="o")

    plt.show()
