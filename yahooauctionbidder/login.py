import itertools
import os
import sys
from selenium.webdriver import Chrome
from ppickle import dump, load
Chrome.xpath = Chrome.find_element_by_xpath
Chrome.xpaths = Chrome.find_elements_by_xpath
from time import sleep
import codecs
import ast
from pprint import pformat

cookie_filename = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'cookie.txt')


class LoggedinChrome(Chrome):
    """provides logined chrome"""

    def __init__(self, username=None, password=None, executable_path="chromedriver", port=0, options=None, service_args=None, desired_capabilities=None, service_log_path=None, chrome_options=None):
        super().__init__(executable_path=executable_path, port=port, options=options, service_args=service_args,
                         desired_capabilities=desired_capabilities, service_log_path=service_log_path, chrome_options=chrome_options)
        if not self._logined():
            self._login_by_cookie()
        self.refresh()
        if username and password and not self._logined():
            self._login_by_credential(username, password)
        self._save_cookie()

    def _logined(self):
        def _logined_mainfunc(self):
            return bool(self.xpaths("//div[@id='acWrHeader']//a[text()='ログアウト']"))

        if "yahoo.co.jp" in self.current_url and _logined_mainfunc(self):
            return True
        self.get_if_diff_url("https://auctions.yahoo.co.jp")
        return _logined_mainfunc(self)

    def _login_by_credential(self, username, password):
        self.get_if_diff_url("https://login.yahoo.co.jp")
        self.xpath("//input[@id='username']").send_keys(username)
        if self.xpaths("//button[@id='btnNext']"):
            self.xpath("//button[@id='btnNext']").click()
        timeout_sec = 10
        while True:
            try:
                self.xpath("//input[@id='passwd']").send_keys(password)
            except Exception as e:
                if timeout_sec < 0:
                    raise
                sleep(0.1)
                timeout_sec -= 0.1
            else:
                break
        self.xpath("//button[@id='btnSubmit']").click()
        self._save_cookie()

    def get_if_diff_url(self, url):
        if self.current_url != url:
            self.get(url)

    def _login_by_cookie(self):
        cookies = self._load_cookie()
        self.get_if_diff_url("https://auctions.yahoo.co.jp")
        for cookie in cookies:
            self.add_cookie(dict(cookie))
        return self._logined()

    def _load_cookie(self):
        try:
            cookies = load(cookie_filename)
        except FileNotFoundError as e:
            cookies = list()
        return cookies

    def _save_cookie(self):
        cookies = self.get_cookies()
        dump(cookie_filename, cookies)
