import time
import requests
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


class Readmoo:
    def __init__(self, book_title: str):
        self.book_title = book_title

    def get_reviews_pipeline(self) -> Optional[List[Tuple]]:
        try:
            self.book_id = self._get_book_id()
            resp = self._req_reviews()
            total_reviews = int(resp["total"])
            resp = self._req_reviews(total_reviews)
            reviews = resp["reviews"]

            result_list = []
            for review in reviews:
                row = Review(
                    title=review["title"],
                    content=review["content"],
                    rating=review["reading"]["rating"],
                    source="readmoo"
                ).__dict__
                result_list.append(row)

            return result_list
        finally:
            driver.quit()

    def _get_book_id(self) -> str:
        driver.get("https://readmoo.com/")

        search_box = driver.find_element(By.NAME, "search_term_string")
        search_box.send_keys(self.book_title)
        time.sleep(3)
        search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='搜尋']")
        search_button.click()
        link_element = driver.find_element(By.CLASS_NAME, "product-link")
        book_id = link_element.get_attribute('data-readmoo-id')

        if book_id:
            return book_id
        else:
            print("未找到 ID")
            return None

    def _req_reviews(self, count: int = 1, offset: int = 0):
        reqUrl = f"https://readmoo.com/api/reviews?readmoo_id={self.book_id}&page%5Bcount%5D={count}&page%5Boffset%5D={offset}"
        resp = requests.request("GET", reqUrl)
        response = resp.json()

        return response
