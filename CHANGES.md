# Changes to apply to `jdicorpo/new-fpga-verilog-test`

This folder contains **drop-in replacements** for files in ChipFoundry's existing starter repository at:

> https://github.com/jdicorpo/new-fpga-verilog-test

Applying them turns the current generic elevator template into the **Silicon Dreams CM-HW-101-M1 course starter**, while preserving the existing Verilog source (`src/elevator.v`) unchanged so that the four deliberate course bugs remain in place.

## Files in this folder → where they go in the repo

| This folder | Repo path | Action |
|---|---|---|
| `README.md` | `/README.md` | Replace |
| `info.yaml` | `/info.yaml` | Replace |
| `docs/info.md` | `/docs/info.md` | Replace |
| `test/test.py` | `/test/test.py` | Replace |
| `notes/known-bugs.md` | `/notes/known-bugs.md` (new folder) | **Do not publish** — instructor only. Add `notes/known-bugs.md` to `.gitignore` on the public template. |

## Files that stay unchanged

- `src/elevator.v` — keep exactly as is. The four deliberate bugs are load-bearing for Module 2's narrative.
- `src/config.json` — keep as is. Learners may adjust `PL_TARGET_DENSITY_PCT` per `SG-M1-08`.
- `test/tb.v`, `test/Makefile`, `test/requirements.txt`, `test/README.md`, `test/tb.gtkw` — keep as is.
- `.devcontainer/`, `.github/`, `.gitignore`, `.vscode/`, `LICENSE` — keep as is.

## Suggested git commit message

```
docs(course): rebrand starter for Silicon Dreams CM-HW-101-M1

Adds course context, pinout labels, datasheet text, and extended
cocotb tests for the ChipMango × ChipFoundry collaboration.
Source Verilog unchanged to preserve deliberate teaching bugs.
```

## Verification after applying

1. `cd test && make` — must still produce PASS on the shipped smoke test plus the three new scenario tests (4 passes total).
2. GitHub Action `gds.yml` — must still produce a clean DRC/LVS on the reference machine.
3. `tb.vcd` waveform — must show the same signal transitions as before (source unchanged).
4. Pinout labels in `info.yaml` — verify `floor1..floor8`, `seg_a..seg_g`, `idle_dp`.

## Breaking changes

None. All changes are documentation or additive tests. Learners forking the current version will not see any functional difference; only the narrative framing changes.
