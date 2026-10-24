# Week 6 / R5 environment test (to be run)

One row per run in `environment.csv`. Protocol (guide Bai 6.5):
- 5 minutes per run, fixed seed (`RandomObjectSpawner.randomSeed`, default 42), at least 3 belt speeds (e.g. 0.1 / 0.3 / 0.5 m/s) and 2 spawn intervals.
- Count: spawned, reached pick zone, picked, missed, overlaps, jams, objects that fell off. Do not delete failed runs.
- After each run press Reset and check no old object or task survives; rerun the same seed and compare the colour sequence.
- Record the commit hash in every row.
