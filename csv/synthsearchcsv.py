"""
Searches the database using SQL.
"""

import polars as pl

import matplotlib.pyplot as plt
import time
import datetime

begin = time.perf_counter()

data = pl.read_csv("transients.csv")

LIMIT = 3.5

source_names = data.filter(
    pl.col("flux_093") > LIMIT,
    pl.col("time").is_between(
        (
            datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)
        ).timestamp(),
        datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ),
)["source"].to_list()

end = time.perf_counter()

print(f"Time taken: {end - begin} seconds.")
print(
    f"Found {len(source_names)} sources flaring above {LIMIT} mJy in f093 in the last week."
)

# Go back and make a plot of these.

fig, ax = plt.subplots(1, len(source_names), figsize=(10, 5))

if len(source_names) == 1:
    ax = [ax]

for i, source_name in enumerate(source_names):
    begin = time.perf_counter()

    # Filter the df
    filtered = data.filter(
        pl.col("source") == source_name,
        pl.col("time").is_between(
            (datetime.datetime.now() - datetime.timedelta(days=30)).timestamp(),
            datetime.datetime.now().timestamp(),
        ),
    )

    end = time.perf_counter()

    print(f"Fetching this data took: {end - begin} seconds.")

    ax[i].errorbar(
        filtered["time"],
        filtered["flux_093"],
        yerr=filtered["uncertainty_093"],
        fmt="o",
        label="f093",
        color="C0",
    )
    ax[i].errorbar(
        filtered["time"],
        filtered["flux_225"],
        yerr=filtered["uncertainty_225"],
        fmt="o",
        label="f225",
        color="C1",
    )
    ax[i].set_xlabel("Time")
    ax[i].set_ylabel("Flux (mJy)")
    ax[i].set_title(source_name)
    ax[i].legend()

plt.savefig("transients_csv.png")
