from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)  #不自动关闭浏览器
options.add_argument("--disable-notifications")  # 禁用通知
options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://readmoo.com/")

    search_box = driver.find_element(By.NAME, "search_term_string")
    book_title = "底層邏輯"

    search_box.send_keys(book_title)
    time.sleep(3)
    search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='搜尋']")
    search_button.click()
    time.sleep(3)
    link_element = driver.find_element(By.CSS_SELECTOR, f"a[aria-label={book_title}]")
    link_element.click()

finally:
    driver.quit()
