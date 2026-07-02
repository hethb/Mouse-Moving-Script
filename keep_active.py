#!/usr/bin/env python3
"""
keep_active.py — keeps the machine active so Teams stays green, the display
doesn't sleep, and the VPN session doesn't time out during long overnight runs.

Behavior:
  * Every CYCLE_SECONDS (default 30s), a "wiggle" burst starts.
  * During each burst (default ~5s), the cursor moves in a random direction,
    changing to a new random direction once per second.
  * Between bursts the cursor is left completely alone.

Movement is small and self-correcting (it nudges back toward center if it
drifts too far), so it won't march your pointer off-screen or interfere much
if you happen to sit back down.

Stop it any time with Ctrl-C.

Recommended launch (also blocks idle/display sleep at the OS level):
    caffeinate -dimsu python3 keep_active.py
"""

import math
import random
import time

import Quartz

# ---- Tunables ---------------------------------------------------------------
CYCLE_SECONDS = 30      # how often a wiggle burst begins
BURST_SECONDS = 5       # how long each burst lasts
STEP_SECONDS = 1        # how often the direction changes within a burst
MOVE_PIXELS = 12        # distance moved per direction, in pixels
MAX_DRIFT = 60          # if cursor is farther than this from start, steer back
# -----------------------------------------------------------------------------


def get_cursor():
    """Current cursor position as (x, y)."""
    e = Quartz.CGEventCreate(None)
    p = Quartz.CGEventGetLocation(e)
    return p.x, p.y


def move_to(x, y):
    """Post a mouse-moved event to an absolute screen coordinate."""
    evt = Quartz.CGEventCreateMouseEvent(
        None, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt)


def wiggle_once(home_x, home_y):
    """Run a single burst: change direction each STEP_SECONDS for BURST_SECONDS."""
    steps = max(1, BURST_SECONDS // STEP_SECONDS)
    for _ in range(steps):
        x, y = get_cursor()

        # If we've wandered too far from home, bias the move back toward it;
        # otherwise pick a fully random direction.
        if math.hypot(x - home_x, y - home_y) > MAX_DRIFT:
            angle = math.atan2(home_y - y, home_x - x)
        else:
            angle = random.uniform(0, 2 * math.pi)

        target_x = x + math.cos(angle) * MOVE_PIXELS
        target_y = y + math.sin(angle) * MOVE_PIXELS
        move_to(target_x, target_y)
        time.sleep(STEP_SECONDS)


def main():
    print("keep_active running — Ctrl-C to stop.")
    print(f"  burst every {CYCLE_SECONDS}s, lasting ~{BURST_SECONDS}s, "
          f"redirecting every {STEP_SECONDS}s.")
    idle = max(0, CYCLE_SECONDS - BURST_SECONDS)
    while True:
        home_x, home_y = get_cursor()
        wiggle_once(home_x, home_y)
        time.sleep(idle)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
