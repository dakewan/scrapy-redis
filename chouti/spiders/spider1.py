# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from ..items import BigfileItem


class Spider1Spider(RedisSpider):
    name = 'spider1'
    redis_key = 'chouti:start_urls'
    allowed_domains = ['chouti.com']
    
    # start_urls = ['https://dig.chouti.com/',]
    #
    # def start_requests(self):
    #     # 设置代理IP
    #     # os.environ['HTTP_PROXY'] = "http://192.168.11.11"
    #     for url in self.start_urls:
    #         yield Request(url=url, callback=self.login, meta={'cookiejar': True},)
    
    def parse(self, response):
        print(response)
        req = Request(
            url='https://dig.chouti.com/login',
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                     'referer': 'https://dig.chouti.com/'},
            body='phone=************&password=************&oneMonth=1',
            meta={"cookiejar": True},
            callback=self.check_login,
        )
        yield req
    
    def check_login(self, response):
        # print(response.text)
        req = Request(
            url='https://dig.chouti.com/',
            method='GET',
            callback=self.show,
            meta={"cookiejar": True},
            dont_filter=True,
        )
        yield req
    
    def show(self, response):
        # print(response)
        # print(response)
        hxs = HtmlXPathSelector(response)
        news_list = hxs.select('//div[@id="content-list"]/div[@class="item"]')
        # print(news_list.extract())
        for new in news_list:
            link_id = new.xpath('.//div[@class="part2"]/@share-linkid').extract_first().strip()
            img_url = new.xpath('.//div[@class="news-pic"]/img/@original').extract_first().strip()
            img_url = 'http:' + img_url
            # title = new.xpath('.//div[@class="part2"]/@share-title').extract_first()
            # print(link_id, img_url)
            yield BigfileItem(url=img_url, type='file', file_name='%s.jpg' % link_id)
            yield Request(
                url='https://dig.chouti.com/link/vote?linksId=%s' % (link_id,),
                method='POST',
                headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'referer': 'https://dig.chouti.com/'},
                meta={"cookiejar": True},
                callback=self.do_favor,
            )
        
        page_list = hxs.select('//*[@id="dig_lcpage"]/ul/li/a/@href').extract()
        for page in page_list:
            page_url = 'http://dig.chouti.com%s' % page
            # print(page_url)
            yield Request(
                url=page_url,
                method='GET',
                callback=self.show
            )
        
    def do_favor(self, response):
        print(response)
