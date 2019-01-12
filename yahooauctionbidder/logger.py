import codecs
import os
import sys

log_dirname = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'log')
log_html_filename = os.path.join(log_dirname, 'html.txt')
log_message_filename = os.path.join(log_dirname, 'message.txt')


def log_html(self):
    os.makedirs(log_dirname, exist_ok=True)
    outerHTML = self.xpath("//html").get_attribute("outerHTML")
    with codecs.open(log_html_filename, 'w', 'utf-8') as f:
        f.write(outerHTML)


def log_message(self, message=None):
    os.makedirs(log_dirname, exist_ok=True)
    with codecs.open(log_message_filename, 'w', 'utf-8') as f:
        f.write(message)
