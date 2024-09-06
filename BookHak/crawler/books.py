import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List, Tuple, Optional
from BookHak.utils.io import Review


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)  # 不自动关闭浏览器
options.add_argument("--disable-notifications")  # 禁用通知
options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)


class Books:
    def __init__(self, book_title: str):
        self.book_title = book_title

    def get_reviews_pipeline(self) -> Optional[List[Tuple]]:
        try:
            self.book_id = self._get_book_id()
            total_page = self._get_total_page()
            if total_page == 0:
                return []

            result_list = []
            for i in range(total_page):
                rows = self._get_reviews_by_page(i)
                result_list += rows

            return result_list
        finally:
            driver.quit()

    def _get_book_id(self) -> str:
        driver.get("https://www.books.com.tw/?loc=tw_logo_001")

        ad_close = driver.find_element(By.ID, "close_top_banner")
        ad_close.click()
        time.sleep(3)

        type_select = driver.find_element(By.CLASS_NAME, "toggle_btn")
        type_select.click()
        type_item = driver.find_element(By.CSS_SELECTOR, "a[cat=BKA]")
        type_item.click()
        search_box = driver.find_element(By.CLASS_NAME, "search_key")
        search_box.send_keys(self.book_title)
        search_button = driver.find_element(By.CLASS_NAME, "search_btn")
        search_button.click()
        link_element = driver.find_element(By.CSS_SELECTOR, f"a[title={self.book_title}]")
        link_href = link_element.get_attribute("href")
        match = re.search(r'/item/(\d+)/', link_href)
        if match:
            book_id = match.group(1)
            return book_id
        else:
            print("未找到 ID")
            return None

    def _get_reviews_by_page(self, page: int):
        _page = page + 1
        soup = self._req(_page)
        items = soup.find_all('div', class_='box-item type-02')
        result_list = []
        for item in items:
            title = item.find('div', class_='title').find('a').get_text() if item.find('div', class_='title').find('a') else ""
            content = item.find('span', calss='comment-content').get_text()
            rating = item.find('span', class_="bui-star")["title"].removesuffix("顆星")
            row = Review(title=title, content=content, rating=rating, source="books").__dict__
            result_list.append(row)

        return result_list

    def _get_total_page(self) -> int:
        soup = self._req(1)
        total_page = soup.find('em').get_text()

        return int(total_page)

    def _req(self, page: int):
        reqUrl = "https://www.books.com.tw/booksComment/ajaxCommemtFilter"
        headersList = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        payload = {
            "type": "getCommemt",
            "stars[]": "all",
            "daterange": "all",
            "num": page,
            "item": self.book_id
        }
        resp = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        response = resp.json()
        soup = BeautifulSoup(response["htmlData"], 'html.parser')

        return soup
