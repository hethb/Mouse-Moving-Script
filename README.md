# Mouse Moving Script

A tiny background script that keeps your Mac "active" so it looks like you're at your desk when you've stepped away.

## What it does

Every 30 seconds it gently wiggles your mouse cursor for about 5 seconds, changing direction randomly once a second, then leaves it alone until the next round. The movements are small and self-correcting, so your pointer never drifts off-screen.

This is useful for:

- **Keeping Microsoft Teams (or Slack) status green** while you're away from the keyboard.
- **Preventing your display and computer from sleeping** — handy for long, unattended runs (e.g. training or downloading overnight).
- **Staying connected to a VPN** that logs you out after a period of inactivity.

It's built for machines where you can't change the sleep or timeout settings yourself.

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

3. **Grant Accessibility permission**

   macOS blocks apps from moving the mouse unless you allow it. Open **System Settings → Privacy & Security → Accessibility**, click **+**, and add the app you'll run the script from (Terminal, iTerm, or VS Code). Turn its switch **on**, then fully quit and reopen that app.

## Running it

```bash
caffeinate -dimsu python3 keep_active.py
```

Leave the window open and you're set. Press **Ctrl-C** to stop.

> `caffeinate` is a built-in macOS command that adds an extra layer of "stay awake" on top of the mouse movement.

## Tuning

Open `keep_active.py` and adjust the values near the top if you want the wiggles more or less frequent, larger, or longer. The defaults work well for most people.
