"""
Generates a synthetic tarnsient catalog.
"""

from synthtrans import Transient
import random
from datetime import timedelta
from sqlmodel import create_engine, SQLModel, Session


def synthcat(n: int, sqlite_url: str):
    """
    Generates a synthetic transient catalog.
    """

    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)

    session = Session(engine)

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

        if i % 100 == 0:
            session.add_all(obs_list)
            session.commit()
            obs_list = []

    session.close_all()

    return


if __name__ == "__main__":
    cat = synthcat(10000, "sqlite:///transients.db")
