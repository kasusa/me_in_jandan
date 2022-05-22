# me_in_jandan
欢迎蛋友！
你可以利用脚本搜索自己在jandan发过的帖子。
<!-- ![image](https://user-images.githubusercontent.com/49443405/169438781-1489c4ed-0405-4712-b8ca-9f9d5bf9b768.png) -->
![image](https://user-images.githubusercontent.com/49443405/169491375-e97f0eda-088a-4b21-947c-579d5e3f4798.png)

# credit
- kasusa 
- Xeterium


# 使用
下载源码后，首先需要确保拥有这些pip包，下载pip包太慢可以参考这个[pip配置豆瓣源](https://kasusa.github.io/hugo/posts/pip%E9%85%8D%E7%BD%AE%E6%BA%90/)
```
pip install bs4
pip install requests
```
可以通过传递参数的方式来指定搜索用户名、爬取的页数。

![image](https://user-images.githubusercontent.com/49443405/169511417-82041e87-7ea8-4907-8e20-0ca450c804b6.png)


你可以对配置文件进行修改，如配置自己的用户名`TARGET_USER_NAME`。

`BASE_URLS` 是要进行爬取的网站列表，如树洞、无聊图、问答区，去掉自己不需要爬取的url可以提升脚本的速度。
```
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
```
**高阶**：另外还提供了一个`jandan.bat`，可以把它放在自己的用户目录，这样可以在命令行中快速启动脚本!

# 未来计划
- 增加oo、xx数量的显示 ✅
<!-- - 使用 [pyscript](https://pyscript.net/) 把该脚本变成一个可以在线使用的webpage ❌(该计划不可行，pyscript不能使用requests库） -->
- 考虑使用[django](https://github.com/Jason-Oleana/How-to-run-a-python-script-by-clicking-on-an-html-button)把该脚本变成一个可以在线使用的webpage
- 增加自己对他人帖子回复的查询功能（需要借助浏览器插件记录回复的帖子id）
