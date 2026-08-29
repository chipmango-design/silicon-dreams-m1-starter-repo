# Silicon Dreams · Module 1 · The Elevator Problem

[![GDS](../../workflows/gds/badge.svg)](../../actions/workflows/gds.yml) [![Docs](../../workflows/docs/badge.svg)](../../actions/workflows/docs.yml) [![Test](../../workflows/test/badge.svg)](../../actions/workflows/test.yml) [![FPGA](../../workflows/fpga/badge.svg)](../../actions/workflows/fpga.yml)

This repository is the **Week 1 starter project** for the Silicon Dreams course (`CM-HW-101`), a three-week co-delivered programme from **ChipMango** and **ChipFoundry** that takes learners from RTL to real silicon.

You are about to design a finite-state-machine elevator controller, simulate it, and submit it to the ChipFoundry chipIgnite shuttle. By the end of the week, your design will be on its way to becoming a physical object.

## Course context

| | |
|---|---|
| **Course code** | CM-HW-101 |
| **Module** | M1 — The Elevator Problem |
| **Duration** | Week 1 (≈ 6–10 practical hours) |
| **Language** | Verilog HDL |
| **Platform** | ChipFoundry chipIgnite |
| **Partners** | ChipMango × ChipFoundry · MoU 2026 |
| **Course home** | [chipmango.io/silicon-dreams](https://chipmango.io/silicon-dreams) |

## Quick start

```bash
# 1. Use this repo as a template (green "Use this template" button in GitHub)
#    Create your own fork under your GitHub username.

# 2. Clone your fork
git clone https://github.com/<your-username>/<your-fork-name>.git
cd <your-fork-name>

# 3. Install simulation dependencies
pip install -r test/requirements.txt
sudo apt-get install iverilog gtkwave   # Ubuntu / Debian
brew install icarus-verilog gtkwave     # macOS

# 4. Smoke-test
cd test && make

# Expected: a green "PASS" line and a tb.vcd waveform file.
```

If smoke-test passes, you are ready to open **TB-M1-01 · Welcome to Mango Tower** (see the course materials distributed by ChipMango).

## What is in this repository

| Path | What it is |
|---|---|
| `src/elevator.v` | Top module `tt_um_example` plus three submodules — state machine, 7-segment decoder, one-hot decoder. |
| `src/config.json` | LibreLane configuration. Do not edit unless you have read `TB-M1-08`. |
| `info.yaml` | Shuttle metadata — project title, pinout, author. Replace the author field with your name before submission. |
| `test/tb.v` | Verilog testbench wrapper. Instantiates the DUT and dumps `tb.vcd`. |
| `test/test.py` | Cocotb smoke-test. You will extend it in `SG-M1-07`. |
| `test/Makefile` | Runs iverilog + cocotb. Your main verification harness. |
| `docs/info.md` | Datasheet text. Ends up on your shuttle submission page. |

## Deliberate bugs (course policy)

This starter contains **four deliberate bugs** that are central to the course story. They are not mistakes; they are puzzles. They unlock narratively in Module 2 (the parallel-lift escape room) and are documented in the instructor notes. **Learners should not fix them in Module 1.** The study guides ask learners to find and document them, then leave them in place until Week 2.

If you are a ChipFoundry engineer reviewing this repo and want the full list, see `notes/known-bugs.md` (hidden from learners by course convention).

## What you will submit

By the end of Module 1 you will push the following to your fork:

- `src/elevator.v` — the starter code with an added `DOOR_OPEN` state (`SG-M1-06`)
- `test/test.py` — at least three meaningful cocotb tests (`SG-M1-07`)
- `notes/` — your annotated diagrams, bug log, waveforms, and reflection
- `info.yaml` — updated with your name, a descriptive title, and the project description
- `docs/info.md` — a real datasheet blurb (not the placeholder)

You will then submit the latest commit to the ChipIgnite shuttle from the ChipFoundry portal. See `TB-M1-08` and `SG-M1-08` for the checklist.

## Relationship to `chipdiscover-verilog-template`

This repo is the Module 1 starter. For Module 3 you will also fork [`chipdiscover-verilog-template`](https://github.com/chipfoundry/chipdiscover-verilog-template) — a blank-slate template — because your final boss submission is a multi-module design that integrates the elevator (from this repo) with a new arbiter, a clock-gating cell, and AXIOM's black-box module.

## Learning outcomes (Module 1)

By completing this module, learners will be able to:

- Explain the ChipFoundry chipIgnite shuttle workflow end-to-end.
- Read and write a Verilog module that obeys the `tt_um_*` pinout contract.
- Design a four-state FSM with explicit encoding, transition logic, and safe defaults.
- Distinguish combinational and sequential always blocks and use the correct assignment operator in each.
- Identify and correctly interpret active-low reset conventions.
- Drive one-hot inputs, decode them, and produce 7-segment display output.
- Write a cocotb testbench, run iverilog simulation, and interpret a gtkwave waveform.
- Submit a design to ChipFoundry and resolve first-pass DRC issues.

## Resources

- ChipFoundry platform docs — [chipfoundry.io/docs](https://chipfoundry.io/docs)
- Silicon Dreams course home — [chipmango.io/silicon-dreams](https://chipmango.io/silicon-dreams)
- SkyWater SKY130 PDK — [skywater-pdk.readthedocs.io](https://skywater-pdk.readthedocs.io)
- LibreLane documentation — [librelane.readthedocs.io](https://librelane.readthedocs.io)
- Course Discord — link distributed with enrolment.

## Licence

RTL is released under **Apache-2.0**. Course materials (`docs/`, `notes/`, study guides, videos) are **CC BY-NC-SA 4.0** by ChipMango × ChipFoundry.

---
*ChipMango × ChipFoundry · MoU Partnership 2026 · CM-HW-101*
