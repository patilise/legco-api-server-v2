from appledaily import fetch_news_from_appledaily, fetch
from news import upsert_news
from individual_news import update_individual_news
from likes import update_news_like_count
from datetime import datetime, timedelta
import os

import logging
urllib3_logger = logging.getLogger('slimit')
urllib3_logger.setLevel(logging.CRITICAL)

def get_memory():
    """ Look up the memory usage, return in MB. """
    proc_file = '/proc/{}/status'.format(os.getpid())
    scales = {'KB': 1024.0, 'MB': 1024.0 * 1024.0}
    with open(proc_file, 'rU') as f:
        for line in f:
            if 'VmHWM:' in line:
                fields = line.split()
                size = int(fields[1])
                scale = fields[2].upper()
                return size*scales[scale]/scales['MB']
    return 0.0


def print_memory():
    print("Peak: %f MB" % (get_memory()))



def fetch_apple_daily(rundate):
    appledaily_articles = fetch_news_from_appledaily(rundate.replace("-", ""))
    print("Fetched %d articles" % (len(appledaily_articles)))
    print(upsert_news(appledaily_articles))
    print("Finding related articles")
    print(update_individual_news(appledaily_articles))
    before = datetime.strptime(rundate,"%Y-%m-%d") - timedelta(weeks = 2)
    before = before.strftime("%Y-%m-%d")
    print("Updating like counts from %s" % (before))
    update_news_like_count(before)


for i in range(14, 28):
    today = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
    print(today)
    fetch_apple_daily(today)
print_memory()
