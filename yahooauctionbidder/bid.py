
from time import sleep
import traceback
from selenium.webdriver.common.keys import Keys


def bid(self, url, price):
    try:
        self.get(url)
        self.xpath(
            "//div[@class='Price__buttonArea']//a[text()='入札する']").click()
        price_input = self.xpath(
            "//div[@class='BidModal__inputArea']//label[text()='最高入札額 ']//input")
        price_input.send_keys(Keys.CONTROL, 'a')
        price_input.send_keys(str(price))
        self.xpath(
            "//div[@class='BidModal__buttonArea']//input[@class='js-validator-submit']").click()
        msg_if_error = element_texts_if_exist(self,
                                              "//p[contains(@class,'BidModal__error') and contains(@style,'block')]")
        if msg_if_error:
            return False, msg_if_error
        self.xpath(
            "//div[@class='SubmitBox']/input[@class='SubmitBox__button SubmitBox__button--bid']").click()
        msg_if_error = element_texts_if_exist(self, "//div[@class='NgAttention']")
        if msg_if_error:
            return False, msg_if_error
        result_text = self.xpath("//div[@id='modAlertBox']//strong").text
        msg = result_text
        if result_text == "入札を受け付けました。あなたが現在の最高額入札者です。":
            return True, msg
        else:
            raise Exception(msg)
    except Exception as e:
        error_msg = traceback.format_exc()
        print(error_msg)
        self.log_outerhtml(error_msg)
        return False, error_msg


def element_texts_if_exist(chrome, xpath):
    elements = chrome.xpaths(xpath)
    if elements:
        return "/".join([e.text.replace("\n", ' ') for e in elements])
    else:
        return False
