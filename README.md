# Mouse Moving Script

A tiny background script that keeps your Mac "active" so it looks like you're at your desk when you've stepped away.

## What it does

Every 30 seconds it gently wiggles your mouse cursor for about 5 seconds, changing direction randomly once a second, then leaves it alone until the next round. The movements are small and self-correcting, so your pointer never drifts off-screen.

This is useful for:

- **Keeping Microsoft Teams (or Slack) status green** while you're away from the keyboard.
- **Preventing your display and computer from sleeping** — handy for long, unattended runs (e.g. training or downloading overnight).
- **Staying connected to a VPN** that logs you out after a period of inactivity.

It's built for machines where you can't change the sleep or timeout settings yourself — including **locked-down, managed work laptops with limited admin access**. It needs no admin rights to run.

## Requirements

- A Mac (macOS)
- Python 3

## Setup

1. **Get the code**

   ```bash
   git clone https://github.com/hethb/Mouse-Moving-Script.git
   cd Mouse-Moving-Script
   ```

2. **Install the one dependency**

   ```bash
   python3 -m pip install pyobjc-framework-Quartz
   ```

That's it — no settings changes required.

## Running it

```bash
./run.sh
```

Leave the window open and you're set. Press **Ctrl-C** to stop.

## Works on locked-down laptops (no admin needed)

The script is built to do the most it can with whatever your machine allows, and it tells you which mode it's in when it starts:

- **Preventing sleep and staying on the VPN** is handled by `caffeinate`, a built-in macOS tool that needs **no permission and no admin rights**. This always works.
- **Moving the cursor** always works too — it never runs your pointer off-screen.
- **Keeping Teams green** ideally uses real mouse events, which *may* require Accessibility permission. When the script starts it self-tests:
  - If events work, it prints `mode: EVENT` and Teams should stay green.
  - If they're blocked, it prints `mode: WARP` and keeps moving the cursor / blocking sleep anyway.

If you land in `WARP` mode and *can* reach settings, add your terminal under **System Settings → Privacy & Security → Accessibility**, then rerun — it'll switch to `EVENT` mode automatically. If you can't, the script still keeps your machine awake and on the VPN.

## Tuning

Open `keep_active.py` and adjust the values near the top if you want the wiggles more or less frequent, larger, or longer. The defaults work well for most people.
