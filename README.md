# ⚡ PWRSTAT

**pwrstat** is a minimalist power usage diagnostic tool for Linux. It logs battery stats once per minute and helps you analyze session efficiency, power draw, and battery drain over time — no bloat, no background daemons, just clean data.

## 🛠 What it does

- Records battery level, charging state, power draw, and active session info
- Outputs clean, parseable logs for pandas analysis
- Lets you graph power consumption by time of day, battery level, or session combo
- Helps you identify inefficient session mixes and spike-heavy workloads

## 🚀 Getting started

To monitor your own system:

1. Clone the repo and inspect `log.csv` for a demo.
2. Set up a cronjob or systemd timer to run the logging script every minute.
3. Analyze the logs with the included pandas pipeline or build your own.

The logging script is tailored to my setup:
- Lenovo ThinkPad P14s
- VoidLinux (runit)
- KDE Plasma or Sway
- Full brightness, Wi-Fi, Bluetooth, and basic tools enabled

Feel free to adapt it to your own system — the core logic is portable.

## 📈 Why it matters

Ever wondered how much power your graphical session actually draws? Or how much battery you lose per hour with Ollama running in the background?

With pwrstat, I’ve profiled KDE Plasma at a median of **6.6W** — full brightness, full connectivity, no cheating. That’s on a ThinkPad running VoidLinux, with clean session logging and no bloat.

## 🧠 What to track (optional extensions)

Want deeper insights? You can extend the logger to include:

- Wi-Fi and Bluetooth state
- CPU load and temperature
- Disk I/O or active process list
- Session combo profiling (e.g. `sway + ollama`)
- Spike detection via IQR thresholds

## 🪶 Philosophy

Minimal overhead. Maximal clarity. No background daemons, no fancy dashboards — just raw data and clean graphs. If you care about battery life, session efficiency, or just want to know what’s silently draining your machine, pwrstat gives you the tools.

---

