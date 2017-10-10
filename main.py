import sys
import threading
from queue import Queue

from crawler import Crawler
from links.domain import get_domain_name
from utils.file_operations import file_to_set

repository_name = str(sys.argv[1])
home = str(sys.argv[2])
count = int(sys.argv[3])
domain_name = get_domain_name(home)
queue_file = repository_name + "/queue.txt"
crawled_file = repository_name + "/crawled.txt"
num_of_threads = 8
q = Queue()
Crawler(repository_name, home, domain_name)


def workers():
    for _ in range(num_of_threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        if count >= len(file_to_set(crawled_file)):
            url = q.get()
            Crawler.crawl_page(threading.current_thread().name, url)
            q.task_done()
        else:
            return


def new_jobs():
    try:
        for link in file_to_set(queue_file):
            q.put(link)
        q.join()
        crawl()
    except KeyboardInterrupt:
        print("Exited")


def crawl():
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        new_jobs()


workers()
crawl()
