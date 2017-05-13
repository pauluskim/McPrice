# -*- coding: utf-8 -*-
# 한글을 못읽어 드리는 파이썬을 위한 ㅠㅠ


from selenium import webdriver
import MySQLdb


# Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
driver = webdriver.Chrome('/Users/jack/roka/chromedriver')
# PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
#driver = webdriver.PhantomJS('/Users/jack/roka/phantomjs-2.1.1-macosx/bin/phantomjs')

driver.implicitly_wait(10)

driver.get('https://nid.naver.com/nidlogin.login')

# 아이디/비밀번호를 입력해준다.
driver.find_element_by_name('id').send_keys('jkkim9103')
driver.find_element_by_name('pw').send_keys('password')

driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "btn_global", " " ))]').click()

driver.get('http://cafe.naver.com/joonggonara')

driver.find_element_by_id("topLayerQueryInput").send_keys("iphone6")
driver.find_element_by_class_name('btn-search-green').click()


iframe = driver.find_element_by_css_selector("iframe#cafe_main")

driver.switch_to_default_content()
driver.switch_to_frame(iframe)

#print(driver.page_source)

links = []
for link in driver.find_elements_by_css_selector('.aaa a.m-tcol-c'):
    links.append(link.get_attribute('href'))


for link in links:
    driver.get(link)
    content_iframe = driver.find_element_by_css_selector("#main-area iframe#cafe_main")

    #driver.switch_to_default_content()
    driver.switch_to.frame(content_iframe)

    empty_box=[]
    for content in driver.find_elements_by_class_name("NHN_Writeform_Main"):
        empty_box.append(content.text)


    db = MySQLdb.connect("localhost", "jack", password, "roka")

    # prepare a cursor object using cursor() method
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    # MySQLdb.cursors.DictCursor를 사용하는 이유 :  query를 통해 데이터를 얻을때 python의 dict로 얻기 위함

    myDict = {'extra': " ".join(empty_box)}

    columns = ','.join(myDict.keys())
    placeholders = ','.join(['%s'] * len(myDict))
    query = "insert into %s (%s) values (%s)" % ("raw_price", columns, placeholders)
    cursor.execute(query, myDict.values())
    db.commit()
    db.close()

driver.close()