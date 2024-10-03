"""
Searches the database using SQL.
"""

import sqlite3

import matplotlib.pyplot as plt
import time
import datetime

begin = time.perf_counter()
database = sqlite3.connect("../transients.db")

cursor = database.cursor()

LIMIT = 3.6

res = cursor.execute(
    """
    SELECT DISTINCT source FROM observation
    WHERE flux_093 > ?
    AND time > ? AND time < ?
    """,
    (
        LIMIT,
        datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=7),
        datetime.datetime.now(tz=datetime.timezone.utc),
    ),
)

source_names = [row[0] for row in res]
end = time.perf_counter()

print(f"Time taken: {end - begin} seconds.")
print(
    f"Found {len(source_names)} sources flaring above {LIMIT} mJy in f093 in the last week."
)

# Go back and make a plot of these.

fig, ax = plt.subplots(1, len(source_names), figsize=(10, 5))

for i, source_name in enumerate(source_names):
    begin = time.perf_counter()
    res = cursor.execute(
        """
        SELECT time, flux_093, uncertainty_093, flux_225, uncertainty_225 FROM observation
        WHERE source = ?
        AND time > ? AND time < ?
        ORDER BY time
        """,
        (
            source_name,
            datetime.datetime.now() - datetime.timedelta(days=30),
            datetime.datetime.now(),
        ),
    )

    rows = res.fetchall()

    times = [row[0] for row in rows]
    fluxes_093 = [row[1] for row in rows]
    uncertainties_093 = [row[2] for row in rows]
    fluxes_225 = [row[3] for row in rows]
    uncertainties_225 = [row[4] for row in rows]
    end = time.perf_counter()

    print(f"Fetching this data took: {end - begin} seconds.")

    ax[i].errorbar(
        times, fluxes_093, yerr=uncertainties_093, fmt="o", label="f093", color="C0"
    )
    ax[i].errorbar(
        times, fluxes_225, yerr=uncertainties_225, fmt="o", label="f225", color="C1"
    )
    ax[i].set_xlabel("Time")
    ax[i].set_ylabel("Flux (mJy)")
    ax[i].set_title(source_name)
    ax[i].legend()

plt.savefig("transients.png")
