import hashlib
import json
import warnings
from datetime import datetime

import urllib3
from Crypto.Hash import RIPEMD160
from latest_user_agents import get_random_user_agent

from unofficial_livecounts_api import env
from unofficial_livecounts_api.error import RequestApiError


def __get_http_client():
    if env.PROXY_ENABLED == "on" and env.PROXY_SERVER:
        return urllib3.ProxyManager(
            env.PROXY_SERVER, cert_reqs="CERT_NONE", assert_hostname=False
        )
    else:
        return urllib3.PoolManager(cert_reqs="CERT_NONE", assert_hostname=False)


warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
http_client = __get_http_client()


def send_request(url):
    try:
        response = http_client.request(
            method="GET",
            url=url,
            headers=__get_default_header(),
        )
        data = json.loads(response.data.decode("utf-8"))
        if not data.get("success", True):
            raise RequestApiError(
                f"server response that it's not success, query: {url}"
            )
        return data
    except Exception as e:
        if isinstance(e, RequestApiError):
            raise e
        raise RequestApiError(f"api server error, query: {url}") from e


def __get_default_header():
    x_ajay = int(datetime.now().timestamp() * 1000)
    x_catto = __get_ripemd160_hash(str(x_ajay))
    x_midas = __get_sha384_hash(__get_sha256_hash(str(x_ajay + 64)))
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "*",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "https://livecounts.io",
        "Referer": "https://livecounts.io/",
        "X-Ajay": x_ajay,
        "X-Catto": x_catto,
        "X-Midas": x_midas,
    }


def __get_ripemd160_hash(message: str):
    h = RIPEMD160.new()
    h.update(message.encode("utf-8"))
    return h.hexdigest()


def __get_sha256_hash(message):
    sha256 = hashlib.sha256()
    sha256.update(message.encode("utf-8"))
    return sha256.hexdigest()


def __get_sha384_hash(message):
    sha384 = hashlib.sha384()
    sha384.update(message.encode("utf-8"))
    return sha384.hexdigest()
