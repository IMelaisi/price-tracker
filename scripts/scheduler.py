import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from scripts.run_daily_scrape import run

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scheduled_job():
    logger.info("Starting scheduled scrape run.")
    run()
    logger.info("Scheduled scrape run finished.")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_job, "cron", hour=6, minute=0)

    logger.info("Scheduler started. Waiting for the next scheduled run (daily at 06:00).")
    logger.info("Press Ctrl+C to stop.")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")