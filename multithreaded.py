#!/usr/bin/env python3

import logging
import os
from time import time

# Multi-threading
from queue import Queue
from threading import Thread

# Downloading
from download import setup_download_dir, get_links, download_link

# Logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

# Number of threads to run
num_threads = 8

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            download_link(directory, link)
            self.queue.task_done()

def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception('Couldn\'t find IMGUR_CLIENT_ID environment variable!')
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create worker threads
    for x in range(num_threads):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though
        # the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    # Wait for the queue to finish
    queue.join()
    print('Took {}'.format(time() - ts))

if __name__ == '__main__':
    main()
