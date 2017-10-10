from urllib.request import urlopen

from links.link_finder import LinkFinder
from links.domain import get_domain_name
from utils.file_operations import (create_files, file_to_set, set_to_file)
from utils.job import create_repository


class Crawler:
    repository_name = ""
    base_url = ""
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    queue = set()
    crawled = set()

    def __init__(self, repository_name, base_url, domain_name):
        Crawler.repository_name = repository_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = repository_name + "/queue.txt"
        Crawler.crawled_file = repository_name + "/crawled.txt"
        self.boot()
        self.crawl_page("First crawler", Crawler.base_url)

    @staticmethod
    def boot():
        create_repository(Crawler.repository_name)
        create_files(Crawler.repository_name, Crawler.base_url)
        Crawler.queue = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Crawler.crawled:
            print(thread_name, "crawling", page_url)
            print("Queue", str(len(Crawler.queue)))
            print("Crawled", str(len(Crawler.crawled)))
            Crawler.add_links_to_queue(Crawler.get_links(page_url))
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files()

    @staticmethod
    def get_links(page_url):
        html_string = ""
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader("Content-Type"):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Crawler.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Crawler.queue) or (url in Crawler.crawled):
                continue
            if Crawler.domain_name != get_domain_name(url):
                continue
            Crawler.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Crawler.queue, Crawler.queue_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)
