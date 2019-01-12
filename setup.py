from setuptools import setup, find_packages
import requests
import os
USERNAME = "umihico"
REPONAME = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]


github_api_url = f"https://api.github.com/repos/{USERNAME}/{REPONAME}"
description = requests.get(github_api_url).json()['description']
topics = requests.get(github_api_url + "/topics", headers={
    "Accept": "application/vnd.github.mercy-preview+json", }).json()['names']
requirements = [
    "selenium",
]


def _version_increment():
    with open('version_texts/version_raw.txt', 'r') as f:
        version = int(float(f.read()))
    version += 1
    version = str(version)
    with open('version_texts/version_raw.txt', 'w') as f:
        f.write(version)
    version = '.'.join(str(version).zfill(3))
    with open('version_texts/version_digitgood.txt', 'w') as f:
        f.write(version)
    return version


setup(
    name=REPONAME,
    version=_version_increment(),
    description=description,
    url=f'https://github.com/{USERNAME}/{REPONAME}',
    author=USERNAME,
    author_email=f'{USERNAME}@users.noreply.github.com',
    license='MIT',
    keywords=' '.join(topics),
    packages=find_packages(exclude=["stdin_credential"]),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
