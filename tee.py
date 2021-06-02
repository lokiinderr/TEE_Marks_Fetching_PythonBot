from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import warnings
import urllib.request, urllib.parse, urllib.error
import credentials as cd
import os

    
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

subs = ["CS", "CH", "HS", "MA", "PH", "IC"]
counter = 0

driver = wb.Chrome()
driver.get('https://iiti.cloud/dashboard/home')
time.sleep(2)

search = driver.find_element_by_xpath('//a[@class="btn btn-block btn-primary"]')
search.click()
time.sleep(2)

search1 = driver.find_element_by_xpath('//input[@type="email"]')
search1.click()


search1.send_keys(cd.sender_username)
search1.send_keys(Keys.RETURN)
time.sleep(2)

search2 = driver.find_element_by_xpath('//input[@type="password"]')
search2.click()

search2.send_keys(cd.sender_pass)
search2.send_keys(Keys.RETURN)
time.sleep(10)

driver.find_element_by_xpath('//a[@class="small-box-footer btn btn-primary"]').click()

URL = driver.current_url

html = urllib.request.urlopen(URL).read()

soup = bs(html, 'html.parser')

links = []

subjects = driver.find_elements_by_xpath('//*[@class = "small-box-footer btn btn-primary"]')
for sub in subjects:
    link = sub.get_attribute('href')
    if "evaluated" in link:
        links.append(link)

while(True):
    for ii in links:
        if (counter == 6):
            time.sleep(300)
            counter = 0
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'t')
        driver.get(ii)
        content = driver.page_source
        soupp = bs(content, 'html.parser')
        try:
            result = soupp.find('h3').find('b').text
            os.system("telegram-send",result, subs[counter] )
            print(result, subs[counter])
        except:
            driver.find_element_by_link_text('Back').click()
            counter = counter+1
            continue       
        driver.find_element_by_link_text('Back').click()
        counter = counter+1



