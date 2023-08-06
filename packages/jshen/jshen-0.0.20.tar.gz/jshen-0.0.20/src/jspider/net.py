import urllib
import urllib.request
import bs4
from bs4 import BeautifulSoup
from pathlib import Path
import time
import os
import requests


def send_request(url_: str, sleep_=0.3) -> bs4.BeautifulSoup:
    # 若url是本地的html文件，则无法发送请求
    if "http" not in url_:
        return bs4_local_html(url_)
    req = urllib.request.Request(url_)
    # 设置请求头
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')  # set user-agent header
    # req.add_header('Cookie','xxx')
    response_ = urllib.request.urlopen(req)
    soup = BeautifulSoup(response_, "html.parser")
    # 给服务器减压
    time.sleep(sleep_)
    return soup


def get_soup_by_requests(url: str, params: dict, headers: dict, sleep_=0.3) -> bs4.BeautifulSoup:
    """
    https://curlconverter.com/ may help for auto generating params and headers.
    Be careful of leaking your cookies to this site。

    eg:
        params = {
            'searchtype': '2',
            'page_index': '1',
            ...
            'zoneId': '',
            'pppStatus': '0',
            'agentName': '',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            # 'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Sec-GPC': '1',
        }
    """
    time.sleep(sleep_)
    response = requests.get(url, params=params, headers=headers)
    return BeautifulSoup(response.content, "html.parser")


def download_html(url_, path_):
    """
    从服务器下载html，将其存放在当前文件夹下
    便于本地BeautifulSoup调试

    # BeautifulSoup解析本地html
    soup = BeautifulSoup(open("data.html",encoding="utf-8"), 'lxml')

    :param url_: 进行下载网页的url
    :return:
    """
    req = urllib.request.Request(url_)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')  # set user-agent header
    # req.add_header('Cookie', 'UM_dis3aa97')  # 更改cookie
    response = urllib.request.urlopen(req)
    # 获得当前路径
    # path = os.getcwd() + '/data.html'
    p = Path('.')
    path = p.joinpath(path_)
    fo = open(path, "wb")
    fo.write(response.read())
    fo.close()


def to_html_by_response(response, name="data.html"):
    """
    :param name:
    :param response: type: http.client.HTTPResponse
    :return:
    """
    path = os.getcwd() + f'{name}'
    fo = open(path, "wb")
    fo.write(response.read())
    fo.close()


def bs4_local_html(filename) -> bs4.BeautifulSoup:
    with open(filename, 'rb') as f:
        doc_html = f.read()
    return BeautifulSoup(doc_html, "html.parser")
