from datetime import datetime
from random import random
import requests
import base64
from bs4 import BeautifulSoup

# CONFIG
# pages to loop for (dont set it to big bro)
MAX_CRAW_PAGES = 20
# your username for searching
TARGET_USER_NAME = 'kasusa'
# put the links you want to search for at bottom!
BASE_URLS = ['http://jandan.net/treehole']
BASE_URLS = ['http://jandan.net/pic']
BASE_URLS = ['http://jandan.net/qa']
BASE_URLS = ['http://jandan.net/treehole','http://jandan.net/pic','http://jandan.net/qa']
# bull shit mode
VERBOSE = True
VERBOSE = False
emojilist = ['👁️','🐸','👽','⚕️','❤️','👑']

class Crawler:
    def __init__(self, base_url) -> None:
        self.target = TARGET_USER_NAME
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
        self.results = list()
        self.curpage = 0

    @classmethod
    def get_max_pages(self, raw: BeautifulSoup) -> int:
        try:
            return int(str(raw.find_all(class_='current-comment-page')[0]).split('[')[-1].split(']')[0])
        except Exception as e:
            print(e)

    def find_post_in_page(self, page: BeautifulSoup) -> list:
        result = ['http://jandan.net/t/'+i
                  for i in list(map((lambda i: str(i).split("#comment-")[-1].split('&quot')[0]),
                                    list(filter(lambda x: str(x).find(self.target) != -1,
                                                page.select(".commentlist>li>div>div>div>small")))))]
        if VERBOSE == True:
            print(f'Page {self.curpage} Found {len(result)} item(s).')
        else:
            if len(result) !=0 :
                # emoji = emojilist[int((random()*100)) % len(emojilist)]
                emoji = emojilist[len(result)]
                print(f'Page {self.curpage}: {len(result)} '+emoji)
        return result

    def find_post_in_page_detailed_notused(self, page: BeautifulSoup) -> list:
        # BeautifulSoup CSS Selector
        raw_data = page.select(".commentlist>li>div>div>div>small")
        # Find user name in raw_data
        find_target = list(filter(lambda x: str(
            x).find(self.target) != -1, raw_data))
        # split string and get Post ID
        post_id_found = list(
            map((lambda i: str(i).split("#comment-")[-1].split('&quot')[0]), find_target))
        # Get Post URL
        result = ['http://jandan.net/t/'+i for i in post_id_found]
        print('Found %d items.' % len(result))
        return result

    def craw(self) -> list:
        bs = BeautifulSoup(requests.get(
            self.base_url, headers=self.headers).text, "html.parser")
        self.max_pages = self.get_max_pages(bs)
        for i in range(self.max_pages, self.max_pages-MAX_CRAW_PAGES, -1):
            if i < 1:
                break
            url = self.base_url+'/' + \
                base64.urlsafe_b64encode(
                    (datetime.now().strftime("%Y%m%d").__str__()+'-'+str(i)).encode()
                ).decode()
            self.curpage = i
            try:
                resp = requests.get(url, headers=self.headers)
            except Exception as e:
                print('Something went wrong!'+e)
            if not resp.ok:
                print('Oops! Something went wrong!')
                continue
            # if pic or hole
            self.results +=self.find_post_in_page(BeautifulSoup(resp.text, "html.parser"))
        return self.results

print(f'''
\033[0;34m当前配置：\033[0m
（配置均可在py文件顶部更改）
用户：{TARGET_USER_NAME}
页数：{MAX_CRAW_PAGES}
url：{BASE_URLS}
废话模式：{VERBOSE}

\033[0;34m注：\033[0m
无聊图总页数约为180，树洞约为80，问答约为10
若命令行支持，可以“ctrl+点击”打开url
''')

print('🐢爬行中…')
for url in BASE_URLS:
    print(f"\033[0;33;40m{url}\033[0m")
    linklist = Crawler(url).craw()
    if  len(linklist) > 0:
        #green color
        print("\033[0;32m"+str(len(linklist))+' result(s) found'+"\033[0m")
        for link in linklist:
            print(link)
    else:
        print("\033[0;31mno result found\033[0m")
    print("")
input('🐢爬完啦~')
