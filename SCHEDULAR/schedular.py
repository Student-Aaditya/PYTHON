# scheduler.py
import time
import schedule
from sync_all import sync_all
from config import SYNC_INTERVAL_MIN

schedule.every(SYNC_INTERVAL_MIN).minutes.do(sync_all)

if __name__ == "__main__":
    print("🚀 Scheduler started")
    sync_all()  # run once immediately

    while True:
        schedule.run_pending()
        time.sleep(1)
