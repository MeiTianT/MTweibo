from selenium import webdriver
from logging import getLogger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import requests,json

#对接selenium
class UserMiddleware(object):
    def __init__(self,timeout=None,service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.PhantomJS(service_args=service_args)
        self.browser.set_window_size(1400,700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser,self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        '''
        用PhantomJS抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return:
        '''
        print('PhantomJS is starting')

        try:
            #调用PhantomJS对象的get方法访问Request对应的URL
            #相当于从Request对象里获取url，然后再用PhantomJS加载
            #而不再使用Scrapy里面的Downloader
            self.browser.get(request.url)
            print('网页源代码',self.browser.page_source)
            #print(self.browser.page_source)
            # # 上一页不可点击，则当前页为第一页
            # first_page = self.wait.until(
            #     # 节点可点击
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'prev.S_txt1.S_line1.page_dis')))
            # if first_page :
            #     # 构造返回一个HtmlResponse对象，是Response的子类，会被发送给Spider，传给Request的回调函数进行解析
            #     return HtmlResponse(url=request.url, body=self.browser.page_source, status=200, request=request,
            #                         encoding='utf-8')
            #
            # 下一页可点击
            next_page = self.wait.until(
                # 节点可点击
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'next.S_txt1.S_line1')))
            if next_page:
                print(next_page)
            #     next_page.click()
            #     # 构造返回一个HtmlResponse对象，是Response的子类，会被发送给Spider，传给Request的回调函数进行解析
            #     return HtmlResponse(url=request.url, body=self.browser.page_source, status=200, request=request,
            #                         encoding='utf-8')
            #
            # # 下一页不可点击，则当前页为最后一页
            # no_next_page = self.wait.until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'next.S_txt1.S_line1.page_dis')))
            # if no_next_page:
            #     print('当前用户爬取完成，正在爬取下一用户。。。')
            #
            # #构造返回一个HtmlResponse对象，是Response的子类，会被发送给Spider，传给Request的回调函数进行解析
            # return HtmlResponse(url=request.url,body=self.browser.page_source,status=200,request=request,encoding='utf-8')

        except TimeoutException:
            print('超时')
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))

#对接ip代理池
class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            print('出错啦')
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                print('使用代理 ' + proxy)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

#对接cookies池
class CookiesMiddleware():
    def __init__(self, cookies_url):
        self.logger = getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            print('出错啦')
            return False

    def process_request(self, request, spider):
        print('正在获取Cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            print('使用Cookies ' + json.dumps(cookies))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )