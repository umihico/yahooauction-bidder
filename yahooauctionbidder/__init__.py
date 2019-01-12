from .login import LoggedinChrome
from .bid import bid
from .logger import log_html
from .logger import log_message


class BidderChrome(LoggedinChrome):
    pass


BidderChrome.bid = bid
BidderChrome.log_html = log_html
BidderChrome.log_message = log_message
