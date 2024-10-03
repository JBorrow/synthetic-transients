"""
Creates a HDF5 sub-catalogue of sources
that can be used in downstream analysis.
"""

import h5py
import sqlite3

import datetime

database = sqlite3.connect("../transients.db")

cursor = database.cursor()

SIGNAL_TO_NOISE_THRESHOLD = 50.0

res = cursor.execute(
    """
    SELECT DISTINCT source FROM observation
    WHERE flux_093 / uncertainty_093 > ?
    AND time > ? AND time < ?
    """,
    (
        SIGNAL_TO_NOISE_THRESHOLD,
        datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=7),
        datetime.datetime.now(tz=datetime.timezone.utc),
    ),
)

source_names = [row[0] for row in res]

with h5py.File("subcatalogue.h5", "w") as handle:
    # Read each rown from the database and write it to the HDF5 file.
    # We need to transform from AOS to SOA
    # Add some information in a header of the file about this run
    handle.attrs.update({
        "signal_to_noise_threshold": SIGNAL_TO_NOISE_THRESHOLD,
        "time": datetime.datetime.now().isoformat(),
        "number_of_sources": len(source_names),
    })

    for source_name in source_names:
        print("Fetching source ", source_name)
        # First get metadat: ra, dec unchanged.
        res = cursor.execute(
            """
            SELECT ra, dec
            FROM observation
            WHERE source = ?
            """,
            (source_name,),
        )

        ra, dec = res.fetchone()
        
        # Now grab the times and fluxes...
        res = cursor.execute(
            """
            SELECT time, flux_027, uncertainty_027, flux_039, uncertainty_039, flux_093, uncertainty_093, flux_145, uncertainty_145, flux_225, uncertainty_225, flux_280, uncertainty_280
            FROM observation
            WHERE source = ?
            """,
            (source_name,),
        )

        rows = res.fetchall()

        times = [row[0] for row in rows]
        fluxes_027 = [row[1] for row in rows]
        uncertainties_027 = [row[2] for row in rows]
        fluxes_039 = [row[3] for row in rows]
        uncertainties_039 = [row[4] for row in rows]
        fluxes_093 = [row[5] for row in rows]
        uncertainties_093 = [row[6] for row in rows]
        fluxes_145 = [row[7] for row in rows]
        uncertainties_145 = [row[8] for row in rows]
        fluxes_225 = [row[9] for row in rows]
        uncertainties_225 = [row[10] for row in rows]
        fluxes_280 = [row[11] for row in rows]
        uncertainties_280 = [row[12] for row in rows]

        # Write the data to the HDF5 file.
        group = handle.create_group(source_name)
        group.attrs.update({"ra": ra, "dec": dec})

        group.create_dataset("time", data=times)
        group.create_dataset("flux_027", data=fluxes_027)
        group.create_dataset("uncertainty_027", data=uncertainties_027)
        group.create_dataset("flux_039", data=fluxes_039)
        group.create_dataset("uncertainty_039", data=uncertainties_039)
        group.create_dataset("flux_093", data=fluxes_093)
        group.create_dataset("uncertainty_093", data=uncertainties_093)
        group.create_dataset("flux_145", data=fluxes_145)
        group.create_dataset("uncertainty_145", data=uncertainties_145)
        group.create_dataset("flux_225", data=fluxes_225)
        group.create_dataset("uncertainty_225", data=uncertainties_225)
        group.create_dataset("flux_280", data=fluxes_280)
        group.create_dataset("uncertainty_280", data=uncertainties_280)




