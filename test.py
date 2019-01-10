
def test():
    pass


import requests
github_api_url = f"https://api.github.com/repos/umihico/microdb/topics"

description = requests.get(github_api_url, headers={
                           "Accept": "application/vnd.github.mercy-preview+json", }).json()['names']
from pprint import pprint
pprint(description)
if __name__ == '__main__':
    test()
