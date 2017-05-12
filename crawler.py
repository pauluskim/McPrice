# -*- coding: utf-8 -*-
# 한글을 못읽어 드리는 파이썬을 위한 ㅠㅠ

import scrapy
import MySQLdb


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://market.cetizen.com/market.php?q=view&auc_no=16973117&auc_sale=1&just_one=&just_one_name=&auc_wireless=&auc_make=&auc_price1=&auc_price2=&akeyword=&keyword_p=%BE%C6%C0%CC%C6%F96&auc_img=&kfild=&hotopt=&dealer=&quality=&usim=&asdate=&nowpage=&escrow_motion=3&view_type=&p=1',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)









# Open database connection
db = MySQLdb.connect("localhost","jack",password,"roka" )

# prepare a cursor object using cursor() method
cursor = db.cursor(MySQLdb.cursors.DictCursor)
# MySQLdb.cursors.DictCursor를 사용하는 이유 :  query를 통해 데이터를 얻을때 python의 dict로 얻기 위함

myDict = {'model': 'iphone5', 'price': '40000', 'extra': 'good'}


columns = ','.join(myDict.keys())
placeholders = ','.join(['%s'] * len(myDict))
query = "insert into %s (%s) values (%s)" % ("raw_price", columns, placeholders )
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

