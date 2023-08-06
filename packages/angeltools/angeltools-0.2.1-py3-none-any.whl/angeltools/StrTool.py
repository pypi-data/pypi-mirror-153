import hashlib
import os
import random
import re
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import quote, urlparse, unquote

import urllib3
from scrapy import Selector
from scrapy.http import HtmlResponse


def get_domain(url):
    domain = urllib3.get_host(url)[1]
    if domain.startswith('www.'):
        domain = domain.lstrip('www.')
    return domain


def hash_str(data):
    md5 = hashlib.md5()
    md5.update(str(data).encode('utf-8'))
    return md5.hexdigest()


def gen_uid1():
    return str(uuid.uuid1())


def get_linux_cmd_path(name):
    res = [x.strip() for x in os.popen(f"whereis {name}").read().split(" ") if x.strip()]
    if len(res) > 1:
        return res[1]
    return None


class ScrapyXpath:
    """
    包装 scrapy response 的xpath方法，不用每次都 extract 再判断结果，使爬虫更整洁
    也可以传入由 requests 获取的 response text 和 url，变成 scrapy selector 对象方便提取
    """
    def __init__(self, scrapy_selector: Selector = None, url=None, html_content=None):
        """
        :param scrapy_selector:     response.xpath('//div[@class="xxx"]')
        """
        if scrapy_selector:
            self.raw = scrapy_selector
        elif url and html_content:
            self.raw = self.response_selector(url, html_content)
        else:
            raise ValueError('scrapy_selector or url and html_content required!')

    def scrapy_response(self, url, html_content):
        return HtmlResponse(url=url, body=html_content, encoding="utf-8")

    def response_selector(self, url, html_content):
        return self.scrapy_response(url, html_content).xpath('//html')

    def __map_str(self, map_dic, raw_str):
        if map_dic:
            n_res = ""
            for si in raw_str:
                t = map_dic.get(si, si)
                n_res += t
        else:
            n_res = raw_str
        return n_res

    def xe(self, xpath_str, strip_str=None, map_dic=None, sep=None, replace_str=None, auto_sep=False, default=""):
        """
        selector = response.xpath('//div[@class="xxx"]')
        sx = ScrapyXpath(selector)

        div_text_list = sx.xe('.//text()')
        div_link = sx.xe('./@href')

        :param xpath_str:   xpath表达式
        :param strip_str:
        :param map_dic:
        :param sep:
        :param replace_str:
        :param auto_sep:
        :param default:
        :return:
        """
        res = self.raw.xpath(xpath_str).extract()
        if res:
            res = [x.strip() for x in res if x and x.strip()]
            if not res:
                return default
            elif len(res) == 1:
                res = res[0].strip(strip_str) if strip_str else res[0]
                if replace_str:
                    res = res.replace(replace_str, "")
                if auto_sep:
                    res = "".join([x.strip() for x in res.split("\n") if x and x.strip()])
                res = self.__map_str(map_dic, res) or res
                return res
            else:
                nw = []
                for w in res:
                    if replace_str:
                        w = w.replace(replace_str, "")
                    if auto_sep:
                        w = "".join([x.strip() for x in w.split("\n") if x and x.strip()])
                    nw.append(self.__map_str(map_dic, w) or w)
                if sep is not None:
                    nw = sep.join(nw)
                return nw
        return default


class UrlFormat:
    def __init__(self, url=None):
        self.url = url

    def quote_str(self, s):
        res = quote(str(s).encode())
        return res

    def unquote_str(self, s):
        res = unquote(s)
        return res

    def make_url(self, base, params_add_dic, quote_param=True):
        new_url = base
        new_url += f'?{"&".join([f"{k}={self.quote_str(v) if quote_param else v}" for k, v in params_add_dic.items()])}'
        return new_url

    def split_url(self):
        url_data = dict()
        if self.url:
            temp_data = urlparse(unquote(self.url))
            url_data["queries"] = {x.split("=")[0]: unquote("=".join(x.split("=")[1:])) for x in temp_data.query.split("&")}
            url_data["host"] = temp_data.netloc
            url_data["protocol"] = temp_data.scheme
            url_data["path"] = temp_data.path
            url_data["require_params"] = temp_data.params
            url_data["fragment"] = temp_data.fragment
        return url_data

    def url_format(self, url_base=None, require_params=None, params_only=False, unquote_params=False, unquote_times=1):
        """
        获取url参数
        :param url_base:        url 前缀
        :param require_params:  需要的参数名，True全部，或者参数名列表 ['page', 'name', ...]
        :param params_only:     True只返回参数字典，否则根据require_params重组url
        :param unquote_params:  是否解密url
        :param unquote_times:   解密次数
        :return:
        """
        if not self.url:
            return {}
        if require_params is None:
            require_params = True
        if url_base:
            self.url = self.join_up([url_base, self.url], duplicate_check=True)
        if re.findall(r'\?', self.url):
            u_temp = self.url.split('?')
            new_url = re.sub(r"ref=[\s\S]+", "", u_temp[0])
            if require_params is True:
                dic = {x.split('=')[0]: x.split('=')[1].strip(" ").strip("/") for x in u_temp[1].split('&') if
                       x.split('=')[0] and len(x.split('=')) > 1}
            else:
                require_params = set(require_params)
                dic = {x.split('=')[0]: x.split('=')[1].strip(" ").strip("/") for x in u_temp[1].split('&') if
                       x.split('=')[0] in require_params and len(x.split('=')) > 1}
            if unquote_params:
                for _ in range(unquote_times):
                    dic = {k: self.unquote_str(v) for k, v in dic.items()}
            if params_only:
                return dic
            if dic:
                new_url += '?{}'.format("&".join(["{}={}".format(k, v) for k, v in dic.items()]))
        else:
            if params_only:
                return {}
            new_url = re.sub(r"ref=[\s\S]+", "", self.url)
        return new_url

    def join_up(self, path_lis, duplicate_check=False, sep=None) -> str:
        """
        拼接路径用的
        url 或者 文件路径都可以
        自动检测是否是url，自动加上分隔符
        如果不确定是否重复了，就把 duplicate_check 设置为 True

        :param path_lis: 需要传入待拼接的路径的列表，['part1', 'part2', 'part3' ...]，注意顺序
        :param duplicate_check: 去掉重复的路径，注意有些路径是重复的，所以默认关闭
        :param sep: 自定义间隔符， 如果不确定就留空
        :return: 返回拼接好的路径字符串 str
        """
        is_url = any([True if re.findall(r'(https?://)|(www\.)', x)
                      else False for x in path_lis if x])
        if sep is None and not is_url:
            sep = os.sep
        elif sep is None and is_url:
            sep = '/'
        path_lis = [x.strip('/').strip('\\') for x in path_lis if x]
        paths_rev = path_lis[::-1]
        new_url = ''
        if duplicate_check:
            for p in paths_rev:
                if p and p not in new_url:
                    new_url = p + sep + new_url
        else:
            new_url = sep.join(path_lis)
        return new_url


