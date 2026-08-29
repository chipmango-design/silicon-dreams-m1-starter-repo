# SPDX-FileCopyrightText: © 2026 ChipMango × ChipFoundry · Silicon Dreams CM-HW-101-M1
# SPDX-License-Identifier: Apache-2.0
#
# Course-shipped cocotb test for Silicon Dreams · Module 1 · Elevator controller.
#
# Learners extend this file in study guide SG-M1-07. The shipped version below
# includes the original smoke test (unchanged for CI compatibility) and three
# additional scenario tests that learners use as a template for their own work.
#
# NOTE TO MAINTAINERS: The starter src/elevator.v contains four deliberate bugs
# (see instructor notes). Tests here PASS *despite* those bugs — by construction,
# so that Module 1 completes. The Module 2 fault-injection testbench exposes them.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


# --------- Helper functions (used by extended tests) -------------------------

async def reset_dut(dut, cycles=10):
    """Apply the standard reset sequence for the ChipFoundry harness.

    rst_n is active-LOW in the harness. The starter RTL treats it as active-high,
    which is a deliberate bug — hold 10 cycles and release either way.
    """
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, cycles)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)


def floor_to_one_hot(floor):
    """Map a floor number (0..8) to the one-hot ui_in value."""
    if floor == 0:
        return 0
    return 1 << (floor - 1)


async def press_floor(dut, floor):
    dut.ui_in.value = floor_to_one_hot(floor)


async def wait_for_floor(dut, target, timeout_cycles=5000):
    """Wait until the internal current_floor hits target, or fail."""
    for _ in range(timeout_cycles):
        await RisingEdge(dut.clk)
        try:
            current = int(dut.user_project.em.current_floor.value)
        except ValueError:
            continue  # X/Z during reset
        if current == target:
            return
    assert False, f"Timed out waiting for floor {target}"


# --------- Test 1: Shipped smoke test (unchanged) ---------------------------

@cocotb.test()
async def test_project(dut):
    """Original shipped smoke test — do not remove."""
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await ClockCycles(dut.clk, 1)

    # uo_out[7]=1 (idle), uo_out[6:0]=0b0111111 (digit 0) => 0b10111111
    assert dut.uo_out.value == 0b10111111


# --------- Test 2: Move up from reset ---------------------------------------

@cocotb.test()
async def test_move_up(dut):
    """After reset, pressing floor 5 should drive the cab to floor 5."""
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    await press_floor(dut, 5)
    await wait_for_floor(dut, 5)

    # At floor 5, idle indicator should be ON (uo_out[7] == 1).
    await ClockCycles(dut.clk, 20)  # settle a bit
    assert dut.uo_out.value.integer & 0x80, "Idle indicator not lit at arrival"


# --------- Test 3: Move down from a higher floor ----------------------------

@cocotb.test()
async def test_move_down(dut):
    """Press floor 8, wait for arrival, then press floor 2, wait for descent."""
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    await press_floor(dut, 8)
    await wait_for_floor(dut, 8)

    await press_floor(dut, 2)
    await wait_for_floor(dut, 2)

    await ClockCycles(dut.clk, 20)
    assert dut.uo_out.value.integer & 0x80, "Idle indicator not lit at arrival on floor 2"


# --------- Test 4: Illegal multi-button press -------------------------------

@cocotb.test()
async def test_illegal_input(dut):
    """Pressing two buttons at once must not cause uncontrolled motion.

    With bit_position_to_value's default clause, illegal patterns decode to 0.
    Starting at floor 0, requesting 0 means "stay put". The cab must not move.
    """
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    # Two buttons pressed at once (button 0 and button 1).
    dut.ui_in.value = 0b00000011
    await ClockCycles(dut.clk, 500)

    current = int(dut.user_project.em.current_floor.value)
    assert current == 0, f"Cab moved to floor {current} under illegal input"

    # Idle indicator should still be lit.
    assert dut.uo_out.value.integer & 0x80, "Idle indicator dropped under illegal input"
