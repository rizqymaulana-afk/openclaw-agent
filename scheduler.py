# scheduler.py

import time
import schedule
import subprocess

# =========================
# JOB
# =========================

def run_daily_report():

    print(
        "\n🚀 Running Daily AI Report..."
    )

    subprocess.run(
        [
            "python3",
            "unified_sales_agent.py"
        ]
    )

    print(
        "\n✅ Daily Report Finished!"
    )

# =========================
# SCHEDULE TIME
# =========================

schedule.every().day.at(
    "20:00"
).do(
    run_daily_report
)

print(
    "⏰ AI Scheduler Running..."
)

print(
    "Waiting for schedule..."
)

# =========================
# LOOP
# =========================

while True:

    schedule.run_pending()

    time.sleep(1)