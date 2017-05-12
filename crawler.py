# -*- coding: utf-8 -*-
# 한글을 못읽어 드리는 파이썬을 위한 ㅠㅠ



import scrapy
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class cetizenSpider(scrapy.Spider):
    name = "cetizen"
    start_urls = [
        'http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&qs=&keyword_p=%BE%C6%C0%CC%C6%F96',
    ]


    def start_requests(self):
        iphone_main_url = "http://market.cetizen.com/market.php?q=market&auc_sale=1&escrow_motion=3&sc=1&qs=&keyword_p=%BE%C6%C0%CC%C6%F96"
        yield scrapy.Request(url=iphone_main_url, callback=self.main_page_parse)


    def main_page_parse(self, response):
        visit_page_list = response.css(".clr100>a::attr('href')").extract()

        for url in visit_page_list:
            yield scrapy.Request(url="http://market.cetizen.com"+url, callback=self.parse)

    def parse(self, response):
        """
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        """
        title = response.css(".p17.b.p17.b::text").extract_first()
        spec = response.css(".p15 span::text").extract_first()
        price = int(response.css(".p21::text").extract_first().strip().replace(",",""))
        detail = {"title": title, "spec": spec, "price": price}
        self.save(detail)

    def save(self, detail):
        # Open database connection

        db = MySQLdb.connect("localhost", "jack", password, "roka")

        # prepare a cursor object using cursor() method
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        # MySQLdb.cursors.DictCursor를 사용하는 이유 :  query를 통해 데이터를 얻을때 python의 dict로 얻기 위함

        myDict = {'model': detail["title"], 'price': detail["price"], 'extra': detail["spec"]}

        columns = ','.join(myDict.keys())
        placeholders = ','.join(['%s'] * len(myDict))
        query = "insert into %s (%s) values (%s)" % ("raw_price", columns, placeholders)
        cursor.execute(query, myDict.values())
        db.commit()
        db.close()








"""
Select!!
query = " select * from %s" & (table)
cur.execute(sql);
results = cur.fetchall()
for row in results:
    print row

결과값 {'wifi_data_usage': '11', 'wifi_status': 1L, 'wifi_running': '1', 'wifi_scanning': '1', 'multicasts': '11'}
------------------------------------------------------------------------------------------------------------
Insert!!

dict의 형태의 값을 db에 insert하는 방법입니다. columns과 placeholders를 만든뒤에 query를 생성합니다.
myDict = {'wifi_data_usage': '11', 'wifi_status': 1L, 'wifi_running': '1', 'wifi_scanning': '1', 'multicasts': '11'}


columns = ','.join(myDict.keys())
placeholders = ','.join([%s'] * len (myDict))
query = "insert into %s (%s) values (%s) % (table, columns, placeholders)
cur.execute(query, myDict.values())
con.commit()

----------------------------------------------------------------------------------------------------------------
Delete!!

query = "delete from %s where column like %s" % (table, value)
cur.execute(query)
con.commit()

------------------------------------------------------------------------------------------------------------------------
Update!!

query = "update %s set column = value where column2=%s" % (table, value)
cur.execute(query)
cur.commit()
"""

