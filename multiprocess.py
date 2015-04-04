#!/usr/bin/env python3

import logging
import os
from time import time

# Multi-processing
from functools import partial
from multiprocessing.pool import Pool

# Downloading
from download import setup_download_dir, get_links, download_link

# Logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

# Number of processes to run
num_processes = 8

def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception('Couldn\'t find IMGUR_CLIENT_ID environment variable!')
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    download = partial(download_link, download_dir)
    with Pool(num_processes) as p:
        p.map(download, links)
    print('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
