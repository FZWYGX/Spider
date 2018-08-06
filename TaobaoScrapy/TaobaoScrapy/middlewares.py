# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time
import random


class TaobaoScrapySpiderMiddleware(object):

    def __init__(self, timeout=None):
        self.timeout = timeout
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def __del__(self):
        self.driver.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
        )

    def process_request(self, request, spider):
        """
        用PhantomJS抓取页面
        """
        # self.logger.debug('PhantomJS is Starting')
        page = request.meta.get('page', 1)
        print("我到这里了", )
        # m不重要, m的作用是判断是否刷新页面
        m = random.randint(2, 202)

        try:
            if page == 1:
                self.driver.get(request.url)
                time.sleep(random.uniform(1, 3))
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
                self.driver.execute_script('window.scrollBy(0, 1200)')
                time.sleep(random.uniform(0.5, 1.5))
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                    status=200)
            if page <= m:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()

                time.sleep(random.uniform(1, 3))

                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
                self.driver.execute_script('window.scrollBy(0, 1200)')
                time.sleep(random.uniform(0.5, 1.5))
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                    status=200)

            if page > m:
                self.driver.get(request.url)
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()

                time.sleep(random.uniform(1, 3))

                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
                self.driver.execute_script('window.scrollBy(0, 1200)')
                time.sleep(random.uniform(0.5, 1.5))
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                    status=200)
        except TimeoutException:
            self.driver.get(request.url)
            return HtmlResponse(url=request.url, status=500, request=request)
