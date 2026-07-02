#!/bin/bash
# Launch the keep-active script with OS-level sleep prevention.
#
# `caffeinate` is a built-in macOS tool that needs NO admin rights and NO
# special permission. Its flags block every kind of sleep/idle:
#   -d  prevent the display from sleeping
#   -i  prevent the system from idle-sleeping
#   -m  prevent the disk from sleeping
#   -s  prevent sleep while on AC power
#   -u  declare the user active
# This half works regardless of how locked-down the laptop is. The mouse
# wiggle (for keeping Teams green) is handled by keep_active.py.

cd "$(dirname "$0")" || exit 1
exec caffeinate -dimsu python3 keep_active.py
