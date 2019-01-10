import itertools
import os
import selenium as _selenium
from selenium.webdriver import Chrome as _Chrome
_Chrome.xpath = _Chrome.find_element_by_xpath
_Chrome.xpaths = _Chrome.find_elements_by_xpath
from time import sleep as _sleep
import codecs as _codecs
import ast as _ast
from pprint import pformat as _pformat

cookie_filename = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'cookie.txt')


class LoggedinChrome(_Chrome):
    """provides logined chrome"""

    def __init__(self, username=None, password=None, executable_path="chromedriver", port=0, options=None, service_args=None, desired_capabilities=None, service_log_path=None, chrome_options=None):
        super().__init__(executable_path=executable_path, port=port, options=options, service_args=service_args,
                         desired_capabilities=desired_capabilities, service_log_path=service_log_path, chrome_options=chrome_options)
        loggedin = self._login_by_cookie()
        if not loggedin:
            self._login_by_credential(username, password)
        self._save_cookie()

    def _logined(self):
        self.get("https://auctions.yahoo.co.jp")
        return True if self.xpaths("//div[@id='acWrHeader']//a[text()='ログアウト']") else False

    def _login_by_credential(self, username, password):
        self.get("https://login.yahoo.co.jp")
        self.xpath("//input[@id='username']").send_keys(username)
        if self.xpaths("//button[@id='btnNext']"):
            self.xpath("//button[@id='btnNext']").click()
        for try_time in itertools.count():
            try:
                self.xpath("//input[@id='passwd']").send_keys(password)
            except Exception as e:
                if try_time > 100:
                    raise
                _sleep(0.1)
            else:
                break
        self.xpath("//button[@id='btnSubmit']").click()
        self._save_cookie()

    def _login_by_cookie(self):
        cookies = self._load_cookie()
        self.get("https://auctions.yahoo.co.jp")
        for cookie in cookies:
            self.add_cookie(dict(cookie))
        return self._logined()

    def _load_cookie(self):
        try:
            with _codecs.open(cookie_filename, 'r', 'utf-8') as f:
                cookies = _ast.literal_eval(f.read())
        except FileNotFoundError as e:
            cookies = list()
        return cookies

    def _save_cookie(self):
        cookies = self.get_cookies()
        with _codecs.open(cookie_filename, 'w', 'utf-8') as f:
            f.write(_pformat(cookies))


def test():
    from stdin_credential import username, password
    chrome = LoggedinChrome(username, password)
    chrome.get("https://auctions.yahoo.co.jp/category/list/MacBook-%E3%83%8E%E3%83%BC%E3%83%88%E3%83%96%E3%83%83%E3%82%AF-%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3-Mac-%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3-%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%82%BF/2084212698/?fr=auc-prop&tab_ex=commerce&p=MacBook")
    print(chrome.xpath("//html").text)


if __name__ == '__main__':
    test()
