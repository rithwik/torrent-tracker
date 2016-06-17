#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4
import sys

BASE_URLS = ['https://torrentz.eu/search?f=',
             'https://torrentz.eu/searchA?f=']

NUMBER = 10

LOG_FILE = 'search_log.txt'

SEARCH_LIST = ['ubuntu',
               'elementary os']

# Default to SEARCH_LIST if no search term provided
if len(sys.argv) > 1:
    search_list = sys.argv[1:]
else:
    search_list = SEARCH_LIST

# Read in the results already processed from the log file
try:
    with open(LOG_FILE, 'r') as f:
        old_results = f.read().split('\n')
except:
    print('No old results found...\n')
    old_results = []


def search(name):
    results = []
    for base_url in BASE_URLS:
        url = base_url + '+'.join(map(str, name.split(' ')))
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        elems = soup.select('dl > dt')
        elems = [x.getText().split(' » ')[0] for x in elems[:NUMBER]]
        for elem in elems:
            results.append(elem)
    return results


f = open(LOG_FILE, 'a')

for name in search_list:
    results = search(name)
    results = set(results) - set(old_results)  # exclude old results
    f.write('\n'.join(results) + '\n')  # write new results to log
    print("-----------------------------------------")
    print('New results for ' + name.upper())
    print("-----------------------------------------")
    print('\n'.join(results) + '\n')

f.close()
