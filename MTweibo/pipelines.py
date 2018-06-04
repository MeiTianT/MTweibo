import re, time
import pymongo
from MTweibo.items import *

class TimePipeline():
    #crawled_at表示爬取时间
    #将crawled_at字段统一定义为当前时间
    def process_item(self, item, spider):
        #item如果是UserItem或WeiboItem，它的crawled_at为当前时间
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = now
        return item

class WeiboPipeline():
    #数据清洗：将微博发布时间（刚刚、几分钟前、几小时前等）转化为标准时间
    #re匹配时间，提取出其中数字，用当前时间戳（秒为单位）减去相对应
    # 的数字*60（如5分钟为5*60,5小时为5*60*60，昨天为24*60*60）
    def parse_time(self, date):
        if re.match('刚刚', date):
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            minute = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            hour = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
        return date

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            if item.get('created_at'):
                item['created_at'] = item['created_at'].strip()
                item['created_at'] = self.parse_time(item.get('created_at'))
            if item.get('pictures'):
                item['pictures'] = [pic.get('url') for pic in item.get('pictures')]
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #为两个Item添加collection索引，索引字段为ID，因为
        # 大规模爬取涉及数据更新问题，为每个collection添加索引可提高检索效率
        self.db[UserItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):
            #使用updata()方法，第一个参数为查询条件；
            # 第二个参数为爬取的Item，使用$set操作符，如果爬取到重复数据
            # 即对数据进行更新，同时不会删除已存在字段。如果不加$set操作符，
            # 会直接进行Item替换，可能会把已存在的字段清空；
            # 第三个参数为True，表示如果数据不存在，则插入数据；
            # 如此即可做到如果数据存在则更新数据，数据不存在则插入数据，从而获得去重的效果
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, UserRelationItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                #对于关注和粉丝列表，使用$addToSet操作符，
                # 可以在向列表类型的字段插入数据同时去重。
                # 值为需要操作的字段名称；利用$each操作符对需要插入
                # 的列表数据进行遍历，以逐条插入用户的关注或粉丝数据到指定字段
                {'$addToSet':
                    {
                        'follows': {'$each': item['follows']},
                        'fans': {'$each': item['fans']}
                    }
                }, True)
        return item
