#!/usr/bin/env python3
"""
keep_active.py — keeps the machine active so Teams stays green, the display
doesn't sleep, and the VPN session doesn't time out during long overnight runs.

Designed to work on a locked-down / managed work laptop with limited admin
rights. It never *requires* you to open System Settings:

  * It self-tests at startup and automatically picks the best cursor-move
    method your machine allows:
      - "event"  -> posts real mouse events. Resets the system idle timer, so
                    Teams/Slack stay green. May need Accessibility permission.
      - "warp"   -> repositions the cursor directly. Needs NO permission and
                    always works, so the pointer still moves and the screen
                    stays busy even when the event path is blocked.
  * Sleep prevention does NOT depend on any of the above — that job belongs to
    the `caffeinate` wrapper in run.sh, a built-in macOS tool that needs no
    permission. Always launch via run.sh (or the caffeinate line below).

Behavior:
  * Every CYCLE_SECONDS (default 30s) a "wiggle" burst starts.
  * During each burst (default ~5s) the cursor moves in a random direction,
    changing to a new random direction once per second.
  * Between bursts the cursor is left alone. Movements are small and steer
    back toward center if they drift, so the pointer never runs off-screen.

Stop any time with Ctrl-C.

Launch (recommended — adds permission-free OS-level sleep blocking):
    caffeinate -dimsu python3 keep_active.py
or just:  ./run.sh
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


def move_event(x, y):
    """Move via a synthesized mouse event — resets the idle timer (Teams green).
    Requires Accessibility permission; events are silently dropped without it."""
    evt = Quartz.CGEventCreateMouseEvent(
        None, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, evt)


def move_warp(x, y):
    """Move by repositioning the cursor directly — needs no permission."""
    Quartz.CGWarpMouseCursorPosition((x, y))


def pick_mover():
    """Return (move_fn, mode). Detects whether real events actually take effect.

    Immune to whether you're touching the trackpad: we post an event to a known
    offset and check if the cursor landed there. If it didn't, the event was
    dropped (no Accessibility permission) and we fall back to warp.
    """
    x, y = get_cursor()
    tx, ty = x + 8, y + 8
    move_event(tx, ty)
    time.sleep(0.05)
    nx, ny = get_cursor()
    move_warp(x, y)  # put it back
    if math.hypot(nx - tx, ny - ty) < 3:
        return move_event, "event"
    return move_warp, "warp"


def wiggle_once(move_fn, home_x, home_y):
    """One burst: change direction each STEP_SECONDS for BURST_SECONDS."""
    steps = max(1, BURST_SECONDS // STEP_SECONDS)
    for _ in range(steps):
        x, y = get_cursor()
        # Steer back toward home if we've wandered too far; else go random.
        if math.hypot(x - home_x, y - home_y) > MAX_DRIFT:
            angle = math.atan2(home_y - y, home_x - x)
        else:
            angle = random.uniform(0, 2 * math.pi)
        move_fn(x + math.cos(angle) * MOVE_PIXELS,
                y + math.sin(angle) * MOVE_PIXELS)
        time.sleep(STEP_SECONDS)


def main():
    move_fn, mode = pick_mover()
    print("keep_active running — Ctrl-C to stop.")
    print(f"  burst every {CYCLE_SECONDS}s, ~{BURST_SECONDS}s long, "
          f"new direction every {STEP_SECONDS}s.")
    if mode == "event":
        print("  mode: EVENT — resetting the idle timer, so Teams should stay "
              "green. ✓")
    else:
        print("  mode: WARP — no Accessibility permission, so the cursor moves "
              "and sleep is blocked, but Teams may still show Away.")
        print("        (If you can toggle it: System Settings > Privacy & "
              "Security > Accessibility > add your terminal, then rerun.)")

    idle = max(0, CYCLE_SECONDS - BURST_SECONDS)
    while True:
        home_x, home_y = get_cursor()
        wiggle_once(move_fn, home_x, home_y)
        time.sleep(idle)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
