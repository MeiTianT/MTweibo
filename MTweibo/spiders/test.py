'''
起始用户
https://weibo.com/u/6544635970

关注列表
https://weibo.com/p/1005056544635970/follow?mod=headfollow
https://weibo.com/p/1005056544635970/follow?page=1

粉丝列表
https://weibo.com/p/1005056544635970/follow?relate=fans&mod=headfans
https://weibo.com/p/1005056544635970/follow?relate=fans&page=3

微博列表
https://weibo.com/p/1005056544635970/home?is_all=1&page=3
https://weibo.com/p/1005053302710805/home?is_all=1&page=3

https://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_all=1&page=3&pagebar=0&id=1005053302710805
https://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_all=1&page=3&pagebar=1&id=1005053302710805


'''

# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from pyquery import PyQuery as pq
# import requests,json
#
#
# url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_all=1&page=3&pagebar=0&id=1005053302710805'
# cookies = {"M_WEIBOCN_PARAMS": "uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword", "MLOGIN": "1", "SUB": "_2A252D8SPDeRhGeBK4lMR8y7Ezj-IHXVV8-zHrDV6PUJbkdANLWXNkW1NRwn4c1op2AySNT1TZANg9QfDbQQf9v1S", "SCF": "AnweqJ38BBBrKcgtzZqRlqJsUe3psF2uxSaAWDk2-I_4ajPbRSZ0Z8kZZuAocGkEy6X29iPAH-DssweT2chZ14M.", "SUHB": "0Ela5pTnamjYno", "SSOLoginState": "1527493855", "_T_WM": "e4875205b59b41be0ca3c6e65b50388e"}
#
# r=requests.get(url,cookies=cookies)#必须带上cookies才能获得网页信息。
# result = json.loads(r.text,encoding='utf-8')
# html=result.get('data')
#
# if html:
#     doc =pq(html)
#     items = doc('div.WB_cardwrap').items()
#     for item in items:
#         weiboM = {
#
#             'deal': item.find('.WB_detail .WB_text').text(),
#
#         }
#         print(weiboM)


# browser = webdriver.PhantomJS()
# wait = WebDriverWait(browser,10)
# cookies = requests.get('http://127.0.0.1:5000/weibo/random').text
# header ={
#     'Cookie':cookies
# }
# r = requests.get('https://weibo.com/p/1005056544635970/follow?mod=headfollow',header=header)
# print(r.cookies)
#
# def index_page():
#     try:
#         url = 'https://weibo.com/p/1005056544635970/follow?mod=headfollow'
#         browser.get(url)
#         print('使用cookies:', browser.get_cookies())
#         print('开始爬取',url)
#         print(browser.page_source)
#
#
#         # #上一页不可点击，则当前页为第一页
#         # first_page = wait.until(
#         #     # 节点可点击
#         #     EC.presence_of_element_located((By.CSS_SELECTOR, 'prev.S_txt1.S_line1.page_dis')))
#         # print(first_page)
#         #
#         #
#         # # 下一页可点击
#         # next_page = wait.until(
#         #     # 节点可点击
#         #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'next.S_txt1.S_line1')))
#         # if next_page:
#         #     next_page.click()
#         #     get_index()
#         #
#         #
#         #
#         # # 下一页不可点击，则当前页为最后一页
#         # no_next_page = wait.until(
#         #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'next.S_txt1.S_line1.page_dis')))
#         # if no_next_page:
#         #     print('当前用户爬取完成，正在爬取下一用户。。。')
#
#     except TimeoutException:
#         print('爬取失败，正在重试。。。')
#         #index_page()
#
#
# def get_index():
#     html = browser.page_source
#     doc = pq(html)
#     items = doc('ul .follow_list').items()
#     print(items)

# if __name__ == '__main__':
#
#     index_page()