class FileLock:
    """
    使用文件操作实现的异步锁

    使用方式：
    with FileLock(lock_id='xxxx', timeout=xx.xx):
        do_the_jobs()

    """
    def __init__(self, lock_id, timeout: float or int = None):
        self.timeout = float(timeout) if timeout else 3600 * 24 * 30 * 12
        self.__init_lock(lock_id)
        self.fps = self.fp.absolute()
        self.enter_with_acquire = False

    def __enter__(self):
        if not self.enter_with_acquire:
            self.__acquire_lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__exit_lock()

    def __call__(self, *args, **kwargs):
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']

    def __init_lock(self, lock_id):
        lock_id_hash = hash_str(str(lock_id))

        if sys.platform == 'linux':
            self.fp = Path(f'/tmp/{lock_id_hash}.lock')
        else:
            self.fp = Path(__file__).parent / f'{lock_id_hash}.lock'

    def __acquire_lock(self):
        expire_time = time.time() + self.timeout
        try:
            while self.__get_size() and time.time() - expire_time < 0:
                self.__wait()
        except KeyboardInterrupt:
            sys.exit()
        self.__add_num()
        return self

    def __read_num(self):
        num = "0"
        try:
            with open(self.fps, 'r') as rf:
                num = rf.read().strip()
        except:pass
        num = int(num) if num else 0
        return num

    def __get_size(self):
        return 0 if not os.path.exists(self.fps) else os.path.getsize(self.fps)

    def __add_num(self):
        self.fp.write_text("1" * (self.__get_size() + 1))

    def __sub_num(self):
        num = self.__get_size()
        if num > 1:
            self.fp.write_text("1" * (num - 1))
        else:
            os.remove(self.fps)

    def __occupy(self):
        if not self.fp.exists():
            return False
        num = self.fp.read_text(encoding='utf-8')
        if num and num.isdigit() and int(num) >= 1:
            return True
        return False

    def __exit_lock(self):
        try:
            self.__sub_num()
        except:
            pass

    def __wait(self):
        time.sleep(random.randint(1, 10)/10)

    def acquire(self, **kwargs):
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        self.enter_with_acquire = True
        return self.__acquire_lock()

    def lock_time(self, format_time: str or bool = False):
        """
        :param format_time: True or "%Y-%m-%d %H:%M:%S" or False
        :return:
        """

        if self.fp.exists():
            tm = os.path.getatime(self.fps)
        else:
            tm = 0
        if not format_time:
            return tm
        else:
            if format_time is True:
                format_time = '%Y-%m-%d %H:%M:%S'
            return time.strftime(format_time, time.localtime(tm))

    def mark(self):
        """
        更新文件日期，返回更新后的时间戳
        :return:
        """
        self.fp.touch()
        return self.lock_time()

    def unmark(self):
        """
        清除锁文件，返回最后更新时间戳
        :return:
        """
        lock_time = self.lock_time()
        self.__exit_lock()
        return lock_time


if __name__ == '__main__':
    # with FileLock('test-lock', timeout=10) as lock:
    #     print(lock.lock_time(format_time=True))
    #     for i in range(100):
    #         print(i)
    #         time.sleep(0.5)
    #     print(lock.lock_time(format_time=True))

    from angeltools.Slavers import BigSlaves

    def do_job(job_name):
        time.sleep(random.randint(1, 10) / 10)
        with FileLock('test-lock', timeout=1000):
            for i in range(20):
                print(f"{job_name}: {i}")
                time.sleep(0.5)

    BigSlaves(7).work(do_job, [x for x in "ABCDEFGHIJKLMN"])

    # uf = UrlFormat('http://www.baidu.com?page=1&user=me&name=%E5%BC%A0%E4%B8%89')
    # print(uf.split_url())
