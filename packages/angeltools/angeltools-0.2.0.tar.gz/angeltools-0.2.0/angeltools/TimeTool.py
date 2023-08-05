import random
import time
from datetime import datetime, timedelta

from angeltools.StrTool import get_domain, FileLock


def tell_timestamp(time_str=None, str_format="%Y-%m-%d %H:%M:%S"):
    if not time_str:
        return int(time.time())
    return int(time.mktime(time.strptime(time_str, str_format)))


def tell_the_datetime(time_stamp=None, format_str=None):
    time_stamp = time_stamp if time_stamp else time.time()
    if not format_str:
        format_str = "%Y-%m-%d %H:%M:%S"
    return time.strftime(format_str, time.localtime(time_stamp))


def tell_datetime():
    return datetime.now()


def wait(url, time_range: list = None):
    """
    用文件锁实现异步等待器，用于爬虫爬取等待
    :param url: https://api.github.com
    :param time_range: 随机时间列表 [start, end]
    """
    time_range = [10, 30] if not time_range else time_range
    domain = get_domain(url)

    wait_time = random.choice([x/100 for x in range(*[int(i*100) for i in time_range], 1)])

    flock = FileLock(lock_id=domain)
    while time.time() < wait_time + flock.lock_time():
        time.sleep(1)
    flock.mark()

    return True


def years_ago(years: int, time_format=None):
    years = int(years)
    time_now = datetime.now()
    back_years = timedelta(days=365 * years)
    yo = time_now - back_years
    if not time_format:
        return yo
    return yo.strftime(time_format)
