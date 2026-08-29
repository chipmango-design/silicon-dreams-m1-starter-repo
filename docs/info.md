<!---
Datasheet for Silicon Dreams · Module 1 · CM-HW-101-M1
Learners replace this file with their own description before shuttle submission.
-->

# Silicon Dreams M1 — Elevator Controller

A 9-floor elevator finite-state-machine controller, designed as the Week 1 project for the **Silicon Dreams** course (`CM-HW-101`), a co-delivered programme from ChipMango and ChipFoundry.

## How it works

The design implements an elevator state machine with four states (`IDLE`, `MOVING_UP`, `MOVING_DOWN`, `DUMMY`), a one-hot button decoder, and a 7-segment display driver. A delay counter prescales the 50 MHz clock to roughly 5 floors-per-second of visible motion.

- **Inputs** (`ui_in[7:0]`): a one-hot button panel. Pressing `ui_in[n]` requests floor `n+1` (floors 1–8). `ui_in = 8'h00` means "no button pressed" or "floor 0".
- **Outputs** (`uo_out[7:0]`): `uo_out[6:0]` drives the 7-segment display (segments a–g, with bit 0 = segment a). `uo_out[7]` is the idle indicator (decimal point); lit when stationary, dark when moving.
- **Clock**: 50 MHz, 20 ns period.
- **Reset**: active-low on `rst_n`. (Learner note: the starter contains a deliberately buggy reset polarity — see course material.)

## How to test

Press any of the eight input buttons (`ui_in[0]` through `ui_in[7]`). The display will increment or decrement one floor at a time until it reaches the requested floor, then the decimal point re-lights to indicate the cab is idle.

Run the cocotb testbench:

```bash
cd test
make
```

A successful run ends with `PASS` and produces `tb.vcd` — open in gtkwave to inspect signal transitions.

## External hardware

Target demo board: any ChipFoundry chipIgnite dev kit exposing the standard `tt_um_*` pinout. Connect eight momentary push-buttons to `ui[0..7]` with pull-downs; connect `uo[0..6]` to a common-cathode 7-segment display via current-limiting resistors; connect `uo[7]` to the display's decimal point pin.

## Course context

This project is **Module 1 of a three-module course**. In later modules the same design is extended, debugged under adversarial conditions, and integrated with a hardware arbiter that shares the die with a second module. Learners' names will be written into the physical die as metal-layer annotations for the top three submissions in Module 3.

— *ChipMango × ChipFoundry · MoU Partnership 2026 · CM-HW-101*
