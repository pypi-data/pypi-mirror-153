import pickle
import random
from dataclasses import dataclass, field
import datetime
from .net import send_request
import requests
import logging
from .JTime import now
from pathlib import Path


def format_proxy(ip: str, port: str) -> dict:
    ip_port = "%s:%s" % (ip.strip(), port.strip())
    proxy = {
        "http://": ip_port,
        "https://": ip_port
    }
    return proxy


def is_alive(ip, port):
    """Check if a proxy is alive or not
    @return: True if alive, False otherwise
    很费时间，评价某个代理是否可用的标准是 timeout超时
    """
    proxy = format_proxy(ip, port)
    try:
        requests.get('http://www.baidu.com', proxies=proxy, timeout=3)
        return True
    except:
        return False


@dataclass(order=True)
class JProxy:
    """
        每天上午，9点更新代理池
        对代理池，构建一个类:
        * ip
        * port
        * 使用的次数

        功能：
        * 在某个时间段，专门去检查死亡的代理是否还活着
        * 在爬取之前，再检查某个代理是否活着
        * get_proxy方法返回一个活着的ip。
        """
    # ip: str = field(default=None, compare=False)
    port: str = field(default=None, compare=False)
    cnt: int = field(default=0, compare=True)
    born: datetime = field(default=None, compare=False)


def get_proxy_66ip(url_, proxy_impl):
    """
    66代理网页，某一页代理ip的爬取
    http://www.66ip.cn/index.html
    """
    soup = send_request(url_)
    center_tag = soup.select('div[align="center"]')[1]
    tr_tag = center_tag.find_all('tr')
    for tr in tr_tag[1::]:
        tmp = tr.find_all('td')[:2:]
        ip = tmp[0].string.strip()
        port = tmp[1].string.strip()
        if is_alive(ip, port):
            proxy_impl.add(ip, JProxy(port, 0, now()))


def get_proxys(proxy_impl, end_page):
    """
    66代理网页，代理ip的爬取
    这个网站可能会挂，或者网页格式会变化，若出错try,except把错误抛出去
    """
    _66ip = "http://www.66ip.cn/index.html"
    try:
        get_proxy_66ip(_66ip, proxy_impl)
        for p in range(2, end_page + 1):
            url_ = f"http://www.66ip.cn/{p}.html"
            get_proxy_66ip(url_, proxy_impl)
    except Exception as e:
        logging.error(e.args)


class ProxyImpl:
    def __init__(self, grave_obj_path: str):
        self.__item: dict[str:JProxy] = dict()
        self.__grave_obj_path = grave_obj_path
        self.grave: ProxyGrave = load_proxy_grave(grave_obj_path)

    def __getitem__(self, ip):
        return self.__item.get(ip)

    def __iter__(self):
        return self.__item

    def add(self, ip: str, proxy_: JProxy) -> None:
        # 已有的代理，不作处理
        if ip in self.__item:
            return
        # 增加新的代理，没有比对grave中死掉的代理
        self.__item[ip] = proxy_

    def get_random_proxy(self) -> dict:
        """
        随机获取某个代理,
        待处理：如果代理的列表是空，这个异常的处理
        """

        ip = random.choice(list(self.__item.keys()))
        return self.get(ip)

    def get(self, ip) -> dict:
        """
        通过ip获取某个指定的代理
        """
        tmp: JProxy = self.__item[ip]
        return format_proxy(ip, tmp.port)

    def push_grave(self, ip):
        """
        由于某个代理加入时，不会在grave中检查是否已经存在；
        故，当某个这个代理死亡的时候，需要在grave中检测。若端口不一样，用新端口覆盖掉旧端口
        字典删除
        """
        # 删除的元素必须存在
        if ip in self.__item.keys():
            self.grave.receive(ip, self.__item[ip])
            # 立即保存到本地
            pickle.dump(self.grave, open(self.__grave_obj_path, 'wb'))
            del self.__item[ip]

    def __repr__(self):
        return self.__item.__repr__()

    def __len__(self):
        return len(self.__item)


class ProxyGrave:
    """
    没有实质上的用处，只是记录使用过的代理和次数
    对于死亡的代理，会立即从变量中移除，故需要立刻写入grave文件中，避免程序崩溃造成的数据丢失

    未来功能：
        从grave中取出代理，有的代理在未来可能可以重新使用
    """

    def __init__(self):
        self.__items: dict[str:JProxy] = dict()

    def __repr__(self):
        return self.__items.__repr__()

    def receive(self, ip: str, jp: JProxy):
        if ip not in self.__items:
            self.__items[ip] = jp
        else:
            # 有的代理可能会更换端口
            self.__items[ip].port = jp.port
            # 代理的请求次数加起来
            self.__items[ip].cnt += jp.cnt


def load_proxy_grave(obj_path: str) -> ProxyGrave:
    """
    若没有这个文件，那直接创建，返回一个空对象
    """
    p = Path(obj_path)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return ProxyGrave()
    try:
        return pickle.load(open(p, 'rb'))
    except:
        return ProxyGrave()


if __name__ == '__main__':
    grave_obj_path = r"D:\github\work\spider\gov_bx\code\obj\grave.obj"
    proxy_impl = ProxyImpl(grave_obj_path)
    get_proxys(proxy_impl, 5)
    print(proxy_impl)
