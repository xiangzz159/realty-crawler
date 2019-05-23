# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/23 19:20

@desc:

'''

from base.errors import NetworkError, DDoSProtection, RequestTimeout, RequestError

from requests import Session
from requests.utils import default_user_agent
from requests.exceptions import HTTPError, Timeout, TooManyRedirects, RequestException
import logging
from ssl import SSLError
import re
import json
import time

__all__ = [
    'RealEstate',
]


class RealEstate(object):
    id = None
    session = None  # Session () by default
    cookie = None
    logger = None  # logging.getLogger(__name__) by default
    userAgent = None
    enableRateLimit = False
    rateLimit = 2000  # milliseconds = seconds * 1000
    timeout = 10000  # milliseconds = seconds * 1000
    userAgent = None
    userAgents = {
        'chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'chrome39': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    headers = None
    proxy = ''
    origin = '*'
    proxies = None
    verbose = False
    minFundingAddressLength = 10  # used in check_address
    substituteCommonCurrencyCodes = True
    lastRestRequestTimestamp = 0
    lastRestPollTimestamp = 0
    restRequestQueue = None
    restPollerLoopIsRunning = False
    rateLimitTokens = 16
    rateLimitMaxTokens = 16
    rateLimitUpdateTime = 0
    last_http_response = None
    last_json_response = None
    last_response_headers = None
    parseJsonResponse = False

    def __init__(self):
        self.userAgent = default_user_agent()
        self.session = self.session if self.session else Session()
        self.logger = self.logger if self.logger else logging.getLogger(__name__)
        self.headers = {} if self.headers is None else self.headers

    def __del__(self):
        if self.session:
            self.session.close()

    def handle_errors(self, code, reason, url, method, headers, body):
        pass

    def prepare_request_headers(self, headers=None):
        headers = headers or {}
        headers.update(self.headers)
        if self.userAgent:
            headers.update({'User-Agent': self.userAgents['chrome39']})
        if self.proxy:
            headers.update({'Origin': self.origin})
        headers.update({'Accept-Encoding': 'gzip, deflate'})
        return headers

    def raise_error(self, exception_type, url=None, method=None, error=None, details=None):
        if error:
            error = str(error)
        output = ' '.join([self.id] + [var for var in (url, method, error, details) if var is not None])
        raise exception_type(output)

    def fetch(self, url, method='GET', headers=None, body=None):
        if self.enableRateLimit:
            self.throttle()
        """Perform a HTTP request and return decoded JSON data"""
        request_headers = self.prepare_request_headers(headers)
        url = self.proxy + url

        if self.verbose:
            print("\nRequest:", method, url, request_headers, body)

        self.logger.debug("%s %s, Request: %s %s", method, url, request_headers, body)

        if body:
            body = body.encode()

        self.session.cookies.clear()

        response = None
        try:
            response = self.session.request(
                method,
                url,
                data=body,
                headers=request_headers,
                timeout=int(self.timeout / 1000),
                proxies=self.proxies
            )
            self.last_http_response = response.text
            self.last_response_headers = response.headers
            if self.verbose:
                print("\nResponse:", method, url, str(response.status_code), str(response.headers),
                      self.last_http_response)
            self.logger.debug("%s %s, Response: %s %s %s", method, url, response.status_code, response.headers,
                              self.last_http_response)
            response.raise_for_status()

        except Timeout as e:
            self.raise_error(RequestTimeout, method, url, e)

        except TooManyRedirects as e:
            self.raise_error(RequestError, url, method, e)

        except SSLError as e:
            self.raise_error(RequestError, url, method, e)

        except HTTPError as e:
            self.handle_errors(response.status_code, response.reason, url, method, self.last_response_headers,
                               self.last_http_response)
            self.handle_rest_errors(e, response.status_code, self.last_http_response, url, method)
            self.raise_error(RequestError, url, method, e, self.last_http_response)

        except RequestException as e:  # base exception class
            self.raise_error(RequestError, url, method, e, self.last_http_response)

        self.handle_errors(response.status_code, response.reason, url, method, None, self.last_http_response)
        return self.handle_rest_response(self.last_http_response, url, method, headers, body)

    def handle_rest_errors(self, exception, http_status_code, response, url, method='GET'):
        error = None
        if http_status_code in [418, 429]:
            error = DDoSProtection
        elif http_status_code in [404, 409, 500, 501, 502, 520, 521, 522, 525]:
            error = RequestError
        elif http_status_code in [422]:
            error = RequestError
        elif http_status_code in [400, 403, 405, 503, 530]:
            # special case to detect ddos protection
            error = RequestError
            if response:
                ddos_protection = re.search('(cloudflare|incapsula)', response, flags=re.IGNORECASE)
                if ddos_protection:
                    error = DDoSProtection
        elif http_status_code in [408, 504]:
            error = RequestTimeout
        elif http_status_code in [401, 511]:
            error = RequestError
        if error:
            self.raise_error(error, url, method, exception if exception else http_status_code, response)

    def handle_rest_response(self, response, url, method='GET', headers=None, body=None):
        try:
            if self.parseJsonResponse:
                self.last_json_response = json.loads(response) if len(response) > 1 else None
                return self.last_json_response
            else:
                return response
        except ValueError as e:  # ValueError == JsonDecodeError
            ddos_protection = re.search('(cloudflare|incapsula|overload|ddos)', response, flags=re.IGNORECASE)
            exchange_not_available = re.search(
                '(offline|busy|retry|wait|unavailable|maintain|maintenance|maintenancing)', response,
                flags=re.IGNORECASE)
            if ddos_protection:
                self.raise_error(DDoSProtection, method, url, None, response)
            if exchange_not_available:
                message = response + ' exchange downtime, exchange closed for maintenance or offline, DDoS protection or rate-limiting in effect'
                self.raise_error(RequestError, method, url, None, message)
            self.raise_error(RequestError, method, url, e, response)

    def throttle(self):
        now = float(self.milliseconds())
        elapsed = now - self.lastRestRequestTimestamp
        if elapsed < self.rateLimit:
            delay = self.rateLimit - elapsed
            time.sleep(delay / 1000.0)

    @staticmethod
    def seconds():
        return int(time.time())

    @staticmethod
    def milliseconds():
        return int(time.time() * 1000)

    @staticmethod
    def microseconds():
        return int(time.time() * 1000000)
