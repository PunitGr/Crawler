import sys
import threading
from queue import Queue

from crawler import Crawler
from links.domain import get_domain_name
from utils.file_operations import file_to_set

REPOSITORY_NAME = str(sys.argv[1])
HOMEPAGE = str(sys.argv[2])
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = REPOSITORY_NAME + "/queue.txt"
CRAWLED_FILE = REPOSITORY_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 8
q = Queue()
Crawler(REPOSITORY_NAME, HOMEPAGE, DOMAIN_NAME)


def workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = q.get()
        Crawler.crawl_page(threading.current_thread().name, url)
        q.task_done()


def new_jobs():
    for link in file_to_set(QUEUE_FILE):
        q.put(link)
    q.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        new_jobs()


workers()
crawl()
