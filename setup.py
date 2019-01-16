from setuptools import setup, find_packages
import requests
import os
USERNAME = "umihico"
REPONAME = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
GITHUB_API_URL = f"https://api.github.com/repos/{USERNAME}/{REPONAME}"


requirements = [

]


def get_description():
    description = requests.get(GITHUB_API_URL).json()['description']
    return description


def get_topic():
    topics = requests.get(GITHUB_API_URL + "/topics", headers={
        "Accept": "application/vnd.github.mercy-preview+json", }).json()['names']
    return ' '.join(topics)


def increment_version():
    filename = 'version.txt'
    with open(filename, 'r') as f:
        raw_version = f.read()  # 0.0.3
    int_version = int(raw_version.replace('.', ''))  # 3
    int_version += 1
    new_version = '.'.join(str(int_version).zfill(3))  # 0.0.4
    with open(filename, 'w') as f:
        f.write(new_version)
    return new_version


def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()


description = get_description()
keywords = get_topic()
version = increment_version()
long_description = get_long_description()
setup(
    name=REPONAME,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/{USERNAME}/{REPONAME}',
    author=USERNAME,
    author_email=f'{USERNAME}@users.noreply.github.com',
    license='MIT',
    keywords=keywords,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
