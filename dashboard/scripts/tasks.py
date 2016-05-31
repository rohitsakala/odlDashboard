''' The functions in this file are used to call the functions in the ./utils/scraper.py periodically '''

from celery.task.schedules import crontab
from celery.decorators import periodic_task
import redis
from celery import chain
from django.core.cache import cache
from hashlib import md5
from scripts.utils import scraper
from celery.utils.log import get_task_logger
 
logger = get_task_logger(__name__)

# A periodic task that will run every day to fetch list of OpenDayLight projects 
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def taskGetProjectsList():
    haveLock = False
    Lock = redis.Redis().lock("projects")
    try:
        haveLock = Lock.acquire(blocking=False)
        if haveLock:
            logger.info("Locked")
            chain(
                scraper.getProjectsList(),
                scraper.getRepos(),
                scraper.getComponents(),
                scraper.getBugStatus(),
                scraper.getBugSeverity(),
                scraper.getBugPriority(),
                scraper.getTestCoverage(),
                scraper.getSuccessDensity(),
                scraper.getCommitCountTotal(),
                scraper.getContributorsCount(),
                scraper.getCommitCountLastWeek()
            )
    finally:
        if haveLock:
            logger.info("Released")
            Lock.release()