# Week 06 Report (R5 / environment) - honest status, 2026-10-24

## 1. Summary
Planned for Week 6 (guide + Week 5 report): conveyor and continuous spawner with a **seeded** random sequence, belt start/stop **with status feedback**, an object lifecycle log, and a **5-minute run** logged to `experiments/week06/environment.csv`.
Delivered instead (ahead of plan): static machine guarding (acrylic shield wings, UR control box), a 4-leg "Manhattan" transit trajectory, a 3-stage return path, and a Blue-bin collision fix.

| Item | Status | Evidence |
|---|---|---|
| Conveyor moving rigid bodies, continuous spawner (max 3 objects, min spacing) | Done | `ConveyorController.cs`, `RandomObjectSpawner.cs` |
| Seeded spawn sequence | **Done in code, untested** | `randomSeed`/`useFixedSeed` fields; needs a two-run comparison in Unity |
| Belt start/stop + status topic (stopped only when actually stopped) | Open | none |
| Object lifecycle log (spawned -> in zone -> selected -> picked/missed) | Open | none |
| 5-minute run, `environment.csv` | Open (template in `experiments/week06/`) | none |
| Static guarding, Manhattan path (counts toward R8, early) | Partial | see decisions D1, D2 |

## 2. Trial data (`experiments/week04/trials.csv`, 550 rows, Oct 3-19)
| Period | Trials | Completed | Rate |
|---|---|---|---|
| Oct 3 | 66 | 63 | 95.5% |
| Oct 4-12 | 291 | 284 | 97.6% |
| Oct 19 (guarding session) | 64 | 56 | 87.5% |
| **All** | **550** | **532** | **96.7%** |

- All 8 failures on Oct 19 were **Blue, `MOVE_TO_BIN`**, before the threshold fix; the last 4 Blue trials passed (small sample - re-validate with >= 20 Blue trials).
- Mean cycle time, Oct 19 successful trials: Red 14.6 s (n=14), Yellow 15.6 s (n=24), Blue 13.5 s (n=18).
- **Caveat (decision D5):** `grasp_success`/`place_success` are set when the command is sent, not from verified object state. Treat them as "command-complete" until Unity reports object status.
- Earlier slides claimed 100% over 500+ trials, ISO 9283 pose accuracy (RP <= 1.2 mm) and < 120 ms collision rejection. The first contradicted the log; the other two were never measured. They have been removed.

## 3. Code changes in this close-out
- `RandomObjectSpawner.cs`: seeded `System.Random` (default seed 42), seed logged at start.
- `task_state_machine.py`: no silent fallbacks. Joint moves use `~plan_attempts` (default 2) then hold and return False; Cartesian moves run only if >= `~cartesian_min_fraction` (default 0.95) of the path is achievable, else hold and fail the trial. **Re-run >= 20 trials and compare with the numbers above - the stricter threshold may expose failures the old fallback hid.**
- `run_workcell.sh`, `create_presentation_*.py`: removed hardcoded `/home/kduy/...` paths.
- `docs/decisions.md` deviation log (D1-D8), `docs/backlog.md` statuses, Week 6 deck regenerated with corrected numbers.

## 4. Next actions
1. Unity: verify seeded sequence (two Play runs, same colour order).
2. Add belt command/status topics and the lifecycle log; run the 5-minute protocol and fill `environment.csv`.
3. Re-validate Blue bin and the new strict planner helpers (>= 20 trials per colour).
4. Add object-state feedback so success flags are measured (D5).
5. Ask the instructor to acknowledge D1-D6 (especially Yellow, D3).

## 5. Decisions needed
- Is a third colour (Yellow) acceptable for M2, or revert to Red/Blue?
- Is the scripted Manhattan fly-over acceptable as an R8 baseline alongside an OMPL comparison?
