import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL_FILE = '/home/mcwave/data/image_net/list/fall11_urls.txt'
OUTPUT_DIR = '/home/mcwave/data/image_net/images/'
MAX_QUEUE_SIZE = 2000
MAX_WORKERS = 20

class MultiThreadScraper:

    def __init__(self):
        self.queue_size = 0

    def scrape_url(self, url, output_path):
        print(url)
        try:
            f1 = open(output_path, 'wb') #
            f1.write(requests.get(url, timeout=10).content)
            f1.close()
        except:
            print("Cannot download", url)
        self.queue_size -= 1

    def run_scraper(self):
        f = open(URL_FILE, 'r')
        pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        count = 0

        while True:
            if self.queue_size >= MAX_QUEUE_SIZE:
                time.sleep(1)
                continue

            count += 1

            # Get next line from file
            line = f.readline()

            # if line is empty
            # end of file is reached
            if not line:
                break

            parts = line.split('\t')
            id = parts[0].strip()
            url = parts[1].strip()
            output_path = OUTPUT_DIR + id + ".jpg"
            if os.path.exists(output_path):
                continue
            try:
                self.queue_size += 1
                job = pool.submit(self.scrape_url, url, output_path)
            except Exception as e:
                print(e)
                continue

        f.close()


if __name__ == '__main__':
    scraper = MultiThreadScraper()
    scraper.run_scraper()
