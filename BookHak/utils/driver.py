from selenium import webdriver


class ChromeDriverManager():
    def __init__(self, detach=True, disable_notifications=True, disable_popup_blocking=True):
        self.options = webdriver.ChromeOptions()
        self._config_options(detach, disable_notifications, disable_popup_blocking)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(10)

    def _config_options(self, detach, disable_notifications, disable_popup_blocking):
        if detach:
            self.options.add_experimental_option('detach', True)  # 不自动关闭浏览器
        if disable_notifications:
            self.options.add_argument("--disable-notifications")  # 禁用通知
        if disable_popup_blocking:
            self.options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截

    def get_driver(self):
        return self.driver
