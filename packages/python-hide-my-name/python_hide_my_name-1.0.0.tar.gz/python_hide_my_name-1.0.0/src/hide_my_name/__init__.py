__author__ = """Aria Bagheri"""
__email__ = 'ariab9342@gmail.com'
__version__ = '1.0.0'

import collections
import json
import re
from multiprocessing.pool import ThreadPool

import requests as requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.64 '
                  'Safari/537.36'
}


class HideMyName:
    timeout: int
    strict: bool
    session: requests.Session
    proxy_list: set
    _multiplier_base: int

    def __init__(self, timeout: int = 50, start_from_page: int = 0, strict: bool = False, initial_proxy_list=None):
        if initial_proxy_list is None:
            initial_proxy_list = set()
        self.initial_proxy_set = initial_proxy_list
        self.strict = strict
        self.timeout = timeout
        self._multiplier_base = start_from_page

    def _fetch_page(self, page: int):
        page_filter = ""
        if page != 0 or self._multiplier_base != 0:
            page_filter = f"&start={64 * (page + self._multiplier_base)}"
        response = requests.get(f"https://hidemy.name/en/proxy-list/?type=hs{page_filter}#list",
                                timeout=self.timeout, headers=headers).text
        if response:
            proxies = re.findall(
                r'<tr>.*?<td>(\d+.\d+.\d+.\d+).*?<td>(\d+).*?<td>(HTTPS?).*?</tr>',
                response
            )
            return proxies

    def _fetch_proxies(self, count: int):
        with ThreadPool() as p:
            proxies = p.map(self._fetch_page, range(count // 64 + 1))
            collections.deque(map(lambda x: self.initial_proxy_set.update(x), proxies))

    @staticmethod
    def test_proxy(lp: tuple):
        typ = lp[2].lower()
        ip = lp[0]
        port = lp[1]
        proxy_d = {typ: f"{typ}://{ip}:{port}"}
        try:
            s = requests.get(f"{typ}://api.ipify.org", timeout=100, headers=headers, proxies=proxy_d)
            if s.text == ip or "Cloudflare" in s.text:
                return ip, port, typ
            else:
                return False
        except IOError:
            return False
        except json.decoder.JSONDecodeError:
            return False

    def _check_proxies(self, check_proxies: set = None):
        proxies = check_proxies if check_proxies else self.initial_proxy_set
        successful_proxies = set()
        with ThreadPool() as p:
            successful_proxies.update(p.map(self.test_proxy, proxies))

        if False in successful_proxies:
            successful_proxies.remove(False)
        self.initial_proxy_set = successful_proxies
        return successful_proxies

    def get_proxies(self, count: int, base: int = 0):
        self._check_proxies()
        self._multiplier_base = base
        while len(self.initial_proxy_set) < count:
            self._fetch_proxies(count)
            self._check_proxies()
            self._multiplier_base += 1

        return self.initial_proxy_set
