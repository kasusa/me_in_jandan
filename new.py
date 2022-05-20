from pprint import pprint
import requests
import threading
import base64
import datetime

from sys import argv
from bs4 import BeautifulSoup


class Spider:
    targets = {
        'pic': 'http://jandan.net/pic/',
        'treehole': 'http://jandan.net/treehole/',
        'qa': 'http://jandan.net/qa/'
    }
    request_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    }

    def __init__(self, target_user_name: str) -> None:
        self.username = target_user_name
        self.results = list()
        self.result_lock = threading.Lock()
        self.pool = list()

    def find_in_page(self, url: str) -> list:
        '''
        Find target user and return list like [{url:str,oo:int,xx:int}]
        '''
        try:
            resp = requests.get(url, headers=Spider.request_header)
        except ConnectionError:
            print('Connection error occurred while get page %s.' % url)
            return list()
        if not resp.ok:
            print('Page %s report status code %d.' % (url, resp.status_code))
            return list()
        results = list()
        html = BeautifulSoup(resp.text, 'html.parser')
        for comment in [x for x in html.select('.commentlist>li') if self.username in str(x)]:
            try:
                results.append({
                    'type': url.split('jandan.net/')[1].split('/')[0],
                    'url': 'http://jandan.net/t/'+comment.select('.righttext>a')[0].text,
                    'oo': comment.select('.tucao-like-container')[0].select('span')[0].text,
                    'xx': comment.select('.tucao-unlike-container')[0].select('span')[0].text
                })
            except IndexError:
                continue
        self.result_lock.acquire()
        print('Found %d items in target page %s.' % (len(results), url))
        self.results += results
        self.result_lock.release()

    def get_max_page(self, url: str) -> int:
        try:
            html = BeautifulSoup(requests.get(
                url, headers=Spider.request_header).text, 'html.parser')
            maxium = int(str(html.find_all(class_='current-comment-page')
                         [0]).split('[')[-1].split(']')[0])
        except ConnectionError:
            print('Connection error.')
            return 0
        except TypeError:
            print('HTML Page doesn\'t contains desired data')
            return 0
        except Exception as e:
            print(e)
            return 0
        return maxium

    def generate_url(self, base: str, page: int) -> str:
        return base+base64.urlsafe_b64encode(
            (datetime.datetime.now().strftime(
                "%Y%m%d").__str__()+'-'+str(page)).encode()
        ).decode()

    def start_all_spiders(self) -> list:
        for key, url in Spider.targets.items():
            max_page = self.get_max_page(url)
            print('Target %s has %d pages.' % (key, max_page))
            for i in range(max_page, max_page-20, -1):
                self.pool.append(threading.Thread(target=self.find_in_page,
                                 args=(self.generate_url(url, i),)))
        for i in self.pool:
            i.start()
            i.join()
        return self.results


'''
if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage:')
        print('\t%s username' % argv[0])
        exit(1)
    Spider(argv[1]).start_all_spiders()
'''

pprint(Spider('kasusa').start_all_spiders())
