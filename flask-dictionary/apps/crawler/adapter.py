import scrapy
import csv
import json
import re
from re import search
from io import StringIO
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
# from nltk.tokenize import sent_tokenize, word_tokenize
PUNCTUATIONS=['"','(',')',',',':','.','!','[',']','?',';']
REG_EX=re.compile('|'.join(map(re.escape, PUNCTUATIONS)))
class KikuyuDataSpider(scrapy.Spider):
    """
    Class to scrap data from sportpesa jackpots. The data will be used for the next
    steps in predicting the most probable results
    """
    name='footbaldata'
    start_urls = ['https://www.bible.com/bible/2926/GEN.1.OGKBIBLE']
    def __init__(self):
        self.driver = webdriver.Chrome()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)    
    
    def parse(self, response):
        self.driver.get(response.url)
        #for link in unique_links:
        rows=self.driver.find_elements(By.CSS_SELECTOR,"book")
        words=set([])
        clicked=True
        max_pages=-1
        count=0
        with open('bible.txt','w') as fd:
            while clicked and (count<max_pages or max_pages==-1):
                clicked=False
                for r in rows:
                    contents=r.find_elements(By.CLASS_NAME,'content')
                    for c in contents:
                        fd.writelines(c.text)
                        # Remove punctuation marks
                        data=REG_EX.sub('',c.text)
                        all_words=data.split()
                        words.update(all_words)
                clickable=self.driver.find_elements(By.CLASS_NAME,'yv-gray50-10')
                if len(clickable):
                    print("Not Click enabled: {}".format(len(clickable)))
                    element=clickable[0]
                    actions = ActionChains(self.driver)
                    actions.move_to_element(element).perform()
                    
                    clickable=self.driver.find_elements(By.CLASS_NAME,'next-arrow')
                    if len(clickable)>0:
                        print("Clicking....")
                        element=clickable[0]
                        a=element.find_element(By.TAG_NAME,'a')
                        if a is not None:
                            self.driver.implicitly_wait(5)
                            url='https://www.bible.com{}'.format(a.get_attribute('href'))
                            print(url)
                            self.driver.get(a.get_attribute('href'))
                            clicked=True
                            WebDriverWait(self.driver, 100).until(lambda dr: dr.find_element(By.CLASS_NAME,"book"))
                            print("Reading....")
                            rows=self.driver.find_elements(By.CLASS_NAME,"book")
                        else:
                            print("Arrow link not found....: {}".format(a))  
                    else:
                        print("Arrow not found....")
                else:
                    print("Not Click enabled")
                count=count+1
        print("Analyzed the pages: {}".format(count))
        return [{'word': word} for word in words]
        
    def closed(self, reason):
        print("Reason: {}".format(reason))
        self.driver.close()
        self.driver.quit()
