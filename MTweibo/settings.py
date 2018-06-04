BOT_NAME = 'MTweibo'

SPIDER_MODULES = ['MTweibo.spiders']
NEWSPIDER_MODULE = 'MTweibo.spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

#要使自定义的CookiesMiddleWare生效，需令其在
# 内置CookiesMiddleWare（优先级700）之前调用，设置一个比700小的优先级即可
#内置HttpProxyMiddleWare优先级为750
DOWNLOADER_MIDDLEWARES = {
    'MTweibo.middlewares.CookiesMiddleware': 554,
    'MTweibo.middlewares.ProxyMiddleware': 555,
    #'MTweibo.middlewares.UserMiddleware': 546,
}

ITEM_PIPELINES = {
    'MTweibo.pipelines.TimePipeline': 300,
    'MTweibo.pipelines.WeiboPipeline': 301,
    'MTweibo.pipelines.MongoPipeline': 302,
}

#
SELENIUM_TIMEOUT = 20
PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

MONGO_URI = 'localhost'
MONGO_DATABASE = 'MTweibo'

COOKIES_URL = 'http://localhost:5000/weibo/random'
PROXY_URL = 'http://localhost:5555/random'
RETRY_HTTP_CODES = [401, 403, 408, 414, 500, 502, 503, 504]