''' The functions in this file are used to call the functions in the ./utils/scraper.py periodically '''

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from scripts.utils import scraper
from celery.utils.log import get_task_logger
 
logger = get_task_logger(__name__)
 
# A periodic task that will run every day to fetch list of OpenDayLight projects 
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def taskGetProjectsList():
    logger.info("Started taskGetProjectsList")
    result = scraper.getProjectsList()
    logger.info("Finished taskGetProjectsList")    
			