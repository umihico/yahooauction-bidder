from yahooauctionbidder import BidderChrome
import sys


def test():
    username = input()
    password = input()
    auctionurl = input()
    chrome = BidderChrome(username, password)
    logined = chrome._logined()
    print('logined:', logined)
    result, message = chrome.bid(auctionurl, 100)
    print(result, message)


if __name__ == '__main__':
    test()
