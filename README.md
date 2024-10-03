Synthetic Lightcurve Service 
============================

A very simple snythetic lightcurve service for the Simons Observatory.
Explores a database-forward interface to transients, providing
egress methods for sub-catalogues as HDF5 files.

To get started, first create your synthetic catalog:

```
python3 prepare/synthcat.py
```

This will take some time as it's generating data for a year's worth
of observations of 10'000 synthetic sources.

You can then analyse this database with the scripts in `database`:

- `synthsearch.py` performs a search on the data to find a handful
  of flaring sources from the past week.
- `synthsubcat.py` creates a sub-catlogue as a HDF5 file that can be
  downloaded for further analysis.

Both of these are extremely fast thanks to the use of the database
technology.